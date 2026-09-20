"""Export an allowlisted, sanitized public documentation snapshot.

Raw research stays local. Review the Git diff and scan staged files before pushing.
"""
import json
import os
from pathlib import Path
import re
from public_links import is_discord_url, is_private_artifact as private_url, private_artifact_roots

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT/'docs'
mapping = {ROOT/'jev-knowledge-reference.md': DOCS/'jev-knowledge-reference.md'}
names = ('jev-usecases.md', 'integration-patterns.md', 'jev-bot-answer-guide.md',
         'pending-and-ecosystem.md', 'storage-and-retrieval.md', 'use-case-template.md',
         'community-evidence-findings.md', 'completion-status.md', 'jev-master-guide.md', 'review-backlog.md',
         'bot-knowledge-flow.md', 'youtube-source-workflow.md', 'incremental-findings.md')
mapping.update({ROOT/'resource-pool'/name:DOCS/name for name in names})
mapping.update({p:DOCS/'use-cases'/p.name for p in (ROOT/'resource-pool/use-cases').glob('*.md')})
mapping[ROOT/'research/README.md'] = DOCS/'research-pipeline.md'
mapping[ROOT/'research/jev-triage-experiment.md'] = DOCS/'local-triage-experiment.md'
config=json.loads((ROOT/'resource-pool/sources/collection-checkpoint.json').read_text())
private_ids={str(config['guild_id']),str(config['main_channel_id'])}
private_artifact_path = ROOT/'resource-pool/sources/private-artifact-urls.json'
private_artifacts = json.loads(private_artifact_path.read_text()) if private_artifact_path.exists() else []
private_roots = private_artifact_roots(private_artifacts)


def is_private_artifact(url):
    return private_url(url, private_roots)


def sanitize(source, target):
    text=source.read_text()
    text=re.sub(r'^source_message_ids:.*\n','',text,flags=re.M)
    def link(match):
        label,url=match.groups()
        if is_discord_url(url):
            return 'Discord source (private provenance retained locally)'
        if is_private_artifact(url):
            return 'Private artifact (provenance retained locally)'
        if url.startswith(('https://','http://','#')):
            return match.group(0)
        path,sep,anchor=url.partition('#')
        original=(source.parent/path).resolve()
        exported=mapping.get(original)
        if exported:
            new=os.path.relpath(exported,target.parent)
            return f'[{label}]({new}'+('#'+anchor if sep else '')+')'
        if original.is_relative_to(ROOT/'scripts') or original.is_relative_to(ROOT/'tests'):
            return f'[{label}]({os.path.relpath(original,target.parent)})'
        return label+' (local-only evidence)'
    text=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',link,text)
    def bare_url(match):
        url = match.group(0)
        if is_discord_url(url):
            return 'Discord source (private reference)'
        if is_private_artifact(url):
            return 'Private artifact (provenance retained locally)'
        return url
    text=re.sub(r'https?://[^\s)>\]"\x27]+', bare_url, text)
    for name in config.get('private_source_names', []):
        text=re.sub(re.escape(name),'Discord source',text,flags=re.I)
    text=text.replace('daily five-post automation remains active','daily five-post automation is paused')
    text=text.replace('Daily X review remains active','Daily X review is paused')
    text=text.replace('X has a daily retry queue','X has a paused daily retry queue')
    text=re.sub(r'(?m)^- Discord source \(private provenance retained locally\).*$', '- Discord source — private provenance retained locally.',text)
    # Keep provenance in private records, without a placeholder bullet in public pages.
    text=re.sub(r'(?m)^- Discord source — private provenance retained locally\.\n?', '', text)
    for value in private_ids:
        text=text.replace(value,'[private source identifier]')
    for value in sorted(private_artifacts, key=len, reverse=True):
        text=text.replace(value, 'Private artifact (provenance retained locally)')
    return text


# Raw transcripts are never export candidates. Recheck promoted review integrity
# on every rebuild, then pass only editorial summaries through sanitization.
from youtube_sources import reviewed_exports
from check_public import inspect
reviewed = reviewed_exports(ROOT)
prepared = {}
for source, content in reviewed.items():
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text(content)
    target = DOCS/'youtube'/source.name
    prepared[target] = sanitize(source, target)
findings = inspect([(p.relative_to(ROOT).as_posix(), content.encode()) for p, content in prepared.items()])
if findings:
    raise ValueError('YouTube export failed the public-content guard; review local source summaries.')
for source in reviewed:
    mapping[source] = DOCS/'youtube'/source.name
# Remove only this exporter's stale generated pages after reviews are withdrawn.
for target in (DOCS/'youtube').glob('youtube-*.md'):
    if target not in prepared:
        target.unlink()

public_records = []
retrieval = {r['id']: r for r in map(json.loads, (ROOT/'resource-pool/retrieval-index.jsonl').read_text().splitlines())}
for source,target in mapping.items():
    target.parent.mkdir(parents=True,exist_ok=True)
    content = sanitize(source,target)
    target.write_text(content)
    if source.parent == ROOT/'resource-pool/use-cases':
        row = retrieval[source.stem]
        public_records.append({'id': row['id'], 'title': row['title'], 'category': row['category'],
                               'default_retrieval': row['default_retrieval'], 'evidence_role': row['evidence_role'],
                               'path': target.relative_to(ROOT).as_posix(), 'body': content})
# Derived examples stay separate from source Markdown and the model's evidence.
from case_designs import export_designs, source_hash
for record in public_records:
    record['design_source_hash'] = source_hash(record)
design_count = export_designs(public_records, DOCS/'case-designs.json')
print(f'Exported {design_count}/{len(public_records)} current teaching designs.')
(DOCS/'bot-cases.json').write_text(json.dumps(public_records, ensure_ascii=False, indent=2)+'\n')
summary=json.loads((ROOT/'resource-pool/coverage-summary.json').read_text())
summary['machine_triage'].pop('summary',None)
triage=json.loads((ROOT/'research/triage/summary.json').read_text())
(DOCS/'metrics.json').write_text(json.dumps({'research_status':config.get('research_status','unknown'),'coverage':summary,'triage':triage},indent=2)+'\n')
print(f'Exported {len(mapping)} sanitized Markdown documents and aggregate metrics. Private inputs remain local.')
