import hashlib
import importlib.util
import json
import tarfile
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('backup_private', Path(__file__).resolve().parents[1] / 'scripts/backup_private.py')
backup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(backup)


class BackupBoundaries(unittest.TestCase):
    def test_archive_excludes_secrets_symlinks_and_prior_backups(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root/'research/storage').mkdir(parents=True)
            (root/'research/body.md').write_text('Private evidence, safe to back up.')
            (root/'research/.env.local').write_text('secret')
            (root/'research/key.pem').write_text('secret')
            (root/'research/storage/old.tar.gz').write_text('old backup')
            (root/'research/link').symlink_to(root/'research/body.md')
            environment = root/'research/media-tools-venv'
            (environment/'lib').mkdir(parents=True)
            (environment/'pyvenv.cfg').write_text('home = /usr/bin')
            (environment/'lib/installed.py').write_text('never-upload-this-secret')
            (root/'.env.local').write_text('AWS_SECRET_ACCESS_KEY=never-upload-this-secret')
            with patch.object(backup, 'ROOT', root), patch.object(backup, 'STORAGE', root/'research/storage'), patch.object(backup, 'INPUTS', ('research',)):
                path, manifest = backup.package()
            self.assertEqual([f['path'] for f in manifest['files']], ['research/body.md'])
            with tarfile.open(path/'evidence.tar.gz') as bundle:
                self.assertEqual(bundle.getnames(), ['research/body.md'])
                self.assertEqual(hashlib.sha256(bundle.extractfile('research/body.md').read()).hexdigest(), manifest['files'][0]['sha256'])

    def test_secret_in_evidence_blocks_package(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root/'research').mkdir()
            (root/'.env.local').write_text('jev_api_key=private-credential-value')
            (root/'research/leak.txt').write_text('accidentally logged private-credential-value')
            with patch.object(backup, 'ROOT', root), patch.object(backup, 'STORAGE', root/'research/storage'), patch.object(backup, 'INPUTS', ('research',)):
                with self.assertRaisesRegex(ValueError, 'Credential value found'):
                    backup.package()
            self.assertFalse(list((root/'research/storage').rglob('*.tar.gz')))


if __name__ == '__main__':
    unittest.main()
