"""Build and query a local, citation-preserving SQLite evidence index."""
import argparse
import csv
import json
from pathlib import Path
import re
import sqlite3

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / 'research/triage'
DB = ROOT / 'research/evidence.sqlite3'


def jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()] if path.exists() else []


def build():
    target = DB.with_suffix('.building.sqlite3')
    if target.exists():
        target.unlink()
    conn = sqlite3.connect(target)
    conn.executescript('''
        CREATE TABLE evidence (id TEXT PRIMARY KEY, resource_type TEXT, title TEXT, body TEXT,
          source_url TEXT, category TEXT, jev_relation TEXT, flags TEXT, links TEXT, case_ids TEXT,
          review_status TEXT, content_hash TEXT, default_retrieval INTEGER);
        CREATE VIRTUAL TABLE evidence_fts USING fts5(id UNINDEXED, title, body);
        CREATE TABLE external_sources (url TEXT PRIMARY KEY, metadata TEXT);
    ''')
    predictions = {r['message_id']: r for r in jsonl(WORK / 'predictions.jsonl')}
    for row in jsonl(WORK / 'messages.jsonl'):
        pred = predictions.get(row['message_id'], {})
        values = (row['message_id'], 'discord_message', row['body'][:100].replace('\n', ' '), row['body'], row['source_url'],
                  pred.get('primary_kind', 'not_triaged'), pred.get('jev_relation', 'not_established'),
                  json.dumps(pred.get('flags', {})), json.dumps(row['links']), json.dumps(row['case_ids']),
                  'machine_triage_only' if pred else 'captured_only', row['content_hash'], 0)
        conn.execute('INSERT INTO evidence VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', values)
        conn.execute('INSERT INTO evidence_fts VALUES (?,?,?)', values[:1] + values[2:4])
    retrieval = {r['id']:r for r in jsonl(ROOT / 'resource-pool/retrieval-index.jsonl')}
    with (ROOT / 'resource-pool/cases.tsv').open() as handle:
        for row in csv.DictReader(handle, delimiter='\t'):
            path = ROOT / 'resource-pool/use-cases' / (row['id'] + '.md')
            body = path.read_text()
            links = re.findall(r'\]\((https?://[^)]+)\)', body)
            values = (row['id'], 'curated_case', row['title'], body, str(path.relative_to(ROOT)), row['category'],
                      'see_case_evidence', '{}', json.dumps(links), json.dumps([row['id']]), 'curated_author_report', '', int(retrieval.get(row['id'],{}).get('default_retrieval',False)))
            conn.execute('INSERT INTO evidence VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', values)
            conn.execute('INSERT INTO evidence_fts VALUES (?,?,?)', values[:1] + values[2:4])
    for row in json.loads((ROOT / 'resource-pool/sources/external-links.json').read_text()):
        conn.execute('INSERT INTO external_sources VALUES (?,?)', (row['url'], json.dumps(row)))
    # Include capability reference and cross-case lessons alongside examples.
    for relative in ('jev-knowledge-reference.md', 'resource-pool/community-evidence-findings.md', 'resource-pool/integration-patterns.md'):
        path = ROOT / relative
        parts = re.split(r'(?m)^## ', path.read_text())
        for number, part in enumerate(parts):
            if not part.strip():
                continue
            title = part.splitlines()[0].lstrip('# ')
            rid = f'reference:{path.stem}:{number}'
            links = re.findall(r'\]\((https?://[^)]+)\)', part)
            values = (rid, 'reference', title, part, relative, 'reference_or_synthesis', 'see_cited_evidence', '{}',
                      json.dumps(links), '[]', 'curated_reference_with_attributed_claims', '', 1)
            conn.execute('INSERT INTO evidence VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', values)
            conn.execute('INSERT INTO evidence_fts VALUES (?,?,?)', values[:1] + values[2:4])
    conn.commit()
    counts = dict(conn.execute('SELECT resource_type, count(*) FROM evidence GROUP BY resource_type'))
    conn.close()
    target.replace(DB)
    print(json.dumps({'database': str(DB), 'counts': counts}))


def search(query, limit, kind):
    # Literal token quoting prevents user text from becoming FTS query syntax.
    tokens = re.findall(r'\w+', query)
    if not tokens:
        raise ValueError('Search requires words')
    match = ' OR '.join('"' + word + '"' for word in tokens)
    conn = sqlite3.connect(f'file:{DB}?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    sql = '''SELECT e.*, bm25(evidence_fts, 0, 3, 1) AS rank
             FROM evidence_fts JOIN evidence e ON e.id = evidence_fts.id
             WHERE evidence_fts MATCH ?'''
    params = [match]
    if kind:
        sql += ' AND e.resource_type = ?'
        params.append(kind)
    sql += ' ORDER BY rank LIMIT ?'
    params.append(limit)
    for row in conn.execute(sql, params):
        result = dict(row)
        result['excerpt'] = result.pop('body')[:1200]
        for key in ('flags', 'links', 'case_ids'):
            result[key] = json.loads(result[key])
        print(json.dumps(result, ensure_ascii=False))
    conn.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('build')
    find = sub.add_parser('search')
    find.add_argument('query')
    find.add_argument('--limit', type=int, default=10)
    find.add_argument('--kind', choices=('discord_message', 'curated_case', 'reference'))
    args = parser.parse_args()
    if args.command == 'build':
        build()
    else:
        search(args.query, args.limit, args.kind)


if __name__ == '__main__':
    main()
