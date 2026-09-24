"""Hosted boundary tests: auth, durable jobs, duplicate delivery and exposure."""
import hashlib
import json
import os
from pathlib import Path
import sys
import time
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import cloud_bot as app
from cloud_stack import template


class Conditional(Exception):
    pass


class Transaction(Exception):
    pass


class CloudTests(unittest.TestCase):
    def setUp(self):
        self.env = patch.dict(os.environ, {'ACCESS_HASH': hashlib.sha256(b'test-code').hexdigest(),
            'TABLE': 'jobs', 'BUCKET': 'private-bucket', 'WORKER': 'worker', 'JEV_AVAILABLE': 'true',
            'WRITER_AVAILABLE': 'true', 'DAILY_LIMIT': '50', 'MAX_CONCURRENT': '1'})
        self.env.start()
        self.addCleanup(self.env.stop)
        self.db, self.s3, self.fn = MagicMock(), MagicMock(), MagicMock()
        self.db.exceptions.ConditionalCheckFailedException = Conditional
        self.db.exceptions.TransactionCanceledException = Transaction
        self.s3.head_object.side_effect = RuntimeError('NoSuchKey')  # Default: no reusable answer.
        self.mock = patch.object(app, 'clients', return_value=(self.db, self.s3, self.fn))
        self.mock.start()
        self.addCleanup(self.mock.stop)

    def event(self, method='POST', path='/api/jobs', body=None, token='test-code'):
        return {'rawPath': path, 'requestContext': {'http': {'method': method}},
                'headers': {'authorization': 'Bearer '+token, 'content-type': 'application/json'},
                'body': json.dumps(body if body is not None else {'idea': 'Route support tickets'})}

    def test_public_answers_do_not_require_credentials(self):
        event = self.event(token='')
        event['headers'].pop('authorization')
        result = app.api(event, None)
        self.assertEqual(result['statusCode'], 202)
        self.fn.invoke.assert_called_once()

    def test_public_config_has_no_credentials(self):
        result = app.api(self.event('GET', '/api/config', token=''), None)
        data = json.loads(result['body'])
        self.assertFalse(data['access_required'])
        self.assertFalse(data['s3_available'])
        self.assertNotIn('test-code', result['body'])

    def test_invalid_input_cannot_invoke(self):
        for body in ([], {'idea': 'x'}, {'idea': 'x'*6001}, {'idea': 'valid', 'source': 's3'}, {'idea': 'valid', 'mode': 'invalid'}):
            self.assertEqual(app.api(self.event(body=body), None)['statusCode'], 400)
        self.fn.invoke.assert_not_called()

    def test_create_uses_atomic_quota_and_lease_then_async_worker(self):
        result = app.api(self.event(), None)
        self.assertEqual(result['statusCode'], 202)
        transaction = self.db.transact_write_items.call_args.kwargs['TransactItems']
        self.assertEqual(len(transaction), 3)
        self.assertIn('ConditionExpression', transaction[0]['Put'])
        self.assertIn('ConditionExpression', transaction[1]['Update'])
        self.assertEqual(self.fn.invoke.call_args.kwargs['InvocationType'], 'Event')

    def test_busy_or_quota_cannot_invoke_worker(self):
        self.db.transact_write_items.side_effect = Transaction()
        self.db.get_item.side_effect = lambda **kw: {'Item': app.item(lease=int(time.time())+900)} if kw['Key']['pk']['S']=='lock' else {}
        result = app.api(self.event(), None)
        self.assertEqual(result['statusCode'], 429)
        self.assertEqual(json.loads(result['body'])['code'], 'busy')
        self.fn.invoke.assert_not_called()

    def test_daily_quota_and_database_failure_have_distinct_errors(self):
        self.db.transact_write_items.side_effect = Transaction()
        self.db.get_item.return_value = {'Item': app.item(used=50)}
        result = app.api(self.event(), None)
        self.assertEqual(json.loads(result['body'])['code'], 'daily_limit')
        self.assertGreater(int(result['headers']['retry-after']), 0)
        self.db.get_item.return_value = {}
        result = app.api(self.event(), None)
        self.assertEqual(result['statusCode'], 503)
        self.assertEqual(json.loads(result['body'])['code'], 'capacity_check_failed')
        self.fn.invoke.assert_not_called()

    def test_worker_releases_its_assigned_slot_only(self):
        with patch('research_answer.answer', return_value={'coverage': {'full_library_evaluated': True}}):
            app.worker({'id':'a'*32,'idea':'test','mode':'evidence','slot':'lock#9'}, None)
        self.assertEqual(self.db.delete_item.call_args.kwargs['Key'], app.item(pk='lock#9'))
        self.assertEqual(self.db.delete_item.call_args.kwargs['ExpressionAttributeValues'], app.item(**{':id':'a'*32}))

    def test_uncertain_queue_result_preserves_lease_and_job_id(self):
        self.fn.invoke.side_effect = RuntimeError('secret provider body')
        result = app.api(self.event(), None)
        self.assertEqual(result['statusCode'], 202)
        self.assertIn('id', json.loads(result['body']))
        self.assertNotIn('secret provider body', result['body'])
        self.db.delete_item.assert_not_called()

    def test_expired_results_cannot_be_read(self):
        self.db.get_item.return_value = {'Item': app.item(ttl=1)}
        result = app.api(self.event('GET', '/api/jobs/'+'a'*32), None)
        self.assertEqual(result['statusCode'], 404)
        self.s3.get_object.assert_not_called()

    def test_timeout_reported_instead_of_infinite_poll(self):
        self.db.get_item.return_value = {'Item': app.item(ttl=int(time.time())+100, status='running', deadline=1)}
        result = app.api(self.event('GET', '/api/jobs/'+'a'*32), None)
        self.assertEqual(json.loads(result['body'])['status'], 'failed')

    def test_duplicate_worker_delivery_skips_provider(self):
        self.db.update_item.side_effect = Conditional()
        with patch('research_answer.answer') as answer:
            app.worker({'id': 'a'*32, 'idea': 'test', 'mode': 'evidence'}, None)
            answer.assert_not_called()
        self.s3.put_object.assert_not_called()

    def test_worker_persists_answer_and_releases_own_lease(self):
        with patch('research_answer.answer', return_value={'coverage': {'full_library_evaluated': True}}):
            app.worker({'id': 'a'*32, 'idea': 'test', 'mode': 'evidence'}, None)
        self.assertEqual(self.s3.put_object.call_args.kwargs['Key'], 'jobs/'+'a'*32+'.json')
        self.assertEqual(self.db.delete_item.call_args.kwargs['ExpressionAttributeNames'], {'#owner': 'owner'})

    def test_worker_error_never_exposes_provider_body(self):
        with patch('research_answer.answer', side_effect=RuntimeError('secret provider body')):
            app.worker({'id': 'a'*32, 'idea': 'test', 'mode': 'evidence'}, None)
        self.assertNotIn('secret provider body', str(self.db.update_item.call_args))
        self.db.delete_item.assert_called_once()

    def test_identical_idea_reuses_cached_answer_without_quota_or_worker(self):
        self.s3.head_object.side_effect = None
        result = app.api(self.event(body={'idea': '  Route   SUPPORT tickets ', 'mode': 'written'}), None)
        self.assertEqual(result['statusCode'], 202)
        self.fn.invoke.assert_not_called()
        self.db.transact_write_items.assert_not_called()
        stored = self.db.put_item.call_args.kwargs['Item']
        self.assertEqual(stored['status']['S'], 'complete')
        self.assertEqual(stored['result_key']['S'], app.cache_key('route support tickets', 'written'))
        self.assertTrue(stored['result_key']['S'].startswith('cache/'))

    def test_reused_answer_is_read_from_cache_and_marked(self):
        now = int(time.time())
        self.db.get_item.return_value = {'Item': {'status': {'S': 'complete'}, 'created': {'N': str(now)}, 'ttl': {'N': str(now+60)},
                                                  'progress': {'S': '{}'}, 'result_key': {'S': 'cache/x.json'}}}
        self.s3.get_object.return_value = {'Body': MagicMock(read=lambda: b'{"idea": "x"}')}
        result = app.api(self.event('GET', '/api/jobs/'+'a'*32), None)
        self.assertEqual(self.s3.get_object.call_args.kwargs['Key'], 'cache/x.json')
        self.assertTrue(json.loads(result['body'])['result']['reused'])

    def test_worker_caches_only_complete_checked_designs(self):
        good = {'coverage': {'search_complete': True}, 'judgments': {'fit': {}}, 'writer': {'status': 'success'}, 'execution': {'status': 'complete'}}
        self.assertTrue(app.reusable(good))
        for change in ({'writer': {'status': 'invalid_output'}}, {'execution': {'status': 'unavailable'}}, {'judgments': None}, {'coverage': {'search_complete': False}}):
            self.assertFalse(app.reusable({**good, **change}))

    def test_infrastructure_separates_site_jobs_and_keys(self):
        stack = template()
        resources = stack['Resources']
        api_env = resources['Api']['Properties']['Environment']['Variables']
        self.assertNotIn('jev_api_key', api_env)
        self.assertNotIn('glm_key', api_env)
        policy = resources['BucketPolicy']['Properties']['PolicyDocument']['Statement'][0]
        self.assertTrue(policy['Resource']['Fn::Sub'].endswith('/site/*'))
        self.assertIn('AWS:SourceArn', policy['Condition']['StringEquals'])
        self.assertEqual(resources['ApiCache']['Properties']['CachePolicyConfig']['MaxTTL'], 0)
        self.assertEqual(resources['AsyncPolicy']['Properties']['MaximumRetryAttempts'], 0)
        self.assertTrue(stack['Parameters']['JevKey']['NoEcho'])


if __name__ == '__main__':
    unittest.main()
