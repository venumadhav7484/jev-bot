"""Bharat test live demo: input checks, the exact Jev request, failure handling, quota and exposure."""
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
import io
import json
import os
from pathlib import Path
import sys
import threading
import unittest
import urllib.error
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
import bharat_try
import cloud_bot as app
from cloud_stack import template
import deploy_cloud
import serve_bot

SECRET_TEXT = 'visitor-private-sentence'


def jev_response(task='topic', choice='sports'):
    keys = list(bharat_try.SPEC[task]['criteria'])
    probs = {k: (0.9 if k == choice else 0.1 / (len(keys) - 1)) for k in keys}
    return {'model': 'jev-1.13.0', 'answers': {task: {'choice': choice, 'confidence': 0.9, 'probabilities': probs}},
            'usage': {'input_tokens': 600, 'output_tokens': 80}}


class Reply(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


def http_error(code):
    return urllib.error.HTTPError(bharat_try.API, code, 'error', {}, io.BytesIO(b'provider detail private-key'))


class Core(unittest.TestCase):
    def test_parse_accepts_both_tasks_and_trims(self):
        self.assertEqual(bharat_try.parse({'task': 'topic', 'text': '  నమస్తే  '}), ('topic', 'నమస్తే'))
        self.assertEqual(bharat_try.parse({'task': 'intent', 'text': 'x' * 500}), ('intent', 'x' * 500))

    def test_parse_rejects_bad_input(self):
        for body in ([], {'task': 'topic'}, {'task': 'topic', 'text': '   '}, {'task': 'topic', 'text': 'x' * 501},
                     {'task': 'chat', 'text': 'hi'}, {'task': 'topic', 'text': 5}):
            with self.assertRaises(ValueError):
                bharat_try.parse(body)

    def test_payload_is_the_tested_question(self):
        body = bharat_try.payload('intent', 'wake me at six')
        question = body['questions']['intent']
        self.assertEqual(body['model'], 'jev-1.13.0')
        self.assertEqual(len(question['criteria']), 60)
        self.assertEqual(question['instructions'], bharat_try.SPEC['intent']['instructions'])
        self.assertEqual(len(bharat_try.payload('topic', 'x')['questions']['topic']['criteria']), 7)

    def test_shape_ranks_options_and_prices_input_tokens(self):
        result = bharat_try.shape('intent', jev_response('intent', 'alarm_set'), 0.4123)
        self.assertEqual(result['label'], bharat_try.SPEC['intent']['criteria']['alarm_set'])
        self.assertEqual(len(result['ranked']), 5)
        self.assertEqual(result['ranked'][0]['key'], 'alarm_set')
        self.assertAlmostEqual(result['usd'], 600 * 0.042 / 1e6)
        self.assertEqual(result['seconds'], 0.412)
        self.assertEqual(len(bharat_try.shape('topic', jev_response(), 0.3)['ranked']), 7)

    def test_unreadable_answer_is_a_failure_not_a_guess(self):
        with self.assertRaises(bharat_try.Unavailable):
            bharat_try.shape('topic', {'answers': {'topic': {'choice': 'cooking'}}}, 0.1)

    def test_busy_gateway_is_retried_once(self):
        opener = MagicMock()
        opener.open.side_effect = [http_error(429), Reply(json.dumps(jev_response()).encode())]
        with patch.object(bharat_try.urllib.request, 'build_opener', return_value=opener), patch.object(bharat_try.time, 'sleep'):
            self.assertEqual(bharat_try.ask('topic', 'x', 'k')['choice'], 'sports')
        self.assertEqual(opener.open.call_count, 2)

    def test_failures_use_visitor_language_without_provider_detail(self):
        cases = [[http_error(403)], [http_error(500), http_error(500)], [urllib.error.URLError('down')], [http_error(401)]]
        for side_effect in cases:
            opener = MagicMock()
            opener.open.side_effect = side_effect
            with patch.object(bharat_try.urllib.request, 'build_opener', return_value=opener), patch.object(bharat_try.time, 'sleep'):
                with self.assertRaises(bharat_try.Unavailable) as caught:
                    bharat_try.ask('topic', 'x', 'k')
            self.assertNotIn('private-key', str(caught.exception))
            self.assertNotIn('HTTP', str(caught.exception))


class Conditional(Exception):
    pass


class Hosted(unittest.TestCase):
    def setUp(self):
        env = patch.dict(os.environ, {'TABLE': 'jobs', 'BUCKET': 'b', 'WORKER': 'worker', 'jev_api_key': 'k'})
        env.start(); self.addCleanup(env.stop)
        self.db, self.fn = MagicMock(), MagicMock()
        self.db.exceptions.ConditionalCheckFailedException = Conditional
        mock = patch.object(app, 'clients', return_value=(self.db, MagicMock(), self.fn))
        mock.start(); self.addCleanup(mock.stop)

    def event(self, body, content_type='application/json'):
        return {'rawPath': '/api/try', 'requestContext': {'http': {'method': 'POST'}},
                'headers': {'content-type': content_type}, 'body': json.dumps(body)}

    def worker_returns(self, value, error=None):
        self.fn.invoke.return_value = {'Payload': io.BytesIO(json.dumps(value).encode()), **({'FunctionError': error} if error else {})}

    def test_invalid_input_never_counts_or_invokes(self):
        for body in ({'task': 'topic', 'text': ''}, {'task': 'x', 'text': 'hi'}, {'task': 'topic', 'text': 'x' * 501}):
            self.assertEqual(app.api(self.event(body), None)['statusCode'], 400)
        self.assertEqual(app.api(self.event({'task': 'topic', 'text': 'hi'}, 'text/plain'), None)['statusCode'], 415)
        self.db.update_item.assert_not_called()
        self.fn.invoke.assert_not_called()

    def test_daily_limit_stops_live_calls(self):
        self.db.update_item.side_effect = Conditional()
        result = app.api(self.event({'task': 'topic', 'text': 'hi'}), None)
        self.assertEqual(result['statusCode'], 429)
        self.assertIn('recorded answers still work', json.loads(result['body'])['error'])
        self.fn.invoke.assert_not_called()

    def test_answer_goes_through_the_worker_and_text_is_not_logged(self):
        self.worker_returns({'choice': 'sports', 'seconds': 0.4})
        with patch('builtins.print') as printed:
            result = app.api(self.event({'task': 'topic', 'text': SECRET_TEXT}), None)
        self.assertEqual(result['statusCode'], 200)
        call = self.fn.invoke.call_args.kwargs
        self.assertEqual(call['InvocationType'], 'RequestResponse')
        self.assertEqual(json.loads(call['Payload'])['try'], {'task': 'topic', 'text': SECRET_TEXT})
        self.assertNotIn(SECRET_TEXT, ''.join(str(c) for c in printed.call_args_list))
        self.assertTrue(self.db.update_item.call_args.kwargs['Key']['pk']['S'].startswith('try#'))

    def test_worker_failures_become_plain_errors(self):
        self.worker_returns({'error': 'Jev is busy or unavailable right now. Please try again in a moment.'})
        result = app.api(self.event({'task': 'topic', 'text': 'hi'}), None)
        self.assertEqual((result['statusCode'], json.loads(result['body'])['error'][:6]), (502, 'Jev is'))
        self.worker_returns({'errorMessage': 'Traceback private-key'}, 'Unhandled')
        result = app.api(self.event({'task': 'topic', 'text': 'hi'}), None)
        self.assertEqual(result['statusCode'], 502)
        self.assertNotIn('private-key', result['body'])

    def test_worker_uses_its_own_key(self):
        with patch.object(bharat_try, 'ask', return_value={'choice': 'sports'}) as ask:
            self.assertEqual(app.worker({'try': {'task': 'topic', 'text': 'hi'}}, None), {'choice': 'sports'})
        ask.assert_called_once_with('topic', 'hi', 'k')
        self.assertIn('error', app.worker({'try': {'task': 'topic', 'text': ''}}, None))

    def test_route_and_bundle_include_the_demo(self):
        routes = [r['Properties']['RouteKey'] for r in template()['Resources'].values() if r['Type'] == 'AWS::ApiGatewayV2::Route']
        self.assertIn('POST /api/try', routes)
        self.assertIn('bharat_try.py', deploy_cloud.MODULES)
        self.assertIn('bharat_spec.json', deploy_cloud.DATA)
        for name in ('bharat.js', 'bharat.css', 'bharat-samples.json'):
            self.assertIn(name, deploy_cloud.ASSETS)
            self.assertTrue((ROOT/'web'/name).is_file())
        self.assertEqual(deploy_cloud.PAGES['bharat-test-demo'], 'bharat.html')


class Local(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), serve_bot.Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown(); cls.server.server_close(); cls.thread.join()

    def request(self, method, path, body=None):
        conn = HTTPConnection('127.0.0.1', self.server.server_port, timeout=5)
        conn.request(method, path, body, {'Content-Type': 'application/json'} if body is not None else {})
        response = conn.getresponse(); data = response.read(); conn.close()
        return response.status, data

    def test_page_and_samples_are_served(self):
        for path in ('/bharat-test-demo', '/bharat-test-demo/'):
            code, page = self.request('GET', path)
            self.assertEqual(code, 200)
            self.assertIn(b'See <em>Jev</em>', page)
        code, data = self.request('GET', '/bharat-samples.json')
        samples = json.loads(data)
        self.assertEqual((code, len(samples['topic']['languages']), len(samples['intent']['locales'])), (200, 25, 8))

    def test_live_route_contract(self):
        with patch.dict(os.environ, {'jev_api_key': 'k'}), patch.object(bharat_try, 'ask', return_value={'choice': 'sports'}):
            self.assertEqual(self.request('POST', '/api/try', json.dumps({'task': 'topic', 'text': 'hi'})), (200, b'{"choice": "sports"}'))
        self.assertEqual(self.request('POST', '/api/try', json.dumps({'task': 'topic', 'text': ''}))[0], 400)
        with patch.dict(os.environ, {'jev_api_key': 'k'}), patch.object(bharat_try, 'ask', side_effect=bharat_try.Unavailable('Jev is busy.')):
            self.assertEqual(self.request('POST', '/api/try', json.dumps({'task': 'topic', 'text': 'hi'})), (502, b'{"error": "Jev is busy."}'))


if __name__ == '__main__':
    unittest.main()
