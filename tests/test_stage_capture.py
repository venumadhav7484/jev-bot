import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from stage_capture import stage


class CaptureIntake(unittest.TestCase):
    def test_overlap_edits_and_new_rows_preserve_frozen_cursor(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sources = root/'resource-pool/sources'; sources.mkdir(parents=True)
            old = {'id': 'chat-messages-22-100', 'text': 'original', 'links': []}
            (sources/'main.json').write_text(json.dumps({'messages': [old]}))
            (sources/'thread.json').write_text('{"messages": []}')
            cp = {'guild_id': '11', 'main_channel_id': '22', 'main_snapshot': 'resource-pool/sources/main.json',
                  'thread_snapshot': 'resource-pool/sources/thread.json', 'capture_high_water_message_id': '100'}
            path = sources/'collection-checkpoint.json'; path.write_text(json.dumps(cp)); before = path.read_bytes()
            doc = {'guild_id': '11', 'messages': [old, old, {**old, 'text': 'edited'}, {**old, 'id': 'chat-messages-22-101'}]}
            result = stage(doc, root)
            self.assertEqual(result['counts'], {'unchanged': 1, 'edited': 1, 'new': 1})
            self.assertEqual(result['incoming_main_high_water'], '101')
            self.assertEqual(result, stage(doc, root))
            self.assertEqual(path.read_bytes(), before)
            self.assertEqual(len(list((root/'research/incoming').iterdir())), 1)
            with self.assertRaises(ValueError):
                stage({**doc, 'guild_id': 'wrong'}, root)
            with self.assertRaises(ValueError):
                stage({**doc, 'messages': [{'id': 'bad'}]}, root)


if __name__ == '__main__':
    unittest.main()
