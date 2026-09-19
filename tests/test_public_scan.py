from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import check_public


class PublicationGuard(unittest.TestCase):
    def test_blocks_private_paths_credentials_and_source_urls(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(check_public, 'ROOT', Path(directory)), patch.object(check_public, 'load_env', return_value={'jev_api_key': 'synthetic-credential'}):
                findings = check_public.inspect([
                    ('research/raw.json', b'private'), ('.env.local', b'key=value'),
                    ('docs/leak.md', b'synthetic-credential'),
                    ('docs/source.md', b'https://discord.com/channels/example'),
                ])
                reasons = {reason for _, reason in findings}
                self.assertTrue({'private path', 'environment file', 'credential value', 'private provenance URL'} <= reasons)
                self.assertEqual(check_public.inspect([('docs/safe.md', b'Public author report with limits.')]), [])


if __name__ == '__main__':
    unittest.main()
