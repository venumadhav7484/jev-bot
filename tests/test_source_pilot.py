"""Evidence versioning, idempotency, billing limits and citation boundaries."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import source_pilot as p


class PilotTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.work = Path(self.tmp.name)
        text = 'This is a reported experiment. Production remains unchanged. '
        self.source = dict(id='a0000000000000000001', url='https://example.org/report', text=text,
                           text_sha256=hashlib.sha256(text.encode()).hexdigest(), passages=p.passages(text))
        p.dump(self.work/'manifest.json', {'source_ids':[self.source['id']]})
        p.dump(self.work/'sources'/f'{self.source["id"]}.json', self.source)
        self.draft = dict(source_id=self.source['id'], text_sha256=self.source['text_sha256'],
                          title='A reported experiment', drafted_by='Test fixture', status='provisional',
                          fields={k:[dict(text='The source describes an experiment.', kind='source_claim',
                            citations=[dict(passage_id='p001',quote='a reported experiment')])] for k in p.FIELDS})
        self.input = self.work/'input.json'
        p.dump(self.input,[self.draft])
        p.import_drafts(self.input,self.work)

    @staticmethod
    def response(payload):
        answers={}
        for k,q in payload['questions'].items():
            if q['type']=='noul': answers[k]={'type':'noul','noul':.9}
            else:
                keys=list(q['criteria']);answers[k]={'type':'choice','choice':keys[0],
                    'probabilities':{x:1. if i==0 else 0. for i,x in enumerate(keys)},'confidence':1.}
        return {'model':p.MODEL,'answers':answers,'usage':{'input_tokens':100,'output_tokens':20}}

    def test_lossless_spans_and_tamper_detection(self):
        text=('line one\nline two\n'*201)+'end'
        self.assertEqual(''.join(x['text'] for x in p.passages(text)),text)
        self.source['passages'][0]['text']='tampered'
        p.dump(self.work/'sources'/f'{self.source["id"]}.json',self.source)
        with self.assertRaises(ValueError):p.load_sources(self.work)

    def test_fabricated_cross_source_and_missing_citations_rejected(self):
        for mutate in (lambda d:d.update(text_sha256='wrong'),
                       lambda d:d['fields']['how'][0]['citations'][0].update(quote='Production was deployed'),
                       lambda d:d['fields']['how'][0].update(citations=[]),
                       lambda d:d.update(status='approved')):
            d=copy.deepcopy(self.draft);mutate(d)
            with self.assertRaises(ValueError):p.validate_draft(d,self.source)

    def test_import_idempotent_and_atomic_validation(self):
        before=list((self.work/'draft-versions').glob('*.json'))
        self.assertEqual(p.import_drafts(self.input,self.work)['unchanged'],1)
        self.assertEqual(list((self.work/'draft-versions').glob('*.json')),before)
        bad=copy.deepcopy(self.draft);bad['source_id']='unknown';p.dump(self.input,[self.draft,bad])
        with self.assertRaises(KeyError):p.import_drafts(self.input,self.work)
        self.assertEqual(list((self.work/'draft-versions').glob('*.json')),before)

    def test_resume_no_charge_and_changed_draft_invalidates_check(self):
        with patch.object(p,'call_once',side_effect=self.response) as api:
            self.assertEqual(p.execute('check',self.work)['new_requests'],1)
            self.assertEqual(p.execute('check',self.work)['cache_hits'],1)
            self.draft['title']='Changed title';p.dump(self.input,[self.draft]);p.import_drafts(self.input,self.work)
            p.report(self.work)
            report=json.loads((self.work/'report.json').read_text())
            self.assertIn('stale_draft_check',report['entries'][0]['review_reasons'])
            p.execute('check',self.work)
            self.assertEqual(api.call_count,2)
            self.assertEqual(p.report(self.work)['editorial_approvals'],0)

    def test_failed_attempt_not_silently_retried_and_budget_prevents_call(self):
        with patch.object(p,'call_once',side_effect=RuntimeError('uncertain')) as api:
            self.assertEqual(p.execute('triage',self.work,max_input_bytes=1)['new_requests'],0)
            p.execute('triage',self.work)
            self.assertEqual(p.execute('triage',self.work)['new_requests'],0)
            self.assertEqual(api.call_count,1)
            self.assertEqual(p.report(self.work)['unresolved_attempts'],1)

if __name__=='__main__':unittest.main()
