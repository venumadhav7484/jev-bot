"""Build a reproducible source register from the locally captured Discord DOM.

No credentials, Discord API calls, network requests, or inference are used.
The register is discovery evidence, not a list of verified Jev integrations.
"""
import json
import re
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / 'resource-pool' / 'sources'
CONFIG = json.loads((ROOT/'resource-pool/sources/collection-checkpoint.json').read_text())
GUILD_ID = CONFIG['guild_id']
data = json.loads((ROOT / CONFIG['main_snapshot']).read_text())
data['messages'] += json.loads((SOURCES / 'discord-threads-2026-09-19.json').read_text())['messages']
access = {r['url']:r for r in json.loads((SOURCES/'link-access.json').read_text())}
reviews = {r['url']:r for r in json.loads((SOURCES/'source-reviews.json').read_text())}
register = {}
for row in data['messages']:
    message_id = row['id'].split('-')[-1]
    for link in row['links']:
        url = link['url']
        p = urlsplit(url)
        host = (p.hostname or '').lower()
        if p.scheme not in ('https', 'http'):
            continue
        if any(s in host for s in ('discord', 'githubassets', 'githubusercontent', 'twimg', 'substackcdn', 'klipy', 'tenor')):
            continue
        if re.search(r'\.(png|jpg|jpeg|gif|webp|svg|mp4)(?:$|/)', p.path, re.I):
            continue
        if host in ('x.com', 'twitter.com', 'fixupx.com', 'fxtwitter.com', 'fixvx.com', 'jf.x.com'):
            status = re.search(r'/([^/]+)/status/(\d+)', p.path)
            if not status:
                continue
            url = 'https://x.com/' + status[1] + '/status/' + status[2]
        else:
            # Preserve functional query parameters, remove only tracking parameters.
            from urllib.parse import parse_qsl, urlencode
            query = urlencode([(k,v) for k,v in parse_qsl(p.query) if not k.startswith('utm_') and k not in ('s','t','si','rcm','tt_content','tt_medium')])
            url = urlunsplit((p.scheme, p.netloc, p.path.rstrip('/') or '/', query, ''))
        entry = register.setdefault(url, {'url':url, 'message_ids':[], 'labels':[], 'access_status':'not_attempted'})
        if message_id not in entry['message_ids']:
            entry['message_ids'].append(message_id)
        label = link['text'].strip()
        if label and label not in entry['labels']:
            entry['labels'].append(label)

# External discoveries retain their own provenance, never invented Discord IDs.
extras = json.loads((SOURCES/'case-extra-sources.json').read_text())
for extra in extras:
    url = extra['url']
    assert urlsplit(url).scheme in ('https', 'http'), url
    entry = register.setdefault(url, {'url':url, 'message_ids':[], 'labels':[], 'access_status':'not_attempted'})
    for key, value in (('case_ids', extra['case_id']), ('discovered_from_urls', extra['discovered_from_url']), ('labels', extra['label'])):
        if value not in entry.setdefault(key, []):
            entry[key].append(value)

out = sorted(register.values(), key=lambda r:r['url'])
for row in out:
    if row['url'] in access:
        row.update({k:v for k,v in access[row['url']].items() if k != 'url'})
    if row['url'] in reviews:
        row.update({k:v for k,v in reviews[row['url']].items() if k != 'url'})
(SOURCES / 'external-links.json').write_text(json.dumps(out, ensure_ascii=False, indent=2)+'\n')
print(f'{len(data["messages"])} messages; {len(out)} external source URLs')
