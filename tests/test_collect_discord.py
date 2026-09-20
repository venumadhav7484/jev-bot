"""Collector boundaries: no live Discord or model requests."""
import datetime as dt
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace as NS
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import collect_discord as collector
import jev_triage as triage
from stage_capture import fingerprint

NOW = dt.datetime(2026, 1, 2, tzinfo=dt.timezone.utc)


def message(mid, content='Original body'):
    return NS(id=mid, content=content, channel=NS(id=22), author=NS(id=33),
              created_at=NOW-dt.timedelta(seconds=1), edited_at=None,
              attachments=[], embeds=[], reference=None, type=NS(value=0))


class History:
    def __init__(self, messages):
        self.messages = messages
        self.calls = []

    async def history(self, **kwargs):
        self.calls.append(kwargs)
        for msg in self.messages:
            yield msg


class CollectorTests(unittest.IsolatedAsyncioTestCase):
    async def test_limit_signals_pending_rows_without_advancing_past_them(self):
        channel = History([message(i) for i in range(101, 105)])
        saved = []
        result = await collector.capture_history(channel, '100', NOW, 3, NS, saved.append)
        self.assertEqual(result, {'count': 3, 'complete': False, 'high_water': '103'})
        self.assertEqual(len(saved), 3)
        self.assertEqual(channel.calls[0]['limit'], 4)
        self.assertTrue(channel.calls[0]['oldest_first'])
        self.assertEqual(channel.calls[0]['before'], NOW)

    async def test_all_and_empty_history(self):
        saved = []
        result = await collector.capture_history(History([message(101)]), '100', NOW, 0, NS, saved.append)
        self.assertTrue(result['complete'])
        result = await collector.capture_history(History([]), '100', NOW, 0, NS, saved.append)
        self.assertEqual(result['high_water'], '100')
        self.assertTrue(result['complete'])

    async def test_out_of_interval_fails_before_saving(self):
        for msg in [message(100), NS(**{**vars(message(101)), 'created_at': NOW})]:
            saved = []
            with self.assertRaises(ValueError):
                await collector.capture_history(History([msg]), '100', NOW, 0, NS, saved.append)
            self.assertEqual(saved, [])

    def test_reply_attachment_and_embed_preservation(self):
        msg = message(101, 'Read https://example.com/project')
        msg.attachments = [NS(to_dict=lambda: {'url': 'https://example.com/file', 'filename': 'diagram.png'})]
        msg.embeds = [NS(to_dict=lambda: {'url': 'https://example.com/article', 'description': 'Preview'})]
        msg.reference = NS(resolved=NS(content='Earlier author claim'), to_dict=lambda: {'message_id': '99'})
        row = collector.serialize(msg)
        self.assertEqual(row['text'], msg.content)
        self.assertEqual(row['reply_context'], 'Earlier author claim')
        self.assertEqual(len(row['links']), 3)
        self.assertEqual(row['api_metadata']['reference']['message_id'], '99')
        changed = {**row, 'api_metadata': {**row['api_metadata'], 'embeds': []}}
        self.assertNotEqual(fingerprint(row), fingerprint(changed))

    async def test_missing_message_content_access_stops_before_history(self):
        class Client:
            user = NS(bot=True)

            async def application_info(self):
                return NS(flags=NS(gateway_message_content=False, gateway_message_content_limited=False))
        with self.assertRaisesRegex(ValueError, 'Message Content'):
            await collector.collect(Client(), None, {}, Path('unused'))

    def test_api_corpus_preserves_body_and_reply_context_without_ui_parsing(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            sources = root/'resource-pool/sources'
            sources.mkdir(parents=True)
            (sources/'collection-checkpoint.json').write_text(json.dumps({'guild_id': '11'}))
            (root/'resource-pool/cases.tsv').write_text('id\tmessage_ids\n')
            text = 'Saturday, 19 September 2026 at 10:08\nActual post text'
            row = collector.serialize(message(101, text))
            row['reply_context'] = 'Separate original author'
            capture = root/'capture.json'
            capture.write_text(json.dumps({'guild_id': '11', 'messages': [row]}))
            with patch.object(triage, 'ROOT', root), patch.object(triage, 'SOURCES', sources):
                rows = triage.corpus([capture])
                self.assertEqual(rows[0]['body'], text)
                self.assertEqual(rows[0]['quote_context'], 'Separate original author')
                row.update(format='discord_browser', body='Target body only',
                           text='Quoted author claim\nTarget body only\nPreview and controls')
                capture.write_text(json.dumps({'guild_id': '11', 'messages': [row]}))
                rows = triage.corpus([capture])
                self.assertEqual(rows[0]['body'], 'Target body only')
                self.assertEqual(rows[0]['quote_context'], 'Separate original author')
                capture.write_text(json.dumps({'guild_id': 'wrong', 'messages': [row]}))
                with self.assertRaises(ValueError):
                    triage.corpus([capture])


if __name__ == '__main__':
    unittest.main()
