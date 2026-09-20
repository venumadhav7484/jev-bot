"""Stage supplied YouTube transcripts and promote traceable editorial reviews.

Offline only: no fetching, model calls or automatic factual verification. Raw
transcripts and claim anchors remain private; only reviewed summaries export.
"""
import argparse
from datetime import date, datetime, timezone
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[1]
STATUSES = {'author_claim', 'corroborated', 'contradicted', 'unresolved', 'reproduced'}
KINDS = {'capability', 'use_case', 'integration', 'lesson', 'limitation', 'performance', 'pricing'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix+'.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')
    temporary.replace(path)


def required(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(label+' is required.')
    return value.strip()


def public_url(value):
    url = urlsplit(required(value, 'Source URL'))
    if url.scheme != 'https' or not url.hostname or url.username or url.password:
        raise ValueError('Use an HTTPS source URL without credentials.')
    return value


def video_identity(value):
    url = urlsplit(public_url(value))
    host = url.hostname.lower()
    parts = url.path.strip('/').split('/')
    if host == 'youtu.be':
        video = parts[0] if len(parts) == 1 else ''
    elif host in ('youtube.com', 'www.youtube.com', 'm.youtube.com'):
        video = parse_qs(url.query).get('v', [''])[0] if url.path == '/watch' else parts[1] if len(parts) == 2 and parts[0] in ('shorts', 'live', 'embed') else ''
    else:
        video = ''
    if not re.fullmatch(r'[\w-]{11}', video, re.ASCII):
        raise ValueError('Provide a YouTube video URL with an 11-character video ID.')
    return video, 'https://www.youtube.com/watch?v='+video


def source_directory(source_id, root):
    if not re.fullmatch(r'[\w-]{11}-[a-f0-9]{64}', source_id, re.ASCII):
        raise ValueError('Invalid transcript source ID.')
    return root/'research/youtube'/source_id


def receive(path, title='', root=ROOT):
    """Preserve an attachment while its video identity is still missing."""
    raw = path.read_bytes()
    if not raw.decode('utf-8-sig').strip() or len(raw) > 10_000_000:
        raise ValueError('Provide a nonempty UTF-8 transcript smaller than 10 MB.')
    digest = sha(raw)
    directory = root/'research/youtube/inbox'/digest
    receipt = directory/'receipt.json'
    if receipt.exists():
        if sha((directory/'transcript.txt').read_bytes()) != digest:
            raise ValueError('Inbox transcript integrity check failed.')
        return json.loads(receipt.read_text())
    directory.mkdir(parents=True, exist_ok=True)
    (directory/'transcript.txt').write_bytes(raw)
    record = {'sha256': digest, 'title': title, 'status': 'awaiting_video_url',
              'received_at': datetime.now(timezone.utc).isoformat(), 'source_type': 'youtube_transcript',
              'next_step': 'Review supplied text now; stage with the video URL before public promotion.'}
    save(receipt, record)
    return record


def stage(path, url, title='', published=None, transcript_kind='unknown', root=ROOT):
    video, canonical = video_identity(url)
    if published:
        date.fromisoformat(published)
    if transcript_kind not in ('manual', 'auto_captions', 'unknown'):
        raise ValueError('Unknown transcript kind.')
    raw = path.read_bytes()
    text = raw.decode('utf-8-sig')
    if not text.strip() or len(raw) > 10_000_000:
        raise ValueError('Provide a nonempty UTF-8 transcript smaller than 10 MB.')
    digest = sha(raw)
    source_id = video+'-'+digest
    directory = source_directory(source_id, root)
    if (directory/'source.json').exists():
        source, _ = load_source(source_id, root)
        return source  # Identical imports never overwrite review or provenance.
    source = {'schema_version': 1, 'source_id': source_id, 'source_type': 'youtube_transcript',
              'video_id': video, 'url': canonical, 'title': title.strip() or 'YouTube video '+video,
              'published_on': published, 'transcript_kind': transcript_kind,
              'received_at': datetime.now(timezone.utc).isoformat(), 'sha256': digest,
              'line_count': len(text.splitlines()), 'origin': 'user_supplied',
              'video_watched': False, 'status': 'pending_review'}
    directory.mkdir(parents=True, exist_ok=True)
    (directory/'transcript.txt').write_bytes(raw)
    save(directory/'source.json', source)
    save(directory/'review-draft.json', {
        'source_id': source_id, 'transcript_sha256': digest, 'reviewed_by': '', 'reviewed_on': '',
        'full_transcript_read': False, 'source_alignment': 'not_checked', 'alignment_notes': '',
        'summary': '', 'gaps': ['Video, visuals and transcript alignment have not been checked.'],
        'claims': [],
    })
    return source


def load_source(source_id, root=ROOT):
    directory = source_directory(source_id, root)
    source = json.loads((directory/'source.json').read_text())
    raw = (directory/'transcript.txt').read_bytes()
    if source['source_id'] != source_id or sha(raw) != source['sha256'] or source_id != source['video_id']+'-'+sha(raw):
        raise ValueError('Transcript integrity check failed; stage edits as a new revision.')
    video, canonical = video_identity(source['url'])
    if video != source['video_id'] or canonical != source['url']:
        raise ValueError('Transcript video identity mismatch.')
    return source, raw.decode('utf-8-sig')


def validate_review(review, source, text, root=ROOT):
    if review.get('source_id') != source['source_id'] or review.get('transcript_sha256') != source['sha256']:
        raise ValueError('Review must reference this exact transcript revision.')
    required(review.get('reviewed_by'), 'Reviewer')
    date.fromisoformat(required(review.get('reviewed_on'), 'Review date'))
    if review.get('full_transcript_read') is not True:
        raise ValueError('Read the complete transcript before promotion.')
    if review.get('source_alignment') not in ('not_checked', 'checked'):
        raise ValueError('Record whether the transcript was checked against the video.')
    required(review.get('alignment_notes'), 'Transcript alignment notes')
    required(review.get('summary'), 'Editorial summary')
    metadata = review.get('video_metadata', {})
    if metadata:
        required(metadata.get('title'), 'Verified video title')
        required(metadata.get('channel'), 'Verified channel')
        date.fromisoformat(required(metadata.get('published_on'), 'Video publication date'))
        required(metadata.get('verification_notes'), 'Metadata verification notes')
    gaps = review.get('gaps')
    if not isinstance(gaps, list) or not all(isinstance(g, str) and g.strip() for g in gaps):
        raise ValueError('Record remaining gaps as a list.')
    claims = review.get('claims')
    if not isinstance(claims, list) or not claims:
        raise ValueError('Extract and review at least one Jev claim before promotion.')
    lines, seen = text.splitlines(), set()
    for claim in claims:
        cid = required(claim.get('id'), 'Claim ID')
        if not re.fullmatch(r'c[1-9][0-9]*', cid) or cid in seen:
            raise ValueError('Claim IDs must be unique c1, c2, etc.')
        seen.add(cid)
        required(claim.get('summary'), 'Claim summary')
        required(claim.get('jev_role'), 'Jev role and surrounding components')
        required(claim.get('limits'), 'Claim limits and measurement conditions')
        if claim.get('kind') not in KINDS or claim.get('status') not in STATUSES:
            raise ValueError('Unknown claim kind or evidence status.')
        anchor = claim.get('anchor', {})
        start, end = anchor.get('start_line'), anchor.get('end_line')
        if type(start) is not int or type(end) is not int or not 1 <= start <= end <= len(lines):
            raise ValueError('Claim needs valid transcript line anchors.')
        quote = required(anchor.get('quote'), 'Private supporting quotation')
        if quote not in '\n'.join(lines[start-1:end]):
            raise ValueError('Supporting quotation does not match the anchored transcript.')
        checks = claim.get('checks')
        if not isinstance(checks, list):
            raise ValueError('Record claim checks, including inaccessible or conflicting evidence.')
        for check in checks:
            public_url(check.get('url'))
            date.fromisoformat(required(check.get('checked_on'), 'Check date'))
            required(check.get('notes'), 'Inspection findings')
            if check.get('access') not in ('inspected', 'inaccessible') or check.get('finding') not in ('supports', 'contradicts', 'inconclusive'):
                raise ValueError('Invalid evidence check status.')
            if check['access'] != 'inspected' and check['finding'] != 'inconclusive':
                raise ValueError('Inaccessible evidence cannot support or contradict a claim.')
        if claim['status'] in ('corroborated', 'contradicted'):
            finding = 'supports' if claim['status'] == 'corroborated' else 'contradicts'
            if not any(c['access'] == 'inspected' and c['finding'] == finding and c['url'] != source['url'] for c in checks):
                raise ValueError('This status needs an inspected supporting or conflicting source.')
        if claim['status'] == 'reproduced':
            record = claim.get('reproduction', {})
            required(record.get('method'), 'Reproduction method and workload')
            relative = required(record.get('artifact'), 'Local reproduction artifact')
            artifact = (root/relative).resolve()
            if not artifact.is_relative_to((root/'research').resolve()) or not artifact.is_file() or sha(artifact.read_bytes()) != record.get('sha256'):
                raise ValueError('Independent reproduction needs a checksum-matched local research artifact.')
        links = claim.get('linked_sources', [])
        if not isinstance(links, list):
            raise ValueError('Linked sources must be a list.')
        for url in links:
            public_url(url)
        cases = claim.get('related_case_ids', [])
        if not isinstance(cases, list):
            raise ValueError('Related case IDs must be a list.')
        for case in cases:
            if not isinstance(case, str) or not re.fullmatch(r'[a-z0-9_-]+', case) or not (root/'resource-pool/use-cases'/(case+'.md')).is_file():
                raise ValueError('Related case ID must reference an existing case.')
    # This validates recorded evidence and structure, not truth or entailment.
    return review


def promote(source_id, review, root=ROOT):
    source, text = load_source(source_id, root)
    validate_review(review, source, text, root)
    record = {'source_id': source_id, 'review': review}
    digest = sha(json.dumps(record, sort_keys=True, ensure_ascii=False).encode())
    save(source_directory(source_id, root)/'reviews'/(digest+'.json'), record)
    save(root/'resource-pool/sources/youtube-reviews'/(source['video_id']+'.json'), record)
    return {'source_id': source_id, 'status': 'reviewed', 'review_sha256': digest,
            'next_step': 'Run scripts/export_public.py, then scripts/check_public.py. Local bot reads the reviewed export; S3 needs a new snapshot.'}


def plain(value):
    # Editorial prose cannot introduce hidden Markdown links, images or headings.
    return re.sub(r'([\\`*_{}\[\]<>#!|])', r'\\\1', ' '.join(value.splitlines()))


def render(source, review):
    metadata = review.get('video_metadata', {})
    lines = ['# YouTube research: '+plain(metadata.get('title', source['title'])), '',
             'Source type: user-supplied YouTube transcript; reviewed editorial summary.',
             'Video: '+source['url'],
             'Video publication date: '+(metadata.get('published_on') or source['published_on'] or 'not supplied')+'.',
             'Review date: '+review['reviewed_on']+'. Transcript kind: '+source['transcript_kind']+'.',
             'Transcript/video alignment: '+review['source_alignment']+'. '+plain(review['alignment_notes']),
             'Transcript review alone does not inspect visuals or reproduce demonstrations. Evidence statuses describe recorded checks, not guaranteed truth.',
             '', plain(review['summary']), '']
    if metadata:
        lines.extend(['Channel: '+plain(metadata['channel'])+'. '+plain(metadata['verification_notes']), ''])
    for claim in review['claims']:
        anchor = claim['anchor']
        lines.extend(['## '+claim['id']+' — '+claim['kind']+' — '+claim['status'], '',
                      'Claim: '+plain(claim['summary']),
                      'Jev and surrounding components: '+plain(claim['jev_role']),
                      'Limits and conditions: '+plain(claim['limits']),
                      f"Private transcript anchor: lines {anchor['start_line']}–{anchor['end_line']}. Original text retained locally."])
        if anchor.get('timestamp'):
            lines.append('Supplied transcript time range: '+plain(anchor['timestamp'])+'.')
        for check in claim['checks']:
            lines.append('Evidence check: '+check['url']+' — '+check['access']+', '+check['finding']+'; '+check['checked_on']+'. '+plain(check['notes']))
        for url in claim.get('linked_sources', []):
            lines.append('Linked source (not inspected in this review): '+url)
        for case in claim.get('related_case_ids', []):
            lines.append(f'Related existing case: [{case}](../use-cases/{case}.md).')
        if claim['status'] == 'reproduced':
            lines.append('Reproduction scope: '+plain(claim['reproduction']['method'])+'. Checksum-matched artifact retained locally.')
        lines.append('')
    lines.extend(['## Remaining gaps', '']+[plain(g) for g in review['gaps']])
    return '\n'.join(lines)+'\n'


def reviewed_exports(root=ROOT):
    """Only promoted, still-valid reviews reach the public export allowlist."""
    exports = {}
    for path in sorted((root/'resource-pool/sources/youtube-reviews').glob('*.json')):
        record = json.loads(path.read_text())
        source, text = load_source(record['source_id'], root)
        if path.stem != source['video_id']:
            raise ValueError('Review register video ID mismatch.')
        review = validate_review(record['review'], source, text, root)
        target = root/'resource-pool/youtube'/('youtube-'+source['video_id']+'.md')
        exports[target] = render(source, review)
    return exports


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    inbox = sub.add_parser('receive')
    inbox.add_argument('transcript', type=Path)
    inbox.add_argument('--title', default='')
    incoming = sub.add_parser('stage')
    incoming.add_argument('transcript', type=Path)
    incoming.add_argument('--url', required=True)
    incoming.add_argument('--title', default='')
    incoming.add_argument('--published')
    incoming.add_argument('--transcript-kind', choices=('manual', 'auto_captions', 'unknown'), default='unknown')
    approved = sub.add_parser('promote')
    approved.add_argument('source_id')
    approved.add_argument('--review', type=Path, required=True)
    args = parser.parse_args()
    if args.command == 'receive':
        result = receive(args.transcript, args.title)
    elif args.command == 'stage':
        result = stage(args.transcript, args.url, args.title, args.published, args.transcript_kind)
    else:
        result = promote(args.source_id, json.loads(args.review.read_text()))
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
