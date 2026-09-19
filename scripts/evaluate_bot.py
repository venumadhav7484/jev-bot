"""Authored end-to-end assistant checks; no API calls or independent accuracy estimate."""
import json
from jev_bot import ROOT, answer


def evaluate():
    scenarios = json.loads((ROOT/'tests/fixtures/retrieval-scenarios.json').read_text())
    results = []
    for scenario in scenarios:
        response = answer(scenario['idea'])
        supports = {c['id'] for c in response['support']}
        counters = {c['id'] for c in response['counterevidence']}
        cards = response['support'] + response['counterevidence']
        checks = {
            'routes_idea': response['pattern'] != 'unknown',
            'expected_support': bool(supports & set(scenario['support'])) if 'support' in scenario else True,
            'expected_counterexample': bool(counters & set(scenario['counter'])) if 'counter' in scenario else True,
            'preserves_limits_and_sources': all(c['limits'] and c['sources'] for c in cards),
            'local_citations_resolve': all((ROOT/c['path']).is_file() for c in cards),
            'marks_design_unexecuted': response['prototype_is_unexecuted_design'],
            'does_not_claim_exhaustive': response['coverage']['exhaustive'] is False,
        }
        results.append({'id': scenario['id'], 'pattern': response['pattern'], 'support': sorted(supports),
                        'counterevidence': sorted(counters), 'checks': checks, 'passed': all(checks.values())})
    unknown = answer('Something for my business')
    results.append({'id': 'unknown_abstention', 'passed': unknown['fit'] == 'Insufficient detail' and not unknown['prototype'] and bool(unknown['questions'])})
    return {'scope': 'Eleven authored natural-language assistant scenarios, including abstention. Local routing only; not independent answer-quality validation.',
            'api_calls': 0, 'scenarios': len(results), 'passed': sum(r['passed'] for r in results), 'results': results}


if __name__ == '__main__':
    report = evaluate()
    target = ROOT/'research/evaluations/bot-report.json'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))
    raise SystemExit(report['passed'] != report['scenarios'])
