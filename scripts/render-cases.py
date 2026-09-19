"""Render manually curated case records; validate source IDs before writing."""
import csv
import json
import re
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

ROOT = Path(__file__).resolve().parents[1]
POOL = ROOT / 'resource-pool'
CONFIG = json.loads((ROOT/'resource-pool/sources/collection-checkpoint.json').read_text())
GUILD_ID = CONFIG['guild_id']
messages = json.loads((ROOT / CONFIG['main_snapshot']).read_text())['messages']
messages += json.loads((ROOT / CONFIG['thread_snapshot']).read_text())['messages']
by_id = {}
for row in messages:
    # A synthetic thread starter can reuse the parent ID without its content.
    by_id.setdefault(row['id'].split('-')[-1], row)
source_status = {r['url']:r for r in json.loads((POOL/'sources/external-links.json').read_text())}
def canonical(url):
    p=urlsplit(url)
    if p.hostname in ('x.com','twitter.com','fixupx.com','fxtwitter.com','fixvx.com','jf.x.com'):
        match=re.search(r'/([^/]+)/status/(\d+)',p.path)
        if match:return f'https://x.com/{match[1]}/status/{match[2]}'
    query=urlencode([(k,v) for k,v in parse_qsl(p.query) if not k.startswith('utm_') and k not in ('s','t','si','rcm','tt_content','tt_medium')])
    return urlunsplit((p.scheme,p.netloc,p.path.rstrip('/') or '/',query,''))
cases = list(csv.DictReader((POOL/'cases.tsv').open(), delimiter='\t'))
extras = json.loads((POOL/'sources/case-extra-sources.json').read_text())
assert all(e['case_id'] in {c['id'] for c in cases} for e in extras), 'unknown extra-source case ID'
assert len({c['id'] for c in cases}) == len(cases), 'duplicate case ID'
for c in cases:
    assert re.fullmatch(r'[a-z0-9-]+', c['id']), c['id']
    assert all(c.values()), c['id']
    assert all(i in by_id for i in c['message_ids'].split(',')), c['id']
out = POOL/'use-cases'
out.mkdir(exist_ok=True)
index = ['# Jev community use cases', '', f'{len(cases)} curated case records from the 2026-09-19 Discord snapshot. This is an expanding review, not an exhaustive catalog.', '', 'All cases have an identifiable Discord source. Reported outcomes are author claims unless explicitly stated otherwise. No external project was installed or benchmark independently reproduced.', '', '[Collection coverage](sources/discord-coverage.md) · [Storage and retrieval](storage-and-retrieval.md)', '', '| Case | Category | Evidence |', '|---|---|---|']
for c in sorted(cases, key=lambda c:(c['category'],c['title'])):
    ids = c['message_ids'].split(',')
    links = []
    for i in ids:
        channel = by_id[i]['id'].split('-')[2]
        links.append(f'- [Discord message {i}](https://discord.com/channels/{GUILD_ID}/{channel}/{i}) — source read.')
    urls=set()
    for i in ids:
        for a in by_id[i]['links']:
            u=a['url']; p=urlsplit(u); host=p.hostname or ''
            if any(s in host for s in ('discord','githubassets','githubusercontent','twimg','jf.x.com')): continue
            if host in ('x.com','twitter.com') and '/status/' not in p.path: continue
            if re.search(r'\.(png|jpg|jpeg|gif|webp|mp4)(?:\?|$)',u,re.I):continue
            if u not in urls:
                urls.add(u)
                label=(a['text'].strip() or host).replace('[','(').replace(']',')').replace('\n',' ')
                evidence=source_status.get(canonical(u),{})
                review=evidence.get('review_status','not_reviewed')
                access=evidence.get('access_status','not_attempted')
                links.append(f'- [{label}]({u}) — access: `{access}`; review: `{review}`.')
    for extra in extras:
        if extra['case_id'] != c['id'] or extra['url'] in urls:
            continue
        u = extra['url']
        urls.add(u)
        evidence = source_status.get(u, {})
        label = extra['label'].replace('[', '(').replace(']', ')').replace('\n', ' ')
        links.append(f'- [{label}]({u}) — discovered via [external source]({extra["discovered_from_url"]}); access: `{evidence.get("access_status", "not_attempted")}`; review: `{evidence.get("review_status", "not_reviewed")}`.')
    # External follow-ups can be reviewed after the frozen capture date.
    # Do not backdate those case notes to the source snapshot.
    review_dates = ['2026-09-19']
    for url in urls:
        date = source_status.get(canonical(url), {}).get('reviewed_on', '')
        if re.fullmatch(r'\d{4}-\d{2}-\d{2}', date):
            review_dates.append(date)
    text = f'''---
id: {c['id']}
title: {json.dumps(c['title'],ensure_ascii=False)}
category: {c['category']}
evidence: author-reported
reviewed_on: {max(review_dates)}
independently_reproduced: false
source_message_ids: {json.dumps(ids)}
---

# {c['title']}

## What

{c['what']}

## How Jev fits

{c['how']}

## Why and impact

{c['why_impact']}

## Limits and reuse

{c['limits']}

## Sources

'''+ '\n'.join(links)+'\n\nAccess and review are separate. A returned page may contain only metadata. [Source register](../sources/external-links.json) · [Review notes](../sources/source-reviews.json).\n'
    (out/(c['id']+'.md')).write_text(text)
    index.append(f'| [{c["title"]}](use-cases/{c["id"]}.md) | {c["category"]} | Author report; see case for inspected evidence |')
(POOL/'jev-usecases.md').write_text('\n'.join(index)+'\n')
print(f'Rendered {len(cases)} cases; all source IDs resolve.')
