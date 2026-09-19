"""Maintain a resumable X review queue from the captured source register.

Offline only. Rebuilding preserves review history, dispositions and retry dates.
"""
import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
POOL=ROOT/'resource-pool'
SOURCES=POOL/'sources'
CONFIG = json.loads((ROOT/'resource-pool/sources/collection-checkpoint.json').read_text())
GUILD_ID = CONFIG['guild_id']
QUEUE=SOURCES/'x-review-backlog.json'

def post_id(url):
    m=re.search(r'https?://(?:www\.)?(?:x\.com|twitter\.com|fixupx\.com|fxtwitter\.com|fixvx\.com|jf\.x\.com)/[^/]+/status/(\d+)',url)
    return m[1] if m else None

sources=json.loads((SOURCES/'external-links.json').read_text())
cases=list(csv.DictReader((POOL/'cases.tsv').open(),delimiter='\t'))
case_by_id={r['id']:r for r in cases}
case_for_message={}
case_for_post={}
for c in cases:
    for mid in c['message_ids'].split(','):
        case_for_message.setdefault(mid,set()).add(c['id'])
    for pid in re.findall(r'https?://(?:www\.)?(?:x\.com|twitter\.com|fixupx\.com|fxtwitter\.com|fixvx\.com)/[^/]+/status/(\d+)',(POOL/'use-cases'/f'{c["id"]}.md').read_text()):
        case_for_post.setdefault(pid,set()).add(c['id'])
messages={}
for filename in (Path(CONFIG['main_snapshot']).name,Path(CONFIG['thread_snapshot']).name):
    for row in json.loads((SOURCES/filename).read_text())['messages']:
        messages.setdefault(row['id'].split('-')[-1],row)
existing=json.loads(QUEUE.read_text()) if QUEUE.exists() else {'entries':[]}
entries={r['post_id']:r for r in existing['entries']}
for s in sources:
    pid=post_id(s['url'])
    if not pid:continue
    missing_media='media_blocked' in s.get('review_status','')
    if pid not in entries and s.get('access_status') not in ('fetch_failed','response_unmatched','not_attempted') and not missing_media:continue
    if pid not in entries:
        entries[pid]={
            'post_id':pid,'url':s['url'],'status':'pending_media' if missing_media else 'pending',
            'blocker':'Post text read; video displayed Unable to play media.' if missing_media else 'Public web fetch failed; full X post and linked evidence not inspected.',
            'first_recorded_on':'2026-09-19','last_attempted_on':s.get('reviewed_on',s.get('checked_on','2026-09-19')),
            'followup_attempts':0,'next_retry_on':None,'review_notes':[],
            'discovered_artifact_urls':[],
            'attempt_history':[{'date':'2026-09-19','stage':'initial_collection','outcome':s.get('access_status'),'review_status':s.get('review_status','not_reviewed')}],
        }
    r=entries[pid]
    r['source_urls']=sorted(set(r.get('source_urls',[])+[s['url']]))
    r['discord_message_ids']=sorted(set(r.get('discord_message_ids',[])+s['message_ids']),key=int)
    case_ids=set(r.get('case_ids',[]))|case_for_post.get(pid,set())
    for mid in r['discord_message_ids']:case_ids|=case_for_message.get(mid,set())
    r['case_ids']=sorted(case_ids)
    r['discord_urls']=[f'https://discord.com/channels/{GUILD_ID}/{messages[mid]["id"].split("-")[2]}/{mid}' for mid in r['discord_message_ids'] if mid in messages]
    r.setdefault('initial_access_status',s.get('access_status'))
    r.setdefault('initial_review_status',s.get('review_status','not_reviewed'))
    r.setdefault('priority',1 if any(case_by_id[c]['category'] in ('quality','security','retrieval','engineering') for c in case_ids if c in case_by_id) else 2 if case_ids else 3)
    r['case_titles']=[case_by_id[c]['title'] for c in r['case_ids'] if c in case_by_id]
    r['title']=' / '.join(r['case_titles']) or 'Unassigned X post by @'+s['url'].split('/')[3]

ordered=sorted(entries.values(),key=lambda r:(r['followup_attempts'],r['priority'],int(r['post_id'])))
document={
    'schema_version':1,'created_on':existing.get('created_on','2026-09-19'),
    'scope':'All X posts recorded as inaccessible or media-blocked in the captured source register; not every post on X.',
    'daily_batch_size':5,'timezone':'Asia/Kolkata','selection_rule':'Pending, pending_media or retry entries whose next_retry_on is null or due; lowest followup_attempts, then priority, then oldest post ID. Skip reviewed and excluded entries.',
    'retry_policy':'Record a failed attempt once per run, defer that entry 7 days, and continue with other entries. Do not retry the same unchanged blocker repeatedly within one run.',
    'automation':existing.get('automation',None),
    'counts':dict(Counter(r['status'] for r in ordered)),
    'entries':ordered,
}
QUEUE.write_text(json.dumps(document,ensure_ascii=False,indent=2)+'\n')
def cell(s):return str(s).replace('|',' / ').replace('\n',' ')
lines=['# X posts awaiting detailed investigation','',
       f'{len(ordered)} distinct posts. Status totals: '+', '.join(f'{k}: {v}' for k,v in document['counts'].items())+'.','',
       'The initial collection could not fully inspect these posts or their media. Every entry retains its X URL, Discord origin, related case files, blocker and retry history in the [JSON queue](sources/x-review-backlog.json). This is the complete backlog from the captured register, not a claim of complete X coverage.','',
       'Review up to **five posts per daily run**, with equal priority given to preserving contradictions and failures. [Review procedure](x-review-workflow.md). Rebuild this view with `python3 scripts/build-x-backlog.py`; edit progress in the JSON queue, not this generated table.','',
       '| Priority | X post | Related use case | Discord evidence | Status |','|---|---|---|---|---|']
for r in ordered:
    account=r['url'].split('/')[3]
    cs='<br>'.join(f'[{cell(case_by_id[c]["title"])}](use-cases/{c}.md)' for c in r['case_ids'] if c in case_by_id) or 'Needs case assignment'
    ds='<br>'.join(f'[{u.rsplit("/",1)[-1]}]({u})' for u in r['discord_urls'])
    lines.append(f'| {r["priority"]} | [@{account} · {r["post_id"]}]({r["url"]}) | {cs} | {ds} | {r["status"]} |')
(POOL/'x-review-backlog.md').write_text('\n'.join(lines)+'\n')
print(json.dumps({'posts':len(ordered),'status':document['counts'],'with_case_links':sum(bool(r['case_ids']) for r in ordered)}))
