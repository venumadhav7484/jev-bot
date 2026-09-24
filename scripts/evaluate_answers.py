"""End-to-end answer evaluation against authored expectations. Makes paid Jev and GLM calls.

Without --apply it only lists the scenarios. Reports go to ignored research/evaluations/.
Expectations are authored design judgments, not ground truth; read failures before tuning.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import datetime as dt
import json
import statistics
import time

from backup_private import ROOT

FIXTURE = ROOT/'tests/fixtures/answer-eval.json'


def agreement(expected, answers, questions):
    """Python mirror of web/bot-client.mjs agreement(): only unambiguous comparisons."""
    values = list((expected or {}).values())
    notes = []
    for qid, a in answers.items():
        q = questions.get(qid, {})
        if a.get('type') == 'choice' and isinstance(q.get('criteria'), dict):
            wanted = next((v for v in values if isinstance(v, str) and v in q['criteria']), None)
            if wanted is not None:
                notes.append(wanted == a['choice'])
        elif a.get('type') == 'noul' and isinstance((expected or {}).get(qid), bool):
            notes.append(expected[qid] == (a['noul'] >= .5))
    return None if not notes else all(notes)


def check(scenario, result, seconds):
    writer = result.get('writer') or {}
    blueprint = writer.get('blueprint') or {}
    types = sorted({q.get('type') for q in blueprint.get('request', {}).get('questions', {}).values()})
    judgments = result.get('judgments') or {}
    execution = result.get('execution') or {}
    agree = [agreement(e.get('output'), x['answers'], blueprint.get('request', {}).get('questions', {}))
             for e, x in zip(blueprint.get('examples', []), execution.get('examples', []))]
    design = writer.get('status') == 'success' and execution.get('status') == 'complete'
    outcome = {'id': scenario['id'], 'seconds': round(seconds, 1), 'needs_detail': result.get('needs_detail'),
               'design': design, 'types': types, 'fit': judgments.get('fit', {}).get('choice'),
               'generation': judgments.get('generation_needed', {}).get('noul'),
               'perception': judgments.get('perception_needed', {}).get('noul'),
               'specific': result.get('coverage', {}).get('idea_specific'),
               'agreement': agree, 'citations_removed': writer.get('citations_removed'),
               'glm_requests': writer.get('requests', 1 if writer else 0),
               'usd': result.get('comparison', {}).get('total_estimated_usd')}
    if scenario.get('detail'):
        outcome['pass'] = bool(result.get('needs_detail'))
    elif scenario.get('generation'):
        outcome['pass'] = not result.get('needs_detail') and (outcome['generation'] or 0) >= .5
    elif scenario.get('perception'):
        outcome['pass'] = not result.get('needs_detail') and (outcome['perception'] or 0) >= .5
    else:
        outcome['pass'] = design and bool(set(types) & set(scenario['types']))
    return outcome


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true', help='Make paid Jev and GLM requests.')
    parser.add_argument('--only', nargs='*', help='Scenario IDs to run.')
    parser.add_argument('--workers', type=int, default=3)
    args = parser.parse_args()
    scenarios = [s for s in json.loads(FIXTURE.read_text()) if not args.only or s['id'] in args.only]
    if not args.apply:
        for s in scenarios:
            print(s['id'], '·', s['idea'])
        print(f'{len(scenarios)} scenarios. Add --apply to run them (paid).')
        return
    from research_answer import answer

    def run(scenario):
        started = time.time()
        try:
            return check(scenario, answer(scenario['idea'], 'written'), time.time()-started)
        except Exception as error:  # Record and continue; one failure must not hide the rest.
            return {'id': scenario['id'], 'pass': False, 'error': type(error).__name__, 'seconds': round(time.time()-started, 1)}
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        outcomes = list(executor.map(run, scenarios))
    seconds = sorted(o['seconds'] for o in outcomes)
    runs = [a for o in outcomes for a in o.get('agreement', []) if a is not None]
    costs = [o['usd'] for o in outcomes if isinstance(o.get('usd'), (int, float))]
    summary = {'at': dt.datetime.now(dt.timezone.utc).isoformat(), 'scenarios': len(outcomes),
               'passed': sum(o['pass'] for o in outcomes),
               'designs': sum(bool(o.get('design')) for o in outcomes),
               'repairs': sum(o.get('glm_requests') == 2 for o in outcomes),
               'example_agreement': f'{sum(runs)}/{len(runs)}',
               'seconds_p50': statistics.median(seconds), 'seconds_max': seconds[-1],
               'usd_total': round(sum(costs), 4), 'usd_unknown': len(outcomes)-len(costs)}
    out = ROOT/'research/evaluations'
    out.mkdir(parents=True, exist_ok=True)
    path = out/('answers-'+dt.date.today().isoformat()+'.json')
    path.write_text(json.dumps({'summary': summary, 'outcomes': outcomes}, indent=2)+'\n')
    for o in outcomes:
        print(('PASS' if o['pass'] else 'FAIL'), o['id'], {k: o.get(k) for k in ('seconds', 'types', 'fit', 'agreement', 'error') if o.get(k) is not None})
    print(json.dumps(summary, indent=2))
    print('Saved', path.relative_to(ROOT))


if __name__ == '__main__':
    main()
