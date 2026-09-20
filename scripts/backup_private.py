"""Create and verify an encrypted, versioned private S3 research snapshot.

Uses AWS CLI and credentials from .env.local without logging secret values.
All deployment metadata and bundles remain in ignored research/storage/.
No bucket is made public, no files are deleted, and no automatic schedule is set.
"""
import argparse
import base64
import hashlib
import io
import json
import os
import re
import subprocess
import tarfile
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STORAGE = ROOT / 'research/storage'
INPUTS = ('resource-pool', 'research', 'jev-knowledge-reference.md', 'RESUME.md',
          'scripts', 'tests', 'web', 'docs', 'README.md', 'AGENTS.md', '.gitignore')
BLOCKED_PARTS = {'.git', '.venv', 'node_modules', '__pycache__', '.codex', '.agents'}


def load_env(path):
    values = {}
    if not path.exists():
        return values
    for line in path.read_text().splitlines():
        key, separator, value = line.strip().removeprefix('export ').partition('=')
        if separator and key and not key.startswith('#'):
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            values[key.strip()] = value
    return values


def eligible(path):
    relative = path.relative_to(ROOT)
    return (not path.is_symlink() and not set(relative.parts) & BLOCKED_PARTS
            and not any((ROOT / parent / 'pyvenv.cfg').is_file()
                        for parent in relative.parents if parent != Path('.'))
            and relative.parts[:2] != ('research', 'storage')
            and not path.name.startswith('.env')
            and path.suffix.lower() not in ('.pem', '.key', '.p12', '.pfx', '.pyc')
            and path.name not in ('run.lock', '.DS_Store'))


