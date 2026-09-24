"""Whole-flow boundaries: freshness, citations, billing and stale evidence."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import fetch_evidence
import research_flow as flow
import consolidate
from jev_triage import dump


class FlowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        self.row = {'message_id':'123', 'body':'Author reports a small integration experiment.',
                    'quote_context':'', 'source_url':'https://example.org/discovery',
                    'existing_case_candidates':[], 'source_keys':[], 'media_or_preview_urls':[],
                    'jev_suggestion':{'primary_kind':'implementation', 'flags':{'negative_evidence':0.1,'measurement_claim':0.1}}}
        dump(self.work/'manifest.json', {'message_ids':['123'],'total_messages':1})
        dump(self.work/'packets/123.json',self.row)
        dump(self.work/'source-groups.json',[])

    @staticmethod
    def fake_jev(payload):
        answers = {}
        for key,q in payload['questions'].items():
            if q['type'] == 'noul':
                answers[key] = {'type':'noul','noul':.05 if key in ('omitted_caveat','draft_contradiction','material_failure_or_correction') else .95}
            else:
                opts = list(q['criteria']); choice = opts[0]
                answers[key] = {'type':'choice','choice':choice,'confidence':.95,
                                'probabilities':{v:1. if v == choice else 0. for v in opts}}
        return {'model':flow.MODEL,'answers':answers,'usage':{'input_tokens':100,'output_tokens':10}}

    @staticmethod
    def fake_glm(payload):
        data = json.loads(payload['messages'][1]['content'])
        p = data['passages'][0]
        draft = {'source_id':data['source_id'],'text_sha256':data['text_sha256'],
                 'title':'Reported experiment','drafted_by':'GLM 5.3','status':'provisional',
                 'fields':{k:[{'text':'Author reports a small integration experiment.',
                              'kind':'source_claim','citations':[{'passage_id':p['id'],
                              'quote':'Author reports a small integration experiment.'}]}]
                           for k in flow.source_pilot.FIELDS}}
        return {'model':'glm-5.3','choices':[{'finish_reason':'stop','message':{'content':json.dumps(draft)}}],
                'usage':{'prompt_tokens':100,'completion_tokens':40}}

    def test_full_flow_resume_and_new_evidence_invalidates_paid_work(self):
        with patch.object(flow,'glm_call',side_effect=self.fake_glm) as glm, patch.object(flow.source_pilot,'call_once',side_effect=self.fake_jev) as jev:
            result = flow.execute(self.work,['draft','check'],workers=1)
            self.assertEqual(result['queues'],{'routine_provisional':1})
            self.assertEqual(result['editorial_approvals'],0)
            flow.execute(self.work,['draft','check'],workers=1)
            self.assertEqual(glm.call_count,1);self.assertEqual(jev.call_count,1)
            self.row['body'] += ' The result was later retracted.'
            dump(self.work/'packets/123.json',self.row)
            flow.report(self.work)
            reasons = json.loads((self.work/'report.json').read_text())['entries'][0]['reasons']
            self.assertIn('stale_draft',reasons);self.assertIn('stale_grounding_check',reasons)
            flow.execute(self.work,['draft','check'],workers=1)
            self.assertEqual(glm.call_count,2);self.assertEqual(jev.call_count,2)

    def test_invalid_quote_keeps_usage_and_never_silently_retries(self):
        def invalid(payload):
            response = self.fake_glm(payload)
            draft = json.loads(response['choices'][0]['message']['content'])
            draft['fields']['how'][0]['citations'][0]['quote'] = 'Invented production deployment evidence'
            response['choices'][0]['message']['content'] = json.dumps(draft)
            return response
        with patch.object(flow,'glm_call',side_effect=invalid) as glm:
            result = flow.execute(self.work,['draft','check'],workers=1)
            self.assertEqual(result['failed_or_uncertain_attempts'],1)
            self.assertEqual(result['usage']['glm_input_tokens'],100)
            self.assertFalse((self.work/'draft/123.json').exists())
            flow.execute(self.work,['draft'],workers=1)
            self.assertEqual(glm.call_count,1)

    def test_comparison_enters_writer_context_without_becoming_source_evidence(self):
        self.row['existing_case_candidates'] = [{'id':'old','what':'Earlier experiment'}]
        dump(self.work/'packets/123.json',self.row)
        with patch.object(flow,'glm_call',side_effect=self.fake_glm) as glm, patch.object(flow.source_pilot,'call_once',side_effect=self.fake_jev):
            flow.execute(self.work,['compare','draft'],workers=1)
            supplied = json.loads(glm.call_args.args[0]['messages'][1]['content'])
            self.assertIn('jev_change_suggestion_not_evidence',supplied)

    def test_media_and_failed_fetches_stay_explicit_gaps(self):
        self.row['source_keys'] = ['source']; self.row['media_or_preview_urls'] = ['https://example.org/demo.mp4']
        source = flow.build_source(self.row,{'source':{'urls':['https://example.org/report']}},self.work)
        self.assertEqual({g['reason'] for g in source['gaps']},{'not_fetched','media_or_previews_not_visually_reviewed'})
        self.row['source_keys'] = []
        self.row['required_media_urls'] = []
        source = flow.build_source(self.row,{},self.work)
        self.assertEqual(source['gaps'],[])
        self.assertEqual(len(source['unreviewed_preview_inventory']),1)

    def test_local_repair_never_invents_quotes_and_preserves_supplemental_text(self):
        source = flow.build_source(self.row,{},self.work)
        draft = json.loads(self.fake_glm(flow.draft_payload(source))['choices'][0]['message']['content'])
        draft['fields']['what'][0]['citations'][0]['passage_id'] = 'wrong'
        repaired, changes = flow.repair_draft_text(json.dumps(draft)+'\nExtra caveat',source)
        self.assertEqual(repaired['fields']['what'][0]['citations'][0]['passage_id'],'p001')
        self.assertTrue(any(c.get('text') == 'Extra caveat' for c in changes))
        draft['fields']['what'][0]['citations'][0]['quote'] = 'This never appeared in any supplied source'
        with self.assertRaises(ValueError):
            flow.repair_draft_text(json.dumps(draft),source)
        self.row['body'] = 'Author reports a small\nintegration experiment.'
        source = flow.build_source(self.row,{},self.work)
        draft['text_sha256'] = source['text_sha256']
        draft['fields']['what'][0]['citations'][0]['quote'] = 'Author reports a small integration experiment.'
        repaired, changes = flow.repair_draft_text(json.dumps(draft),source)
        self.assertIn('\n',repaired['fields']['what'][0]['citations'][0]['quote'])

    def test_source_refresh_preserves_old_version_and_detects_change(self):
        def response(text):
            return {'status':'text_fetched','text':text,'links':[],'truncated':False,'final_url':'https://example.org/report'}
        with patch.object(fetch_evidence,'retrieve',side_effect=[response('old'),response('new')]) as retrieve:
            entry = {'url':'https://example.org/report'}
            fetch_evidence.fetch(entry,out=self.work)
            fetch_evidence.fetch(entry,out=self.work)
            self.assertEqual(retrieve.call_count,1)
            fetch_evidence.fetch(entry,refresh=True,out=self.work)
            self.assertEqual(retrieve.call_count,2)
            saved = json.loads((self.work/(flow.hashlib.sha256(entry['url'].encode()).hexdigest()+'.json')).read_text())
            self.assertTrue(saved['changed_since_previous'])
            archived = list((self.work/'versions').rglob('*.json'))
            self.assertEqual(len(archived),1)
            self.assertEqual(json.loads(archived[0].read_text())['text'],'old')

    def test_digest_repair_requires_request_binding_and_valid_quotes(self):
        source = flow.build_source(self.row, {}, self.work)
        draft = json.loads(self.fake_glm(flow.draft_payload(source))['choices'][0]['message']['content'])
        draft['text_sha256'] = 'mistyped-digest'
        with self.assertRaises(ValueError):
            flow.repair_draft_text(json.dumps(draft), source)
        repaired, changes = flow.repair_draft_text(json.dumps(draft), source, request_bound=True)
        self.assertEqual(repaired['text_sha256'], source['text_sha256'])
        self.assertEqual(changes[0]['kind'], 'request_bound_source_digest')
        draft['fields']['what'][0]['citations'][0]['quote'] = 'Invented benchmark result'
        with self.assertRaises(ValueError):
            flow.repair_draft_text(json.dumps(draft), source, request_bound=True)
        draft['source_id'] = 'another-source'
        with self.assertRaises(ValueError):
            flow.repair_draft_text(json.dumps(draft), source, request_bound=True)

    def test_rebuild_status_uses_checkpoint_counts_and_preserves_review_cursor(self):
        pool = self.work/'resource-pool'
        summary = dict(s3_uploaded=False,curated_cases=2,default_retrieval_cases=1,
                       editorial_review={'unassigned_messages':1},external_review_status_counts={'not_reviewed':1,'sections_reviewed':1},
                       external_unresolved_content_status_counts={'not_reviewed':1},
                       external_urls_with_content_gaps=1,external_urls=2,
                       message_coverage_status_counts={'cited_in_case':2,'uncatalogued_source_row':1},
                       unique_messages=3,main_channel_rows=2,thread_rows=1,thread_count=1)
        media = dict(content_review_counts={},attachments_reviewed=0,attachments_pending=0,
                     unique_urls=0,messages=0,entries=[])
        checkpoint = dict(snapshot_date='2027-01-02',capture_high_water_timestamp_utc='2027-01-02T03:04:05+00:00',
                          capture_high_water_message_id='200',capture_high_water_url='https://example.org/200',
                          earliest_captured_message_id='100',review_progress={'fully_reviewed_through_message_id':'150'})
        dump(pool/'coverage-summary.json',summary)
        dump(pool/'sources/media-accounting.json',media)
        dump(pool/'sources/x-review-backlog.json',{'counts':{},'entries':[]})
        dump(pool/'sources/collection-checkpoint.json',checkpoint)
        dump(pool/'sources/external-links.json',[
            {'url':'https://example.org/pending','review_status':'not_reviewed'},
            {'url':'https://example.org/read','review_status':'sections_reviewed'}])
        (self.work/'README.md').write_text('<!-- SNAPSHOT-START --><!-- SNAPSHOT-END -->')
        with patch.object(consolidate,'ROOT',self.work):
            consolidate.write_status()
        text = (pool/'completion-status.md').read_text()
        self.assertIn('02 January 2027',text)
        self.assertIn('3 unique IDs',text)
        self.assertIn('1 uncatalogued',text)
        saved = json.loads((pool/'sources/collection-checkpoint.json').read_text())
        self.assertEqual(saved['review_progress']['fully_reviewed_through_message_id'],'150')
        backlog=json.loads((pool/'sources/remaining-review-backlog.json').read_text())
        self.assertEqual([r['url'] for r in backlog['entries']],['https://example.org/pending'])
        self.assertIn('1 explicit content gaps among 2 URLs',(pool/'review-backlog.md').read_text())


if __name__ == '__main__':
    unittest.main()
