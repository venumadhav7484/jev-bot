"""Export an allowlisted, sanitized public documentation snapshot.

Raw research stays local. Review the Git diff and scan staged files before pushing.
"""
import json
import os
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT/'docs'
mapping = {ROOT/'jev-knowledge-reference.md': DOCS/'jev-knowledge-reference.md'}
names = ('jev-usecases.md', 'integration-patterns.md', 'jev-bot-answer-guide.md',
         'pending-and-ecosystem.md', 'storage-and-retrieval.md', 'use-case-template.md',
         'community-evidence-findings.md', 'completion-status.md')
mapping.update({ROOT/'resource-pool'/name:DOCS/name for name in names})
mapping.update({p:DOCS/'use-cases'/p.name for p in (ROOT/'resource-pool/use-cases').glob('*.md')})
mapping[ROOT/'research/README.md'] = DOCS/'research-pipeline.md'
mapping[ROOT/'research/jev-triage-experiment.md'] = DOCS/'local-triage-experiment.md'
config=json.loads((ROOT/'resource-pool/sources/collection-checkpoint.json').read_text())
private_ids={str(config['guild_id']),str(config['main_channel_id'])}


def sanitize(source, target):
    text=source.read_text()
    text=re.sub(r'^source_message_ids:.*\n','',text,flags=re.M)
    def link(match):
        label,url=match.groups()
        if re.search(r'https?://[^/]*(?:discord(?:app)?\.com|discord\.gg)',url):
            return 'Discord source (private provenance retained locally)'
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
    text=re.sub(r'https?://(?:cdn\.)?discord(?:app)?\.com/[^\s)>]+','Discord source (private reference)',text)
    text=re.sub(r'https?://discord\.gg/[^\s)>]+','Discord source (private reference)',text)
    for name in config.get('private_source_names', []):
        text=re.sub(re.escape(name),'Discord source',text,flags=re.I)
    text=text.replace('daily five-post automation remains active','daily five-post automation is paused')
    text=text.replace('daily five-post automation remains active','daily five-post automation is paused')
    text=text.replace('Daily X review remains active','Daily X review is paused')
    text=text.replace('X has a daily retry queue','X has a paused daily retry queue')
    text=re.sub(r'(?m)^- Discord source \(private provenance retained locally\).*$', '- Discord source — private provenance retained locally.',text)
    text=re.sub(r'(\n- Discord source — private provenance retained locally\.){2,}',r'\n- Discord source — private provenance retained locally.',text)
    for value in private_ids:
        text=text.replace(value,'[private source identifier]')
    return text


for source,target in mapping.items():
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(sanitize(source,target))
summary=json.loads((ROOT/'resource-pool/coverage-summary.json').read_text())
summary['machine_triage'].pop('summary',None)
triage=json.loads((ROOT/'research/triage/summary.json').read_text())
(DOCS/'metrics.json').write_text(json.dumps({'research_status':'paused','coverage':summary,'triage':triage},indent=2)+'\n')
print(f'Exported {len(mapping)} sanitized Markdown documents and aggregate metrics. Private inputs remain local.')
