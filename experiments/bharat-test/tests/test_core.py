import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

from common import INDIAN, MOST_SPOKEN, TOPICS, load_split, parse, payload


class DataTests(unittest.TestCase):
    def test_all_sets_parallel_with_204_test_rows(self):
        english = load_split('eng_Latn')
        self.assertEqual(len(english), 204)
        for lang in INDIAN:
            rows = load_split(lang)
            self.assertEqual([r['index_id'] for r in rows], [r['index_id'] for r in english], lang)
            self.assertEqual([r['category'] for r in rows], [r['category'] for r in english], lang)

    def test_language_lists(self):
        self.assertEqual(len(INDIAN), 24)
        self.assertTrue(set(MOST_SPOKEN) <= set(INDIAN))
        self.assertEqual(len(MOST_SPOKEN), 10)


class RequestTests(unittest.TestCase):
    def test_payload_shape(self):
        body = payload('नमस्ते')
        self.assertEqual(body['state'], {'text': 'नमस्ते'})
        self.assertEqual(list(body['questions']['topic']['criteria']), list(TOPICS))

    def test_parse_accepts_valid_and_rejects_invalid(self):
        probs = {k: 1 / 7 for k in TOPICS}
        self.assertEqual(parse({'answers': {'topic': {'choice': 'sports', 'probabilities': probs,
                                                      'confidence': 0.5}}})[0], 'sports')
        with self.assertRaises(ValueError):
            parse({'answers': {'topic': {'choice': 'cricket', 'probabilities': probs}}})
        with self.assertRaises(ValueError):
            parse({'answers': {'topic': {'choice': 'sports', 'probabilities': {'sports': 1.0}}}})


if __name__ == '__main__':
    unittest.main()
