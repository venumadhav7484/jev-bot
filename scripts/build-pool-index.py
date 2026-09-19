"""Build offline retrieval, provenance and coverage artifacts from curated sources."""
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
POOL=ROOT/'resource-pool'
SOURCES=POOL/'sources'
CONFIG = json.loads((ROOT/'resource-pool/sources/collection-checkpoint.json').read_text())
GUILD_ID = CONFIG['guild_id']
cases=list(csv.DictReader((POOL/'cases.tsv').open(),delimiter='\t'))
main=json.loads((ROOT / CONFIG['main_snapshot']).read_text())
threads=json.loads((ROOT / CONFIG['thread_snapshot']).read_text())
links=json.loads((SOURCES/'external-links.json').read_text())
by_id={}
for row in main['messages']+threads['messages']:
    by_id.setdefault(row['id'].split('-')[-1],row)
case_for={}
for case in cases:
    for mid in case['message_ids'].split(','):
        assert mid in by_id,(case['id'],mid)
        case_for.setdefault(mid,[]).append(case['id'])

explicit_pending=json.loads((SOURCES/'editorial-dispositions.json').read_text())
review_path = SOURCES/'editorial-review.json'
editorial = json.loads(review_path.read_text()) if review_path.exists() else {}
normalized_path = ROOT/'research/triage/messages.jsonl'
normalized = {r['message_id']: r for r in map(json.loads, normalized_path.read_text().splitlines())} if normalized_path.exists() else {}
known_cases = {c['id'] for c in cases}
for mid, decision in editorial.items():
    assert mid in by_id, ('Unknown reviewed message', mid)
    assert decision.get('reason'), ('Missing review rationale', mid)
    assert set(decision.get('case_ids', [])) <= known_cases, ('Unknown review case', mid)
    assert mid in normalized and decision['content_hash'] == normalized[mid]['content_hash'], ('Stale editorial review', mid)
coverage=[]
triage_path=ROOT/'research/triage/predictions.jsonl'
triage={r['message_id']:r for r in map(json.loads,triage_path.read_text().splitlines())} if triage_path.exists() else {}
for mid,row in by_id.items():
    channel=row['id'].split('-')[2]
    status='cited_in_case' if mid in case_for else editorial.get(mid, {}).get('status', explicit_pending.get(mid,'uncatalogued_source_row'))
    coverage.append(dict(message_id=mid,channel_id=channel,source_url=f'https://discord.com/channels/{GUILD_ID}/{channel}/{mid}',status=status,case_ids=case_for.get(mid,[])))
    if mid in editorial:
        coverage[-1]['editorial_review'] = editorial[mid]
        coverage[-1]['case_ids'] = sorted(set(coverage[-1]['case_ids']) | set(editorial[mid].get('case_ids', [])))
    if mid in triage:
        suggestion=triage[mid]
        coverage[-1]['machine_triage']={k:suggestion[k] for k in ('primary_kind','jev_relation','model','request_hash','evidence_status')}
(SOURCES/'message-coverage.json').write_text(json.dumps(coverage,indent=2)+'\n')

# Thin descriptions remain in the catalog but are excluded from default suggestions.
thin={'robotics-120-teaser','farmer-roleplay','safe-sh','gavel','textured','stll-legal','generation-ship','heist-one','microphone-mute','newsletter-classifier','principle-matching','synthetic-claims','offload-bench'}
policy_path = SOURCES/'case-retrieval-policy.json'
policy = json.loads(policy_path.read_text()) if policy_path.exists() else {}
assert set(policy) <= {c['id'] for c in cases}, 'Unknown case in retrieval policy'
for cid, rule in policy.items():
    if rule.get('default_retrieval', True):
        thin.discard(cid)
    else:
        thin.add(cid)
retrieval=[]
for c in cases:
    path=POOL/'use-cases'/f'{c["id"]}.md'
    text=path.read_text()
    assert all(h in text for h in ('## What','## How Jev fits','## Why and impact','## Limits and reuse','## Sources')),path
    retrieval.append(dict(id=c['id'],title=c['title'],category=c['category'],path=str(path.relative_to(ROOT)),resource_type='community_case',evidence='author_report_with_optional_artifact_inspection',independently_reproduced=False,default_retrieval=c['id'] not in thin,what=c['what'],how=c['how'],why_impact=c['why_impact'],limits=c['limits'],source_message_ids=c['message_ids'].split(','),source_urls=list(dict.fromkeys(re.findall(r'\]\((https?://[^)]+)\)',text)))))
    retrieval[-1]['evidence_role'] = policy.get(c['id'], {}).get('evidence_role', 'implementation_report' if c['id'] not in thin else 'thin')
    retrieval[-1]['retrieval_reason'] = policy.get(c['id'], {}).get('reason', 'Curated author report; include limitations and distinguish claims from reproduced results.')
(POOL/'retrieval-index.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in retrieval))

thread_counts=Counter(r['id'].split('-')[2] for r in threads['messages'])
access_counts=Counter(r.get('access_status','unknown') for r in links)
stats=dict(snapshot_date='2026-09-19',main_channel_rows=len(main['messages']),thread_rows=len(threads['messages']),thread_count=len(thread_counts),thread_rows_include_starters_and_parent_copies=True,external_urls=len(links),access_status_counts=dict(access_counts),curated_cases=len(cases),default_retrieval_cases=sum(r['default_retrieval'] for r in retrieval),message_coverage_status_counts=dict(Counter(r['status'] for r in coverage)),exhaustive=False,independent_benchmarks_run=0,s3_uploaded=False)
stats['machine_triage']={'completed':len(set(triage)&set(by_id)), 'remaining':len(set(by_id)-set(triage)), 'is_editorial_approval':False, 'summary':'research/triage/summary.json'}
stats['editorial_review'] = {'newly_reviewed_messages': len(editorial), 'unassigned_messages': sum(r['status'] == 'uncatalogued_source_row' for r in coverage), 'unresolved_evidence_statuses': dict(Counter(r['status'] for r in editorial.values() if r['status'] in {'media_context_unresolved', 'measurement_context_unresolved', 'reported_use_insufficient_detail'}))}
stats['editorial_review']['evidence_flags_survive_case_assignment'] = True
stats['external_review_status_counts'] = dict(Counter(r.get('review_status', 'not_reviewed') for r in links))
backup_path = ROOT/'research/storage/latest-backup.json'
if backup_path.exists():
    backup = json.loads(backup_path.read_text())
    stats['s3_uploaded'] = backup.get('download_and_file_hashes_verified', False)
    stats['s3_backup_completed_at'] = backup['completed_at']
(POOL/'coverage-summary.json').write_text(json.dumps(stats,indent=2)+'\n')
manifest=[]
for p in sorted(list(POOL.rglob('*'))+[ROOT/'jev-knowledge-reference.md']):
    if not p.is_file() or p.name=='manifest.json':continue
    raw=p.read_bytes()
    manifest.append(dict(path=str(p.relative_to(ROOT)),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
(POOL/'manifest.json').write_text(json.dumps(dict(snapshot_date='2026-09-19',files=manifest),indent=2)+'\n')
print(json.dumps(stats,indent=2))
