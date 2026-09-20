"""Build private review packets using existing cases, source notes and Jev triage.

Offline only. A URL match is a reuse candidate, not proof of unchanged content.
Every incoming message remains pending editorial review. No model gate approves
or discards evidence, and no public files or collection cursors are changed.
"""
import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from jev_triage import dump, stamp

ROOT = Path(__file__).resolve().parents[1]
X_HOSTS = {'x.com', 'www.x.com', 'twitter.com', 'www.twitter.com',
           'fixupx.com', 'fxtwitter.com', 'fixvx.com', 'jf.x.com'}


def source_key(url):
    """Conservative identity key; keep functional queries and fragments."""
    p = urlsplit(url)
    if p.scheme not in ('http', 'https') or not p.hostname or p.username or p.password:
        return None
    host = p.hostname.lower()
    if host in X_HOSTS:
        match = re.fullmatch(r'/[^/]+/status/(\d+)/?', p.path)
        if match:
            return 'https://x.com/i/status/' + match[1]
    query = urlencode([(k, v) for k, v in parse_qsl(p.query, keep_blank_values=True)
                       if not k.lower().startswith('utm_') and k.lower() != 'fbclid'])
    return urlunsplit((p.scheme, p.netloc.lower(), p.path or '/', query, p.fragment))


def link_kind(url):
    p = urlsplit(url)
    host = (p.hostname or '').lower()
    if host == 'discord.com' and p.path.startswith('/channels/'):
        return 'discussion_context'
    if (host in ('opengraph.githubassets.com', 'repository-images.githubusercontent.com',
                 'pbs.twimg.com', 'cdn-thumbnails.huggingface.co') or
            re.search(r'\.(png|jpe?g|gif|webp|svg|mp4|webm|mp3|wav|ogg)$', p.path, re.I)):
        return 'media_or_preview'
    return 'source'


def case_index(root):
    by_message, cases = defaultdict(set), {}
    with (root/'resource-pool/cases.tsv').open() as handle:
        for case in csv.DictReader(handle, delimiter='\t'):
            cases[case['id']] = case
            for mid in case['message_ids'].split(','):
                by_message[mid].add(case['id'])
    return by_message, cases


def cache_receipt(root, source):
    relative = source.get('fetch_capture_path')
    if not relative:
        return {'available': False}
    path = (root/relative).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        return {'available': False}
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    expected = source.get('capture_sha256')
    return {'available': True, 'path': relative, 'sha256': actual,
            'matches_registered_hash': actual == expected if expected else None}


def plan(root, batch_id):
    if not re.fullmatch(r'[a-f0-9]{64}', batch_id):
        raise ValueError('Expected staged capture batch ID.')
    batch = root/'research/incoming'/batch_id
    manifest = json.loads((batch/'manifest.json').read_text())
    if manifest['batch_id'] != batch_id:
        raise ValueError('Manifest batch ID mismatch.')
    messages = [json.loads(s) for s in (batch/'triage/messages.jsonl').read_text().splitlines()]
    predictions = {r['message_id']: r for r in
                   map(json.loads, (batch/'triage/predictions.jsonl').read_text().splitlines())}
    by_message, cases = case_index(root)
    existing = defaultdict(list)
    for source in json.loads((root/'resource-pool/sources/external-links.json').read_text()):
        key = source_key(source['url'])
        if key:
            ids = set(source.get('case_ids', []))
            for mid in source.get('message_ids', []):
                ids.update(by_message[mid])
            existing[key].append({'url': source['url'], 'case_ids': sorted(ids),
                                  'review_status': source.get('review_status'),
                                  'reviewed_on': source.get('reviewed_on'),
                                  'note': source.get('note', ''),
                                  'cache': cache_receipt(root, source)})
    groups, packets = {}, []
    for row in messages:
        mid = row['message_id']
        body_keys = {source_key(u.rstrip('.,;!?)')) for u in re.findall(r'https?://[^\s<>"\x00]+', row['body'])}
        prediction = predictions.get(mid)
        if prediction and prediction['content_hash'] != row['content_hash']:
            raise ValueError('Stale Jev prediction for incoming source.')
        source_keys, media, context, candidates = [], [], [], set(by_message[mid])
        target_keys, required_media = [], []
        for url in row['links']:
            key = source_key(url)
            if key is None:
                continue
            kind = link_kind(url)
            if kind != 'source':
                (media if kind == 'media_or_preview' else context).append(url)
                parsed = urlsplit(url)
                attachment = (parsed.hostname in ('cdn.discordapp.com', 'media.discordapp.net') and parsed.path.startswith('/attachments/'))
                if kind == 'media_or_preview' and (key in body_keys or attachment):
                    required_media.append(url)
                continue
            if key not in source_keys:
                source_keys.append(key)
            group = groups.setdefault(key, {'key': key, 'urls': [], 'message_ids': [],
                                            'prior_reviews': existing.get(key, []),
                                            'status': 'pending_change_check' if existing.get(key) else 'pending_source_review'})
            if url not in group['urls']:
                group['urls'].append(url)
            if mid not in group['message_ids']:
                group['message_ids'].append(mid)
            # Embed headers and quoted replies often link to unrelated projects
            # or platform homepages. Only target-body URLs propose case merges.
            if key in body_keys:
                target_keys.append(key)
                for old in group['prior_reviews']:
                    candidates.update(old['case_ids'])
        packets.append({'message_id': mid, 'source_url': row['source_url'],
                        'content_hash': row['content_hash'], 'body': row['body'],
                        'quote_context': row['quote_context'], 'source_keys': source_keys,
                        'target_source_keys': sorted(set(target_keys)), 'required_media_urls': required_media,
                        'media_or_preview_urls': media, 'discussion_context_urls': context,
                        'existing_case_candidates': [cases[c] for c in sorted(candidates) if c in cases],
                        'jev_suggestion': prediction, 'status': 'pending_editorial_review'})
    summary = {'messages': len(packets), 'source_groups': len(groups),
               'previously_registered_source_groups': sum(bool(g['prior_reviews']) for g in groups.values()),
               'new_source_groups': sum(not g['prior_reviews'] for g in groups.values()),
               'messages_with_case_candidates': sum(bool(p['existing_case_candidates']) for p in packets),
               'source_references': sum(len(p['source_keys']) for p in packets),
               'messages_with_media_or_preview': sum(bool(p['media_or_preview_urls']) for p in packets),
               'prediction_priorities': dict(Counter(p['jev_suggestion']['priority'] for p in packets if p['jev_suggestion'])),
               'automatically_approved': 0, 'automatically_excluded': 0,
               'end_to_end_speedup_measured': False}
    result = {'version': 'delta-review-plan-v1', 'created_at': stamp(), 'batch_id': batch_id,
              'summary': summary, 'source_groups': list(groups.values()), 'packets': packets}
    dump(batch/'review-plan.json', result)
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch-id', required=True)
    args = parser.parse_args()
    print(json.dumps(plan(ROOT, args.batch_id), indent=2))
