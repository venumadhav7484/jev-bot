"""Stateful atomic-store model: capacity, quota, expiry and ownership boundaries."""
import copy
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import sys
import threading
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import cloud_bot as app

class Conditional(Exception): pass
class Transaction(Exception): pass
class Store:
    exceptions=SimpleNamespace(ConditionalCheckFailedException=Conditional,TransactionCanceledException=Transaction)
    def __init__(self): self.rows={};self.mutex=threading.Lock()
    def get_item(self,**kw):
        with self.mutex:return {'Item':copy.deepcopy(self.rows.get(kw['Key']['pk']['S'],{}))}
    def transact_write_items(self,ClientRequestToken,TransactItems):
        assert len(ClientRequestToken)<=36
        put,quota,job=TransactItems[0]['Put'],TransactItems[1]['Update'],TransactItems[2]['Put']
        slot=put['Item']['pk']['S'];day=quota['Key']['pk']['S'];identifier=job['Item']['pk']['S']
        now=int(put['ExpressionAttributeValues'][':now']['N']);limit=int(quota['ExpressionAttributeValues'][':limit']['N'])
        with self.mutex:
            used=int(self.rows.get(day,{}).get('used',{}).get('N','0'))
            if int(self.rows.get(slot,{}).get('lease',{}).get('N','0'))>=now or used>=limit or identifier in self.rows: raise Transaction()
            self.rows[slot]=copy.deepcopy(put['Item']);self.rows[day]=app.item(used=used+1);self.rows[identifier]=copy.deepcopy(job['Item'])
    def delete_item(self,**kw):
        key=kw['Key']['pk']['S'];owner=kw['ExpressionAttributeValues'][':id']['S']
        with self.mutex:
            if self.rows.get(key,{}).get('owner',{}).get('S')!=owner:raise Conditional()
            del self.rows[key]

class Capacity(unittest.TestCase):
    def setUp(self):
        self.env=patch.dict(os.environ,{'DAILY_LIMIT':'5000','MAX_CONCURRENT':'10','TABLE':'test'});self.env.start();self.addCleanup(self.env.stop)
        self.db=Store();self.now=1700000000;self.day='day#'+time.strftime('%Y-%m-%d',time.gmtime(self.now))
    def claim(self,i): return app.claim_job(self.db,'test',f'{i:032x}',self.now)
    def test_ten_parallel_slots_eleventh_busy_no_quota_charge(self):
        with ThreadPoolExecutor(max_workers=20) as pool: results=list(pool.map(self.claim,range(20)))
        accepted=[slot for slot,error in results if error is None]
        self.assertEqual(len(accepted),10);self.assertEqual(len(set(accepted)),10)
        self.assertEqual(int(self.db.rows[self.day]['used']['N']),10)
        self.assertTrue(all(json.loads(error['body'])['code']=='busy' for slot,error in results if error))
    def test_last_daily_answer_claimed_once_under_contention(self):
        self.db.rows[self.day]=app.item(used=4999)
        with ThreadPoolExecutor(max_workers=5) as pool: results=list(pool.map(self.claim,range(5)))
        self.assertEqual(sum(error is None for slot,error in results),1)
        self.assertEqual(int(self.db.rows[self.day]['used']['N']),5000)
        self.assertTrue(all(json.loads(error['body'])['code']=='daily_limit' for slot,error in results if error))
    def test_expired_slot_reused_and_old_owner_cannot_release_it(self):
        self.db.rows['lock']=app.item(owner='old',lease=self.now-1)
        slot,error=self.claim(42);self.assertIsNone(error);self.assertEqual(slot,'lock')
        app.release(self.db,'old',slot);self.assertEqual(self.db.rows[slot]['owner']['S'],f'{42:032x}')
        app.release(self.db,f'{42:032x}',slot);self.assertNotIn(slot,self.db.rows)
    def test_next_utc_day_has_fresh_quota(self):
        self.db.rows[self.day]=app.item(used=5000)
        slot,error=app.claim_job(self.db,'test','b'*32,(self.now//86400+1)*86400)
        self.assertIsNone(error)
