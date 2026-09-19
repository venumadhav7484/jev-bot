import json
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import evidence


class RetrievalPolicy(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.db = Path(self.temp.name) / 'evidence.sqlite3'
        conn = sqlite3.connect(self.db)
        conn.executescript('''
            CREATE TABLE evidence (id TEXT, resource_type TEXT, title TEXT, body TEXT,
                flags TEXT, links TEXT, case_ids TEXT, default_retrieval INTEGER);
            CREATE VIRTUAL TABLE evidence_fts USING fts5(id UNINDEXED, title, body);
        ''')
        for rid, kind, role, default in (
            ('case', 'curated_case', 'reported_application', 1),
            ('failure', 'curated_case', 'counterexample', 0),
            ('proposal', 'curated_case', 'proposal', 0),
            ('raw', 'discord_message', 'unknown', 0),
            ('tool', 'curated_case', 'community_tool', 1),
            ('media', 'media_review', 'observation', 0),
        ):
            body = 'routing ' + 'state ' * 300 + 'LIMIT: accuracy unverified. Source review: timeout fails open.'
            conn.execute('INSERT INTO evidence VALUES (?,?,?,?,?,?,?,?)',
                         (rid, kind, 'routing', body, json.dumps({'evidence_role': role}),
                          '["https://example.com/source"]', '[]', default))
            conn.execute('INSERT INTO evidence_fts VALUES (?,?,?)', (rid, 'routing', body))
        conn.commit()
        conn.close()
        self.mock = patch.object(evidence, 'DB', self.db)
        self.mock.start()
        self.addCleanup(self.mock.stop)

    def test_default_hides_raw_proposals_and_counterexamples(self):
        self.assertEqual({'case', 'tool'}, {r['id'] for r in evidence.search_records('routing')})

    def test_counterevidence_remains_retrievable(self):
        self.assertEqual(['failure'], [r['id'] for r in evidence.search_records('routing', purpose='counterevidence')])

    def test_media_requires_research_and_preserves_partial_boundary(self):
        self.assertEqual([], evidence.search_records('routing', kind='media_review'))
        rows = evidence.search_records('routing', kind='media_review', purpose='research', full=True)
        self.assertEqual(['media'], [r['id'] for r in rows])
        body = evidence.media_context({'attachment_id': 'sample', 'status': 'video_sampled',
                                      'complete': False, 'note': 'Only opening frame inspected.'},
                                     'https://example.com/source')
        self.assertIn('Inspection complete: False', body)
        self.assertIn('not independent implementation validation', body)
        self.assertIn('https://example.com/source', body)
        self.assertIn('Only opening frame inspected.', body)

    def test_full_context_preserves_trailing_limits(self):
        rows = evidence.search_records('routing', full=True)
        self.assertTrue(all('timeout fails open' in r['body'] for r in rows))
        excerpts = evidence.search_records('routing')
        self.assertTrue(all(r['excerpt_is_complete_evidence'] is False for r in excerpts))

    def test_input_cannot_override_retrieval_policy(self):
        rows = evidence.search_records('routing OR raw:* NOT proposal')
        self.assertEqual({'case', 'tool'}, {r['id'] for r in rows})
        with self.assertRaises(ValueError):
            evidence.search_records('routing', purpose='unrestricted')


if __name__ == '__main__':
    unittest.main()
