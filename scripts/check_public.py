"""Check public or staged files against local credentials and private provenance.

This is a publication guard, not a complete secret-detection system. It prints
paths and issue types only, never matched secrets or private source contents.
"""
import argparse
import json
from pathlib import Path
import re
import subprocess
from backup_private import ROOT, load_env
from public_links import is_discord_url, is_private_artifact, private_artifact_roots


def inspect(files):
    secrets = [v.encode() for k, v in load_env(ROOT/'.env.local').items()
               if len(v) >= 8 and any(t in k.lower() for t in ('key', 'secret', 'token', 'password'))]
    cp_path = ROOT/'resource-pool/sources/collection-checkpoint.json'
    cp = json.loads(cp_path.read_text()) if cp_path.exists() else {}
    private_names = cp.get('private_source_names', [])
    private_ids = {str(cp[k]) for k in ('guild_id', 'main_channel_id') if k in cp}
    corpus = ROOT/'research/triage/messages.jsonl'
    if corpus.exists():
        private_ids.update(r['message_id'] for r in map(json.loads, corpus.read_text().splitlines()))
    denylist = ROOT/'resource-pool/sources/private-artifact-urls.json'
    roots = private_artifact_roots(json.loads(denylist.read_text()) if denylist.exists() else [])
    findings = []
    for name, raw in files:
        p = Path(name)
        if p.parts[0] in ('research', 'resource-pool') or p.name in ('RESUME.md', 'jev-knowledge-reference.md') and len(p.parts) == 1:
            findings.append((name, 'private path'))
        if p.name.startswith('.env') and p.name != '.env.example':
            findings.append((name, 'environment file'))
        if any(secret in raw for secret in secrets):
            findings.append((name, 'credential value'))
        if re.search(rb'(?:AKIA|ASIA)[A-Z0-9]{16}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----', raw):
            findings.append((name, 'credential-like material'))
        text = raw.decode('utf-8', errors='replace')
        if any(value in text for value in private_ids) or any(n.casefold() in text.casefold() for n in private_names):
            findings.append((name, 'private source identifier/name'))
        # Generic documentation/test URLs are allowed outside the exported corpus.
        if p.parts[0] == 'docs':
            for url in re.findall(r'https?://[^\s)>\]"\x27]+', text):
                if is_discord_url(url) or is_private_artifact(url, roots):
                    findings.append((name, 'private provenance URL'))
        if re.search(r'/Users/[A-Za-z0-9._-]+/', text):
            findings.append((name, 'machine-specific absolute path'))
    return findings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--staged', action='store_true')
    args = parser.parse_args()
    if args.staged:
        names = subprocess.check_output(['git', 'diff', '--cached', '--name-only', '--diff-filter=ACMR', '-z'], cwd=ROOT).decode().split('\0')
        files = [(n, subprocess.check_output(['git', 'show', ':'+n], cwd=ROOT)) for n in names if n]
    else:
        paths = []
        for name in ('README.md', '.env.example', 'docs', 'web', 'scripts', 'tests'):
            p = ROOT/name
            paths.extend(f for f in (p.rglob('*') if p.is_dir() else [p]) if f.is_file() and '__pycache__' not in f.parts)
        files = [(p.relative_to(ROOT).as_posix(), p.read_bytes()) for p in paths]
    findings = inspect(files)
    print(json.dumps({'files_checked': len(files), 'findings': findings}, indent=2))
    raise SystemExit(bool(findings))


if __name__ == '__main__':
    main()
