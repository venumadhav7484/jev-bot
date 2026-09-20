import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import youtube_sources as youtube
import knowledge_corpus


class YouTubeIntake(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.path = self.root/'input.txt'
        self.path.write_text('0:00\nJev makes a choice.\n0:02\nThe application executes it.\n')
        self.url = 'https://www.youtube.com/watch?v=abcdefghijk'

    def review(self, source):
        return {'source_id': source['source_id'], 'transcript_sha256': source['sha256'],
                'reviewed_by': 'Editor', 'reviewed_on': '2026-09-20', 'full_transcript_read': True,
                'source_alignment': 'not_checked', 'alignment_notes': 'Video not watched.',
                'summary': 'An attributed decision example.', 'gaps': ['No visual review.'],
                'claims': [{'id': 'c1', 'kind': 'capability', 'status': 'author_claim',
                            'summary': 'The speaker describes a bounded decision.', 'jev_role': 'Host executes it.',
                            'limits': 'Not independently reproduced.',
                            'anchor': {'start_line': 2, 'end_line': 2, 'quote': 'Jev makes a choice.'}, 'checks': []}]}

    def test_missing_url_inbox_is_private_and_not_exported(self):
        record = youtube.receive(self.path, 'Title', self.root)
        self.assertEqual(record['status'], 'awaiting_video_url')
        self.assertEqual(youtube.reviewed_exports(self.root), {})
        self.assertEqual(record, youtube.receive(self.path, 'Changed', self.root))

    def test_duplicate_and_edited_transcripts_preserve_revisions(self):
        original = youtube.stage(self.path, self.url, root=self.root)
        repeated = youtube.stage(self.path, 'https://youtu.be/abcdefghijk?t=5', root=self.root)
        self.assertEqual(original, repeated)
        self.path.write_text(self.path.read_text()+'Extra line.\n')
        changed = youtube.stage(self.path, self.url, root=self.root)
        self.assertNotEqual(original['source_id'], changed['source_id'])
        self.assertTrue(youtube.load_source(original['source_id'], self.root)[1].endswith('executes it.\n'))
        self.assertFalse(youtube.reviewed_exports(self.root))

    def test_promoted_summary_includes_limits_not_private_quotes(self):
        source = youtube.stage(self.path, self.url, root=self.root)
        review = self.review(source)
        youtube.promote(source['source_id'], review, self.root)
        page = next(iter(youtube.reviewed_exports(self.root).values()))
        self.assertIn('author_claim', page)
        self.assertIn('Not independently reproduced.', page)
        self.assertNotIn('Jev makes a choice.', page)
        self.assertNotIn('Editor', page)
        doc = knowledge_corpus.document('docs/youtube/youtube-abcdefghijk.md', page)
        lib = knowledge_corpus.assemble([doc], 'local')
        self.assertEqual(lib['documents'][0]['evidence_role'], 'reviewed_youtube_transcript')

    def test_review_gate_rejects_unread_stale_unanchored_and_unsubstantiated_claims(self):
        source = youtube.stage(self.path, self.url, root=self.root)
        review = self.review(source)
        changes = [lambda r: r.update(full_transcript_read=False),
                   lambda r: r.update(transcript_sha256='wrong'),
                   lambda r: r['claims'][0]['anchor'].update(quote='Invented'),
                   lambda r: r['claims'][0].update(status='corroborated'),
                   lambda r: r['claims'][0].update(status='reproduced'),
                   lambda r: r['claims'][0].update(related_case_ids=['../escape'])]
        for change in changes:
            candidate = copy.deepcopy(review); change(candidate)
            with self.assertRaises(ValueError):
                youtube.promote(source['source_id'], candidate, self.root)
        self.assertFalse(youtube.reviewed_exports(self.root))

    def test_changed_original_blocks_reexport(self):
        source = youtube.stage(self.path, self.url, root=self.root)
        youtube.promote(source['source_id'], self.review(source), self.root)
        (youtube.source_directory(source['source_id'], self.root)/'transcript.txt').write_text('tampered')
        with self.assertRaises(ValueError):
            youtube.reviewed_exports(self.root)

    def test_corroboration_needs_inspected_external_evidence(self):
        source = youtube.stage(self.path, self.url, root=self.root)
        review = self.review(source)
        claim = review['claims'][0]; claim['status'] = 'corroborated'
        claim['checks'] = [{'url': 'https://docs.typesafe.ai/primitives', 'checked_on': '2026-09-20',
                            'access': 'inaccessible', 'finding': 'supports', 'notes': 'Could not inspect.'}]
        with self.assertRaises(ValueError):
            youtube.promote(source['source_id'], review, self.root)
        claim['checks'][0].update(access='inspected', notes='Typed Choice contract inspected; no workload reproduction.')
        youtube.promote(source['source_id'], review, self.root)
        self.assertTrue(youtube.reviewed_exports(self.root))

    def test_video_urls_and_source_ids_cannot_escape_storage(self):
        for value in ('https://example.com/watch?v=abcdefghijk', 'https://user:secret@youtube.com/watch?v=abcdefghijk', 'https://youtube.com/watch?v=../escape'):
            with self.assertRaises(ValueError):
                youtube.video_identity(value)
        with self.assertRaises(ValueError):
            youtube.source_directory('../../escape', self.root)


if __name__ == '__main__':
    unittest.main()
