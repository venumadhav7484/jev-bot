"""/psychro-data: same parser and Jev request as pilot v2, visitor-facing input errors, hosted route and exposure."""
import io
import json
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT/'experiments/psychrometric-charts'
sys.path.insert(0, str(ROOT/'scripts'))
sys.path.insert(0, str(EXP/'src'))
import psychro_try
import cloud_bot as app
from cloud_stack import template
import deploy_cloud


def pilot_rows():
    rows = []
    for name in ('pilot_questions.jsonl', 'pilot2_questions.jsonl'):
        path = EXP/'data'/name
        if path.exists():
            rows += [json.loads(l) for l in path.read_text(encoding='utf-8').splitlines()]
    return rows


class SameAsPilot(unittest.TestCase):
    @unittest.skipUnless(pilot_rows(), 'pilot data not present')
    def test_parser_and_request_match_pilot_v2(self):
        import pilot_v2
        from questions import extract
        for row in pilot_rows():
            self.assertEqual(psychro_try.extract(row['text']), extract(row['text']))
            text, numbers = psychro_try.parse({'text': row['text']})
            self.assertEqual(psychro_try.payload(text, numbers), pilot_v2.payload(row['text']))

    def test_input_errors_are_for_visitors(self):
        for body, word in (({'text': 'what is the dew point?'}, 'has 0'), ({'text': 'DB 30 WB 22 RH 50'}, 'has 3'), ({'text': 'x' * 301}, '300')):
            with self.assertRaises(ValueError) as caught:
                psychro_try.parse(body)
            self.assertIn(word, str(caught.exception))

    def test_units_fix_single_option_numbers_without_jev(self):
        text, numbers = psychro_try.parse({'text': 'RH 55%, DP 14 C. Need WB.'})
        body = psychro_try.payload(text, numbers)
        self.assertNotIn('value_1', body['questions'])      # 55% can only be relative humidity
        self.assertEqual(list(body['questions']['value_2']['criteria']), ['dry-bulb temperature', 'wet-bulb temperature', 'dew-point temperature'])
        answers = {'value_2': {'choice': 'dew-point temperature', 'confidence': 0.9, 'probabilities': {'dew-point temperature': 0.9}},
                   'asked_first': {'choice': 'wet-bulb temperature', 'confidence': 0.8}}
        shaped = psychro_try.shape({'answers': answers, 'usage': {'input_tokens': 700}}, numbers, 0.4)
        self.assertEqual([n['label'] for n in shaped['numbers']], ['rh', 'tdp'])
        self.assertEqual([n['source'] for n in shaped['numbers']], ['unit', 'jev'])
        self.assertEqual(shaped['highlight'], 'twb')

    def test_unreadable_answer_is_a_failure(self):
        text, numbers = psychro_try.parse({'text': 'DB 30 WB 22 dew point?'})
        with self.assertRaises(psychro_try.Unavailable):
            psychro_try.shape({'answers': {'asked_first': {'choice': 'dew-point temperature'}}}, numbers, 0.1)


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

    def event(self, body):
        return {'rawPath': '/api/psychro', 'requestContext': {'http': {'method': 'POST'}},
                'headers': {'content-type': 'application/json'}, 'body': json.dumps(body)}

    def test_bad_question_explains_without_counting_or_calling(self):
        result = app.api(self.event({'text': 'what is the dew point?'}), None)
        self.assertEqual(result['statusCode'], 400)
        self.assertIn('exactly two values', json.loads(result['body'])['error'])
        self.db.update_item.assert_not_called(); self.fn.invoke.assert_not_called()

    def test_reading_goes_through_worker_with_its_own_counter(self):
        self.fn.invoke.return_value = {'Payload': io.BytesIO(json.dumps({'numbers': [], 'seconds': 0.4}).encode())}
        with patch('builtins.print') as printed:
            result = app.api(self.event({'text': 'DB 30 private-site-note WB 22'}), None)
        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(json.loads(self.fn.invoke.call_args.kwargs['Payload'])['psychro']['text'], 'DB 30 private-site-note WB 22')
        self.assertTrue(self.db.update_item.call_args.kwargs['Key']['pk']['S'].startswith('psychro#'))
        self.assertNotIn('private-site-note', ''.join(str(c) for c in printed.call_args_list))

    def test_worker_uses_its_own_key(self):
        with patch.object(psychro_try, 'ask', return_value={'numbers': []}) as ask:
            self.assertEqual(app.worker({'psychro': {'text': 'DB 30 WB 22'}}, None), {'numbers': []})
        self.assertEqual(ask.call_args.args[2], 'k')

    def test_route_page_and_assets_are_deployed(self):
        routes = [r['Properties']['RouteKey'] for r in template()['Resources'].values() if r['Type'] == 'AWS::ApiGatewayV2::Route']
        self.assertIn('POST /api/psychro', routes)
        self.assertIn('psychro_try.py', deploy_cloud.MODULES)
        self.assertEqual(deploy_cloud.PAGES['psychro-data'], 'psychro.html')
        for name in ('psychro.js', 'psychro.css', 'psychro-solver.mjs', 'psychro-flycarpet.svg', 'psychro-upload.mjs',
                     'vendor/tesseract/tesseract.min.js', 'vendor/tesseract/core/tesseract-core-simd-lstm.wasm.js', 'vendor/tesseract/lang/eng.traineddata.gz'):
            self.assertTrue((ROOT/'web'/name).is_file(), name)
        self.assertNotIn('style="', (ROOT/'web/psychro-flycarpet.svg').read_text())   # CSP-safe: no inline styles
        self.assertNotIn('onclick', (ROOT/'web/psychro-flycarpet.svg').read_text())


if __name__ == '__main__':
    unittest.main()
