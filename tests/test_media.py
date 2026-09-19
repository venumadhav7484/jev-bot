import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from audit_media import validate_review_provenance, review_is_complete


class MediaProvenance(unittest.TestCase):
    def test_partial_or_unrecognized_reviews_remain_pending(self):
        self.assertTrue(review_is_complete({'status': 'image_visually_reviewed'}))
        self.assertTrue(review_is_complete({'status': 'video_fully_reviewed', 'complete': True}))
        for review in [None, {'status': 'video_sampled'}, {'status': 'access_failed'},
                       {'status': 'image_visually_reviewed', 'complete': False}]:
            self.assertFalse(review_is_complete(review))

    def test_reply_cannot_inherit_parent_attachment_review(self):
        messages = [
            {'message_id': 'parent', 'attachment_urls': ['https://cdn.discordapp.com/attachments/1/10/image.png']},
            {'message_id': 'reply', 'attachment_urls': ['https://cdn.discordapp.com/attachments/1/11/image.png']},
        ]
        validate_review_provenance(messages, [{'message_id': 'parent', 'attachment_id': '10'}])
        with self.assertRaises(ValueError):
            validate_review_provenance(messages, [{'message_id': 'reply', 'attachment_id': '10'}])


if __name__ == '__main__':
    unittest.main()
