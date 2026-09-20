"""Load the entire exported research library, locally or from a verified S3 snapshot.

No category filtering, silent truncation, archive extraction, or raw-media claims.
S3 identifiers and receipts stay in ignored local storage.
"""
import base64
import hashlib
import json
from pathlib import Path, PurePosixPath
import tarfile
import tempfile
import threading

from backup_private import AWS, ROOT

SCOPE = ('All exported research Markdown, including every case, master guide, '
         'knowledge reference, findings, lessons and review gaps. Raw messages, '
         'unprocessed media, binary files, code and credentials are not model context.')
_cache = {}
_lock = threading.Lock()


def digest_file(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').digest()


def document(path, body):
    return {'path': path, 'title': next((line.lstrip('# ').strip() for line in body.splitlines()
                                       if line.startswith('# ')), path),
            'body': body, 'sha256': hashlib.sha256(body.encode()).hexdigest()}


def assemble(documents, source, snapshot=None, metadata=None):
    documents = sorted(documents, key=lambda d: d['path'])
    if not documents:
        raise ValueError('Research library is empty.')
    metadata = metadata or {}
    for doc in documents:
        policy = metadata.get(doc['path'], {})
        is_case = doc['path'].startswith('docs/use-cases/')
        doc['evidence_role'] = policy.get('evidence_role', 'unclassified_case' if is_case else 'reviewed_youtube_transcript' if doc['path'].startswith('docs/youtube/') else 'research_guide')
        doc['default_retrieval'] = policy.get('default_retrieval', not is_case)
    fingerprint = hashlib.sha256(json.dumps([(d['path'], d['sha256'], d['evidence_role'], d['default_retrieval']) for d in documents]).encode()).hexdigest()
    return {'documents': documents, 'source': source, 'snapshot': snapshot or fingerprint,
            'fingerprint': fingerprint, 'scope': SCOPE,
            'document_count': len(documents),
            'case_count': sum(d['path'].startswith('docs/use-cases/') for d in documents)}


def from_archive(archive, source, snapshot):
    """Read regular public Markdown members only; never extract paths to disk."""
    documents = []
    metadata = {}
    seen = set()
    with tarfile.open(archive, 'r:gz') as bundle:
        for member in bundle:
            path = PurePosixPath(member.name)
            if path.is_absolute() or '..' in path.parts:
                raise ValueError('Invalid research archive path.')
            if member.name == 'docs/bot-cases.json' and member.isfile():
                metadata = {r['path']: r for r in json.load(bundle.extractfile(member))}
                continue
            if not path.parts or path.parts[0] != 'docs' or path.suffix != '.md':
                continue
            if not member.isfile() or member.name in seen:
                raise ValueError('Invalid or duplicate research document in archive.')
            seen.add(member.name)
            documents.append(document(member.name, bundle.extractfile(member).read().decode('utf-8')))
    return assemble(documents, source, snapshot, metadata)


def load(source='local', root=ROOT):
    if source == 'local':
        docs = []
        for path in sorted((root/'docs').rglob('*.md')):
            if path.is_symlink() or not path.resolve().is_relative_to((root/'docs').resolve()):
                raise ValueError('Research document points outside the exported library.')
            docs.append(document(path.relative_to(root).as_posix(), path.read_text()))
        records = root/'docs/bot-cases.json'
        metadata = {r['path']: r for r in json.loads(records.read_text())} if records.exists() else {}
        return assemble(docs, 'local', metadata=metadata)
    if source != 's3':
        raise ValueError('Choose local or s3 research.')
    storage = root/'research/storage'
    try:
        receipt = json.loads((storage/'latest-backup.json').read_text())
        config = json.loads((storage/'s3-config.json').read_text())
        obj = next(o for o in receipt['objects'] if o['key'].endswith('/evidence.tar.gz'))
        expected = base64.b64decode(obj['sha256_base64'], validate=True)
        object_path = PurePosixPath(obj['key'])
        assert not object_path.is_absolute() and '..' not in object_path.parts
        assert len(object_path.parts) == 3 and object_path.parts[0] == 'snapshots'
        assert receipt['download_and_file_hashes_verified'] is True
        assert receipt['bucket'] == config['bucket'] and receipt['region'] == config['region']
        assert len(expected) == 32 and obj['version_id']
    except (OSError, ValueError, KeyError, StopIteration, AssertionError):
        raise ValueError('S3 research needs a verified backup receipt and matching local configuration.') from None
    # Cache only a checksum-verified immutable object version. Never switch to local
    # research silently when the selected S3 snapshot cannot be loaded.
    cache_key = (str(root), expected.hex(), obj['version_id'])
    with _lock:
        if cache_key in _cache:
            return _cache[cache_key]
        name = PurePosixPath(obj['key']).parent.name
        candidates = [storage/name/'verified-download.tar.gz', storage/name/'evidence.tar.gz']
        archive = next((p for p in candidates if p.is_file() and digest_file(p) == expected), None)
        if archive is None:
            directory = storage/'knowledge-cache'
            directory.mkdir(parents=True, exist_ok=True)
            archive = directory/(expected.hex()+'.tar.gz')
            if not archive.exists() or digest_file(archive) != expected:
                aws = AWS(config['region'])
                with tempfile.NamedTemporaryFile(dir=directory, delete=False) as handle:
                    temporary = Path(handle.name)
                try:
                    aws.call('s3api', 'get-object', '--bucket', config['bucket'],
                             '--expected-bucket-owner', config['account_id'], '--key', obj['key'],
                             '--version-id', obj['version_id'], str(temporary))
                    if digest_file(temporary) != expected:
                        raise ValueError('S3 research download checksum mismatch.')
                    temporary.replace(archive)
                finally:
                    temporary.unlink(missing_ok=True)
        corpus = from_archive(archive, 's3', receipt['completed_at'])
        corpus['cache_note'] = 'Verified local cache of the selected immutable S3 backup version.'
        _cache[cache_key] = corpus
        return corpus


def passages(corpus, max_chars=3600):
    """Lossless bounded passages. Every character is included; offsets are auditable."""
    result = []
    for doc in corpus['documents']:
        start = 0
        while start < len(doc['body']):
            end = min(start+max_chars, len(doc['body']))
            if end < len(doc['body']):
                boundary = doc['body'].rfind('\n', start+max_chars//2, end)
                if boundary >= 0:
                    end = boundary+1
            result.append({'id': f'p{len(result)+1}', 'path': doc['path'], 'title': doc['title'],
                           'start': start, 'end': end, 'text': doc['body'][start:end],
                           'evidence_role': doc['evidence_role'], 'default_retrieval': doc['default_retrieval']})
            start = end
    return result
