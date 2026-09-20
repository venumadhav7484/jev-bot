import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from plan_delta_review import source_key, link_kind, plan


class DeltaReviewTests(unittest.TestCase):
    def test_identity_keeps_revision_query_and_fragment(self):
        self.assertNotEqual(source_key('https://example.org/?version=1'), source_key('https://example.org/?version=2'))
        self.assertNotEqual(source_key('https://example.org/#one'), source_key('https://example.org/#two'))
        self.assertEqual(source_key('https://x.com/a/status/123?s=20'), source_key('https://jf.x.com/b/status/123'))
        self.assertIsNone(source_key('https://user:secret@example.org/'))
        self.assertEqual(link_kind('https://github.com/a/repo'), 'source')
        self.assertEqual(link_kind('https://opengraph.githubassets.com/hash/a/repo'), 'media_or_preview')

    def test_reuse_joins_case_messages_without_approving_or_changing_cursor(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); bid = 'a'*64
            sources = root/'resource-pool/sources'; sources.mkdir(parents=True)
            (root/'resource-pool/cases.tsv').write_text('id\ttitle\tmessage_ids\nknown\tExisting case\t100\n')
            (sources/'external-links.json').write_text(json.dumps([{'url':'https://github.com/a/repo', 'message_ids':['100'], 'review_status':'readme_reviewed'}]))
            batch = root/'research/incoming'/bid; (batch/'triage').mkdir(parents=True)
            (batch/'manifest.json').write_text(json.dumps({'batch_id':bid}))
            row = dict(message_id='200', source_url='https://discord.com/channels/1/2/200',
                       content_hash='hash', body='New update https://github.com/a/repo', quote_context='',
                       links=['https://github.com/a/repo', 'https://opengraph.githubassets.com/hash/a/repo'])
            (batch/'triage/messages.jsonl').write_text(json.dumps(row)+'\n')
            (batch/'triage/predictions.jsonl').write_text(json.dumps({'message_id':'200', 'content_hash':'hash', 'priority':1})+'\n')
            summary = plan(root, bid)
            self.assertEqual(summary['messages_with_case_candidates'], 1)
            self.assertEqual(summary['source_groups'], 1)
            self.assertEqual(summary['automatically_approved'], 0)
            self.assertFalse((sources/'collection-checkpoint.json').exists())
            packet = json.loads((batch/'review-plan.json').read_text())['packets'][0]
            self.assertEqual(packet['status'], 'pending_editorial_review')
            row['body'] = 'Unrelated music demo with a quoted project preview'
            (batch/'triage/messages.jsonl').write_text(json.dumps(row)+'\n')
            self.assertEqual(plan(root, bid)['messages_with_case_candidates'], 0)
            (batch/'triage/predictions.jsonl').write_text(json.dumps({'message_id':'200', 'content_hash':'stale', 'priority':1})+'\n')
            with self.assertRaisesRegex(ValueError, 'Stale'):
                plan(root, bid)


if __name__ == '__main__':
    unittest.main()
