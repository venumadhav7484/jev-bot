import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from public_links import is_discord_url, is_private_artifact, private_artifact_roots


class PrivateProvenance(unittest.TestCase):
    def test_private_branch_protects_repo_and_other_paths(self):
        roots = private_artifact_roots(['https://github.com/example/private/tree/topic/pkg'])
        for url in ('https://github.com/example/private',
                    'https://github.com/EXAMPLE/PRIVATE/pull/42?x=1',
                    'https://raw.githubusercontent.com/example/private/main/README.md',
                    'https://github.com/example/%70rivate/issues'):
            self.assertTrue(is_private_artifact(url, roots), url)
        self.assertFalse(is_private_artifact('https://github.com/example/public', roots))
        self.assertFalse(is_private_artifact('https://github.com/example/private-tools', roots))

    def test_discord_media_and_subdomains_are_private(self):
        for url in ('https://discord.com/channels/1/2',
                    'https://cdn.discordapp.com/attachments/1/2/file.png',
                    'https://media.discordapp.net/attachments/1/2/file.png',
                    'https://discord.gg/example'):
            self.assertTrue(is_discord_url(url), url)
        self.assertFalse(is_discord_url('https://notdiscord.com/docs'))


if __name__ == '__main__':
    unittest.main()