def package():
    STORAGE.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid.uuid4().hex[:8]
    directory = STORAGE / stamp
    directory.mkdir()
    secrets = [value.encode() for value in load_env(ROOT / '.env.local').values() if len(value) >= 8]
    files = []
    for name in INPUTS:
        source = ROOT / name
        for path in sorted(source.rglob('*')) if source.is_dir() else [source]:
            if path.is_file() and eligible(path):
                files.append(path)
    manifest = {'format': 1, 'created_at': datetime.now(timezone.utc).isoformat(),
                'contains_private_evidence': True, 'credentials_included': False,
                'files': []}
    archive = directory / 'evidence.tar.gz'
    try:
        with tarfile.open(archive, 'w:gz') as bundle:
            for path in files:
                data = path.read_bytes()
                if any(secret in data for secret in secrets):
                    raise ValueError(f'Credential value found in backup input: {path.relative_to(ROOT)}')
                if re.search(rb'(?:AKIA|ASIA)[A-Z0-9]{16}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----', data):
                    raise ValueError(f'Credential-like material found in backup input: {path.relative_to(ROOT)}')
                name = path.relative_to(ROOT).as_posix()
                info = tarfile.TarInfo(name)
                info.size = len(data)
                info.mode = 0o600
                bundle.addfile(info, io.BytesIO(data))
                manifest['files'].append({'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
        manifest['archive_sha256'] = hashlib.sha256(archive.read_bytes()).hexdigest()
        manifest['archive_bytes'] = archive.stat().st_size
        (directory / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    except Exception:
        archive.unlink(missing_ok=True)
        raise
    return directory, manifest


class AWS:
    def __init__(self, region):
        self.env = os.environ.copy()
        self.env.update({key: value for key, value in load_env(ROOT / '.env.local').items() if key.startswith('AWS_')})
        self.env.update(AWS_PAGER='', AWS_MAX_ATTEMPTS='2')
        self.region = region

    def call(self, service, action, *args):
        command = ['aws', service, action, '--region', self.region, '--output', 'json',
                   '--cli-connect-timeout', '10', '--cli-read-timeout', '60', *args]
        result = subprocess.run(command, env=self.env, capture_output=True, text=True)
        if result.returncode:
            error = result.stderr
            for value in load_env(ROOT / '.env.local').values():
                if len(value) >= 8:
                    error = error.replace(value, '[REDACTED]')
            raise RuntimeError(f'{service} {action}: {error[:1200]}')
        return json.loads(result.stdout) if result.stdout.strip() else {}


def backup(region):
    aws = AWS(region)
    identity = aws.call('sts', 'get-caller-identity')
    owner = identity['Account']
    STORAGE.mkdir(parents=True, exist_ok=True)
    config_path = STORAGE / 's3-config.json'
    if config_path.exists():
        config = json.loads(config_path.read_text())
        if config['account_id'] != owner or config['region'] != region:
            raise ValueError('Existing backup configuration belongs to another account or region')
    else:
        config = {'bucket': 'jev-bot-private-' + uuid.uuid4().hex[:20], 'account_id': owner,
                  'region': region, 'created': False}
        config_path.write_text(json.dumps(config, indent=2) + '\n')
    bucket = config['bucket']
    if not config['created']:
        options = ['--bucket', bucket, '--object-ownership', 'BucketOwnerEnforced']
        if region != 'us-east-1':
            options += ['--create-bucket-configuration', json.dumps({'LocationConstraint': region})]
        try:
            aws.call('s3api', 'create-bucket', *options)
        except RuntimeError as error:
            if 'BucketAlreadyOwnedByYou' not in str(error):
                raise
        config['created'] = True
        config_path.write_text(json.dumps(config, indent=2) + '\n')
    common = ['--bucket', bucket, '--expected-bucket-owner', owner]
    public_block = dict(BlockPublicAcls=True, IgnorePublicAcls=True, BlockPublicPolicy=True, RestrictPublicBuckets=True)
    aws.call('s3api', 'put-public-access-block', *common, '--public-access-block-configuration', json.dumps(public_block))
    aws.call('s3api', 'put-bucket-ownership-controls', *common, '--ownership-controls', json.dumps({'Rules': [{'ObjectOwnership': 'BucketOwnerEnforced'}]}))
    aws.call('s3api', 'put-bucket-encryption', *common, '--server-side-encryption-configuration', json.dumps({'Rules': [{'ApplyServerSideEncryptionByDefault': {'SSEAlgorithm': 'AES256'}}]}))
    aws.call('s3api', 'put-bucket-versioning', *common, '--versioning-configuration', 'Status=Enabled')
    policy = {'Version': '2012-10-17', 'Statement': [{'Sid': 'DenyInsecureTransport', 'Effect': 'Deny', 'Principal': '*', 'Action': 's3:*', 'Resource': [f'arn:aws:s3:::{bucket}', f'arn:aws:s3:::{bucket}/*'], 'Condition': {'Bool': {'aws:SecureTransport': 'false'}}}]}
    aws.call('s3api', 'put-bucket-policy', *common, '--policy', json.dumps(policy))
    checks = {
        'public_access': aws.call('s3api', 'get-public-access-block', *common),
        'ownership': aws.call('s3api', 'get-bucket-ownership-controls', *common),
        'encryption': aws.call('s3api', 'get-bucket-encryption', *common),
        'versioning': aws.call('s3api', 'get-bucket-versioning', *common),
        'policy_status': aws.call('s3api', 'get-bucket-policy-status', *common),
    }
    assert checks['public_access']['PublicAccessBlockConfiguration'] == public_block
    assert checks['ownership']['OwnershipControls']['Rules'][0]['ObjectOwnership'] == 'BucketOwnerEnforced'
    assert checks['encryption']['ServerSideEncryptionConfiguration']['Rules'][0]['ApplyServerSideEncryptionByDefault']['SSEAlgorithm'] == 'AES256'
    assert checks['versioning']['Status'] == 'Enabled'
    assert checks['policy_status']['PolicyStatus']['IsPublic'] is False
    directory, manifest = package()
    prefix = f'snapshots/{directory.name}'
    objects = []
    for name in ('evidence.tar.gz', 'manifest.json'):
        path = directory / name
        digest = base64.b64encode(hashlib.sha256(path.read_bytes()).digest()).decode()
        key = f'{prefix}/{name}'
        uploaded = aws.call('s3api', 'put-object', *common, '--key', key, '--body', str(path), '--server-side-encryption', 'AES256', '--checksum-algorithm', 'SHA256', '--checksum-sha256', digest)
        head = aws.call('s3api', 'head-object', *common, '--key', key, '--version-id', uploaded['VersionId'], '--checksum-mode', 'ENABLED')
        assert head['ContentLength'] == path.stat().st_size and head['ChecksumSHA256'] == digest
        assert head['ServerSideEncryption'] == 'AES256'
        objects.append({'key': key, 'version_id': uploaded['VersionId'], 'sha256_base64': digest, 'bytes': path.stat().st_size})
    restored = directory / 'verified-download.tar.gz'
    aws.call('s3api', 'get-object', *common, '--key', objects[0]['key'], '--version-id', objects[0]['version_id'], str(restored))
    assert hashlib.sha256(restored.read_bytes()).hexdigest() == manifest['archive_sha256']
    with tarfile.open(restored, 'r:gz') as bundle:
        expected = {row['path']: row for row in manifest['files']}
        assert set(bundle.getnames()) == set(expected)
        for member in bundle:
            assert member.isfile() and not member.name.startswith('/') and '..' not in Path(member.name).parts
            assert hashlib.sha256(bundle.extractfile(member).read()).hexdigest() == expected[member.name]['sha256']
    receipt = {'bucket': bucket, 'region': region, 'prefix': prefix, 'objects': objects,
               'files': len(manifest['files']), 'uncompressed_bytes': sum(row['bytes'] for row in manifest['files']),
               'checks': checks, 'download_and_file_hashes_verified': True,
               'completed_at': datetime.now(timezone.utc).isoformat()}
    (directory / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    (STORAGE / 'latest-backup.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({key: receipt[key] for key in ('bucket', 'region', 'prefix', 'files', 'uncompressed_bytes', 'download_and_file_hashes_verified')}, indent=2))


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('command', choices=['prepare', 'backup'])
    parser.add_argument('--region', default='us-east-1')
    args = parser.parse_args()
    if args.command == 'backup':
        backup(args.region)
    else:
        directory, manifest = package()
        print(json.dumps({'bundle': str(directory), 'files': len(manifest['files']), 'archive_bytes': manifest['archive_bytes'], 'credentials_included': False}))


if __name__ == '__main__':
    main()
