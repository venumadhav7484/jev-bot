"""Run authored retrieval probes; this does not evaluate generated bot answers."""
import argparse
import json
from pathlib import Path
from evidence import ROOT, search_records


def evaluate():
    scenarios = json.loads((ROOT / 'tests/fixtures/retrieval-scenarios.json').read_text())
    results = []
    for scenario in scenarios:
        checks = []
        for query_field, expected_field, purpose in (
            ('query', 'support', 'recommendation'),
            ('counter_query', 'counter', 'counterevidence'),
        ):
            if query_field not in scenario:
                continue
            rows = search_records(scenario[query_field], 10, purpose=purpose, full=True)
            ids = [r['id'] for r in rows]
            hit = bool(set(ids) & set(scenario[expected_field]))
            allowed = all(r['resource_type'] != 'discord_message' and
                          (purpose != 'recommendation' or r['default_retrieval']) for r in rows)
            provenance = all((ROOT / r['source_url']).is_file() and bool(r['body']) for r in rows)
            checks.append({'purpose': purpose, 'query': scenario[query_field],
                           'retrieved_ids': ids, 'expected_any': scenario[expected_field],
                           'expected_evidence_found': hit, 'retrieval_policy_passed': allowed,
                           'local_provenance_resolves': provenance,
                           'passed': hit and allowed and provenance})
        results.append({'id': scenario['id'], 'checks': checks,
                        'passed': all(c['passed'] for c in checks)})
    return {'scope': 'Ten authored search scenarios over the local snapshot; not an independent relevance benchmark or end-to-end chatbot evaluation.',
            'queries_are_authored': True, 'model_calls': 0,
            'scenarios': len(results), 'passed': sum(r['passed'] for r in results), 'results': results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    report = evaluate()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report['passed'] == report['scenarios'] else 1)


if __name__ == '__main__':
    main()
