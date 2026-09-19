"""Checks for attribution, response validation, and safe cache invalidation."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('jev_triage', Path(__file__).resolve().parents[1] / 'scripts/jev_triage.py')
triage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(triage)


class TriageTests(unittest.TestCase):
    def test_quoted_project_does_not_become_reply_body(self):
        raw = '@builder\nI built an agent\nreader\n — \n10:08\nSaturday, 19 September 2026 at 10:08\nvery cool!\n1\nAdd Reaction'
        body, quote, status = triage.normalize_text(raw)
        self.assertNotIn('built an agent', body)
        self.assertIn('built an agent', quote)
        self.assertIn('very cool!', body)
        self.assertEqual(status, 'recognized_header')

    def test_unknown_ui_preserves_text(self):
        raw = 'Unexpected rendering\n0.92\nimportant technical claim'
        self.assertEqual(triage.normalize_text(raw)[0], raw)

    def test_numeric_body_not_deleted_as_reaction(self):
        raw = '[\n10:08\n]\nSaturday, 19 September 2026 at 10:08\n0.92\n1\nAdd Reaction'
        self.assertEqual(triage.normalize_text(raw)[0], '0.92\n1')

    def test_cache_invalidated_when_context_or_rubric_changes(self):
        a = {'state': {'context': 'old'}, 'questions': triage.questions('123')}
        b = {'state': {'context': 'correction'}, 'questions': triage.questions('123')}
        self.assertNotEqual(triage.cache_key(a), triage.cache_key(b))

    def test_rejects_missing_and_nonfinite_answers(self):
        payload = {'questions': {'x': {'type': 'noul'}}}
        result = {'model': 'jev-1.13.0', 'answers': {}, 'usage': {'input_tokens': 4, 'output_tokens': 2}}
        with self.assertRaises(ValueError):
            triage.validate(payload, result)
        result['answers'] = {'x': {'type': 'noul', 'noul': float('nan')}}
        with self.assertRaises(ValueError):
            triage.validate(payload, result)
        result['answers']['x']['noul'] = 0.5
        triage.validate(payload, result)

    def test_choice_order_invalidates_cache(self):
        first = {'questions': {'x': {'criteria': {'yes': 'Yes', 'no': 'No'}}}}
        reversed_order = {'questions': {'x': {'criteria': {'no': 'No', 'yes': 'Yes'}}}}
        self.assertNotEqual(triage.cache_key(first), triage.cache_key(reversed_order))

    def test_rejects_unknown_choice(self):
        payload = {'questions': {'x': {'type': 'choice', 'criteria': {'a': 'a', 'b': 'b'}}}}
        result = {'model': 'jev-1.13.0', 'answers': {'x': {'type': 'choice', 'choice': 'invented', 'probabilities': {'a': .5, 'b': .5}, 'confidence': .5}}, 'usage': {'input_tokens': 4, 'output_tokens': 2}}
        with self.assertRaises(ValueError):
            triage.validate(payload, result)

    @unittest.skipUnless((triage.SOURCES / "collection-checkpoint.json").exists(), "Private archive not distributed")
    def test_archive_no_silent_loss_or_oversized_payload(self):
        rows = triage.corpus()
        expected = {r['message_id'] for r in rows}
        seen = []
        for group, payload in triage.batches(rows):
            self.assertLessEqual(len(triage.json.dumps(payload, ensure_ascii=False).encode()), 55000)
            for row in group:
                seen.append(row['message_id'])
                self.assertIn(row['message_id'] + '_kind', payload['questions'])
        self.assertEqual(set(seen), expected)
        self.assertEqual(len(seen), len(expected))


if __name__ == '__main__':
    unittest.main()
