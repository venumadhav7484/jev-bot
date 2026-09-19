"""Stage an incremental authorized Discord capture without changing the frozen corpus.

Input uses the existing UI capture format: {guild_id, messages:[{id,text,links}]}.
This reads local exports only. It does not authenticate to Discord or collect posts.
New and edited IDs are queued; captured and fully reviewed cursors remain distinct.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
from jev_triage import dump, stamp

ROOT = Path(__file__).resolve().parents[1]


def fingerprint(row):
    return hashlib.sha256(json.dumps({'text': row['text'], 'links': row.get('links', [])},
                                     sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def stage(document, root=ROOT):
    checkpoint = json.loads((root/'resource-pool/sources/collection-checkpoint.json').read_text())
    if not isinstance(document, dict) or str(document.get('guild_id')) != checkpoint['guild_id']:
        raise ValueError('Capture guild_id must match the private collection checkpoint.')
    rows = document.get('messages')
    if not isinstance(rows, list) or not rows:
        raise ValueError('Provide a nonempty messages array.')
    previous = {}
    for relative in (checkpoint['main_snapshot'], checkpoint['thread_snapshot']):
        for row in json.loads((root/relative).read_text())['messages']:
            mid = row['id'].split('-')[-1]
            previous.setdefault(mid, set()).add(fingerprint(row))
    unique = {}
    for row in rows:
        if not isinstance(row, dict) or not re.fullmatch(r'chat-messages-\d+-\d+', row.get('id', '')):
            raise ValueError('Unrecognized captured message ID.')
        if not isinstance(row.get('text'), str) or not isinstance(row.get('links', []), list):
            raise ValueError('Each row needs text and an optional links array.')
        for link in row.get('links', []):
            if not isinstance(link, dict) or not isinstance(link.get('url'), str) or not isinstance(link.get('text', ''), str):
                raise ValueError('Invalid captured link.')
        _, _, channel, mid = row['id'].split('-')
        key = (mid, fingerprint(row))
        if key not in unique:
            unique[key] = {'message_id': mid, 'channel_id': channel, 'content_hash': key[1], 'row': row,
                           'status': 'unchanged' if key[1] in previous.get(mid, set()) else 'edited' if mid in previous else 'new'}
    entries = sorted(unique.values(), key=lambda r: (int(r['message_id']), r['content_hash']))
    digest = hashlib.sha256(json.dumps(entries, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    directory = root/'research/incoming'/digest
    manifest = directory/'manifest.json'
    if manifest.exists():
        return json.loads(manifest.read_text())
    main_ids = [r['message_id'] for r in entries if r['channel_id'] == checkpoint['main_channel_id']]
    result = {'batch_id': digest, 'staged_at': stamp(), 'stage': 'pending_review',
              'counts': {s: sum(r['status'] == s for r in entries) for s in ('new', 'edited', 'unchanged')},
              'frozen_capture_cursor': checkpoint['capture_high_water_message_id'],
              'incoming_main_high_water': max(main_ids, key=int) if main_ids else None,
              'review_cursor_advanced': False, 'capture_cursor_advanced': False,
              'next_step': 'Inspect new/edited rows and thread context. Promote an approved immutable snapshot, then run normalization, triage and editorial review before consolidation.'}
    dump(directory/'capture.json', document)
    dump(directory/'changes.json', entries)
    dump(manifest, result)
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('input', type=Path)
    args = p.parse_args()
    print(json.dumps(stage(json.loads(args.input.read_text())), indent=2))


if __name__ == '__main__':
    main()
