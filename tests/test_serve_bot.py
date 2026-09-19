from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
import json
from pathlib import Path
import sys
import threading
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import serve_bot


class LocalServerBoundaries(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), serve_bot.Handler)
        cls.worker = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.worker.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown(); cls.server.server_close(); cls.worker.join()

    def request(self, method, path, body=None, headers=None):
        conn = HTTPConnection('127.0.0.1', self.server.server_port, timeout=5)
        conn.request(method, path, body, headers or {})
        response = conn.getresponse(); data = response.read(); status = response.status
        conn.close(); return status, data

    def test_private_paths_and_traversal_are_not_served(self):
        for path in ('/.env.local', '/research/evidence.sqlite3', '/docs/%2e%2e/.env.local'):
            self.assertEqual(self.request('GET', path)[0], 404)

    def test_explorer_module_and_public_catalog_are_served(self):
        code, module = self.request('GET', '/evidence.mjs')
        self.assertEqual(code, 200)
        self.assertIn(b'export function prepare', module)
        code, catalog = self.request('GET', '/docs/bot-cases.json')
        self.assertEqual(code, 200)
        self.assertTrue(json.loads(catalog))

    def test_untrusted_origin_and_host_are_rejected(self):
        self.assertEqual(self.request('GET', '/', headers={'Host': 'attacker.example'})[0], 403)
        self.assertEqual(self.request('POST', '/api/answer', '{}', {'Origin': 'https://attacker.example', 'Content-Type': 'application/json'})[0], 403)

    def test_json_contract_and_provider_opt_in(self):
        with patch.object(serve_bot, 'answer', return_value={'fit': 'test'}) as mocked:
            code, data = self.request('POST', '/api/answer', json.dumps({'idea': 'Route email'}), {'Content-Type': 'application/json'})
            self.assertEqual(code, 200); self.assertEqual(json.loads(data)['fit'], 'test')
            mocked.assert_called_once_with('Route email', False)
        self.assertEqual(self.request('POST', '/api/answer', '{}', {'Content-Type': 'text/plain'})[0], 415)


if __name__ == '__main__':
    unittest.main()
