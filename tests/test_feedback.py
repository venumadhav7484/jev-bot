"""Public feedback boundary: validate, deduplicate, expire and log only feedback."""
import base64
import contextlib
import io
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

class FeedbackTests(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock()
        self.db.exceptions.ConditionalCheckFailedException = Conditional
        self.db.get_item.return_value = {'Item': app.item(status='complete', ttl=int(time.time())+500)}
        self.patch = patch.object(app, 'clients', return_value=(self.db, MagicMock(), MagicMock()))
        self.patch.start(); self.addCleanup(self.patch.stop)
        self.env = patch.dict(os.environ, TABLE='test-jobs'); self.env.start(); self.addCleanup(self.env.stop)

    def submit(self, payload, encoded=False):
        raw=json.dumps(payload)
        event={'rawPath':'/api/feedback', 'requestContext':{'http':{'method':'POST'}},
               'headers':{'content-type':'application/json'}, 'body':raw}
        if encoded:
            event.update(body=base64.b64encode(raw.encode()).decode(), isBase64Encoded=True)
        output=io.StringIO()
        with contextlib.redirect_stdout(output):
            response=app.api(event, None)
        return response['statusCode'], output.getvalue()

    def test_rating_and_comment_log_only_allowlisted_fields(self):
        for field,value in [('rating','up'),('rating','down'),('comment','Useful.\nShow more code.')]:
            status,logged=self.submit({'job_id':'a'*32,field:value}, True)
            self.assertEqual(status,200)
            record=json.loads(logged)
            self.assertEqual(set(record),{'event','job_id','submitted_at',field})
            self.assertEqual(record[field],value)
            self.assertEqual(len(logged.splitlines()),1)
        condition=self.db.update_item.call_args.kwargs['ConditionExpression']
        self.assertIn('attribute_not_exists',condition)
        self.assertIn('#ttl > :now',condition)

    def test_invalid_payloads_never_write_or_log(self):
        for payload in [[], {'job_id':'bad','rating':'up'}, {'job_id':'a'*32,'rating':'yes'},
                        {'job_id':'a'*32,'comment':' '}, {'job_id':'a'*32,'comment':'x'*2001},
                        {'job_id':'a'*32,'rating':'up','comment':'both'},
                        {'job_id':'a'*32,'comment':'ok','idea':'private'}]:
            self.assertEqual(self.submit(payload),(400,''))
        self.db.update_item.assert_not_called()

    def test_missing_running_expired_jobs_rejected(self):
        for job in [{}, app.item(status='running',ttl=int(time.time())+100), app.item(status='complete',ttl=1)]:
            self.db.get_item.return_value={'Item':job}
            self.assertEqual(self.submit({'job_id':'a'*32,'rating':'up'}),(404,''))
        self.db.update_item.assert_not_called()

    def test_retry_is_idempotent_and_changed_vote_rejected(self):
        self.db.update_item.side_effect=Conditional()
        self.db.get_item.return_value={'Item':app.item(status='complete',ttl=int(time.time())+500,feedback_rating='up')}
        self.assertEqual(self.submit({'job_id':'a'*32,'rating':'up'}),(200,''))
        self.assertEqual(self.submit({'job_id':'a'*32,'rating':'down'}),(409,''))

    def test_db_failure_does_not_log_success(self):
        self.db.update_item.side_effect=RuntimeError('private detail')
        self.assertEqual(self.submit({'job_id':'a'*32,'rating':'up'}),(503,''))

    def test_route_and_retention(self):
        resources=template()['Resources']
        self.assertEqual(resources['FeedbackRoute']['Properties']['RouteKey'],'POST /api/feedback')
        self.assertEqual(resources['ApiLogs']['Properties']['RetentionInDays'],30)

if __name__=='__main__': unittest.main()
