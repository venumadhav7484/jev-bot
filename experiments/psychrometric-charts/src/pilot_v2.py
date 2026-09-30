"""Pilot v2 (PLAN.md, second section): return all 7 properties; code narrows each number's options by its unit.

Usage:
  python pilot_v2.py run [--workers 8] [--limit N]   -> runs/pilot2_raw.jsonl (resumable; transport retries only)
  python pilot_v2.py score                           -> runs/pilot2_results.json
The value-labelling instruction is v1's, unchanged (run_pilot.payload wording).
"""
import argparse
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from pathlib import Path
import statistics
import sys
import threading

sys.path.insert(0, str(Path(__file__).resolve().parent))
import psychro as ps
from questions import extract
from run_pilot import MODEL, ORDINAL, PROPERTIES, call, key
from score_pilot import TOL, USD_PER_M, to_si

HERE = Path(__file__).resolve().parents[1]
QUESTIONS, RAW, OUT = HERE / 'data/pilot2_questions.jsonl', HERE / 'runs/pilot2_raw.jsonl', HERE / 'runs/pilot2_results.json'
PASS = 194
TEMPS = ('tdb', 'twb', 'tdp')
BY_UNIT = {'°C': TEMPS, 'C': TEMPS, 'degrees': TEMPS, '°F': TEMPS, 'F': TEMPS, 'degrees F': TEMPS,
           '%': ('rh',), 'g/kg': ('w',), 'kJ/kg': ('h',), 'm³/kg': ('v',), '': ps.PROPS}
ALL = 'all other properties'
ASKED = {**{name: desc for name, desc in PROPERTIES.values()}, ALL: 'All other properties: the text asks for every remaining property'}
NAME_TO_KEY = {name: k for k, (name, _) in PROPERTIES.items()}


def plan(text):
    """Numbers, each with its unit-validated options (a single option is assigned by code)."""
    return [{'raw': n['raw'], 'value': n['value'], 'unit': n['unit'], 'options': BY_UNIT[n['unit']]} for n in extract(text)]


def payload(text):
    questions = {}
    for k, n in enumerate(plan(text)):
        if len(n['options']) > 1:
            questions[f'value_{k + 1}'] = {'type': 'choice', 'criteria': {PROPERTIES[p][0]: PROPERTIES[p][1] for p in n['options']},
                'instructions': f'`text` is a question about moist air (psychrometrics). Which property does the value "{n["raw"]}" '
                                f'(the {ORDINAL[k]} number in the text) state?'}
    questions['asked_first'] = {'type': 'choice', 'criteria': ASKED, 'instructions':
        '`text` is a question about moist air (psychrometrics). Which property does it ask to find? If it asks for several, '
        'choose the first one it mentions. If it asks for all the other properties, choose that.'}
    return {'model': MODEL, 'state': {'text': text}, 'questions': questions}


def run(args):
    rows = [json.loads(l) for l in QUESTIONS.read_text(encoding='utf-8').splitlines()]
    RAW.parent.mkdir(exist_ok=True)
    done = {json.loads(l)['id'] for l in RAW.read_text().splitlines() if json.loads(l).get('ok')} if RAW.exists() else set()
    todo = [r for r in rows if r['id'] not in done][: args.limit or None]
    secret, lock = key(), threading.Lock()

    def one(row):
        rec = {'id': row['id']}
        try:
            response, seconds, attempts = call(payload(row['text']), secret)
            rec.update(ok=True, answers=response.get('answers'), model=response.get('model'), usage=response.get('usage'),
                       seconds=round(seconds, 3), attempts=attempts)
        except RuntimeError as e:
            rec.update(ok=False, error=str(e))
        with lock, RAW.open('a', encoding='utf-8') as f:
            f.write(json.dumps(rec, ensure_ascii=False) + '\n')
        return rec['ok']

    with ThreadPoolExecutor(args.workers) as pool:
        results = [f.result() for f in as_completed([pool.submit(one, r) for r in todo])]
    print(f'{sum(results)} ok, {len(results) - sum(results)} failed, {len(done)} already done')


def pipeline(text, answers):
    nums = plan(text)
    labels = [n['options'][0] if len(n['options']) == 1 else NAME_TO_KEY[answers[f'value_{k + 1}']['choice']] for k, n in enumerate(nums)]
    si = [to_si(p, n['value'], n['unit']) for p, n in zip(labels, nums)]
    first = answers['asked_first']['choice']
    highlight = 'all' if first == ALL else NAME_TO_KEY[first]
    if None in si:
        return labels, highlight, None, 'label does not fit the unit'
    try:
        return labels, highlight, ps.solve((labels[0], si[0]), (labels[1], si[1])), None
    except ValueError as e:
        return labels, highlight, None, str(e)


def score(args):
    rows = {r['id']: r for r in map(json.loads, QUESTIONS.read_text(encoding='utf-8').splitlines())}
    raw = {}
    for line in RAW.read_text(encoding='utf-8').splitlines():
        rec = json.loads(line)
        if rec.get('ok') or rec['id'] not in raw:
            raw[rec['id']] = rec
    items, by = [], defaultdict(Counter)
    for qid, row in rows.items():
        rec = raw.get(qid, {})
        if not rec.get('ok'):
            items.append({'id': qid, 'p1': False, 'p2': False, 'reason': 'no answer', 'text': row['text']})
            continue
        labels, highlight, state, reason = pipeline(row['text'], rec['answers'])
        truth_labels = [g['prop'] for g in row['given']]
        true_first = 'all' if len(row['asked']) == 5 else row['asked'][0]
        p1 = labels == truth_labels
        p2 = state is not None and all(abs(state[p] - row['truth'][p]) <= TOL[p] for p in ps.PROPS)
        jev_labelled = sum(1 for n in plan(row['text']) if len(n['options']) > 1)
        items.append({'id': qid, 'p1': p1, 'p2': p2, 'highlight_ok': highlight == true_first, 'labels': labels,
                      'true_labels': truth_labels, 'highlight': highlight, 'true_first': true_first, 'reason': reason,
                      'jev_labelled': jev_labelled, 'seconds': rec['seconds'], 'tokens': rec['usage']['input_tokens'],
                      'style': row['style'], 'unit': '°F' if row['fahrenheit'] else '°C', 'text': row['text']})
        for dim in ('style', 'unit'):
            by[f'{dim}:{items[-1][dim]}'].update(n=1, p1=p1, p2=p2, highlight=items[-1]['highlight_ok'])
    ok = [i for i in items if 'seconds' in i]
    p1, p2 = sum(i['p1'] for i in items), sum(i['p2'] for i in items)
    summary = {'n': len(items), 'answered': len(ok), 'p1': p1, 'p1_pass': p1 >= PASS, 'p2': p2, 'p2_pass': p2 >= PASS,
               'pass_line': PASS, 'highlight_correct': sum(i.get('highlight_ok', False) for i in items),
               'numbers_labelled_by_jev': sum(i.get('jev_labelled', 0) for i in items),
               'numbers_labelled_by_unit': 2 * len(items) - sum(i.get('jev_labelled', 0) for i in items),
               'seconds_p50': statistics.median(i['seconds'] for i in ok), 'input_tokens_mean': round(statistics.mean(i['tokens'] for i in ok)),
               'usd_total': sum(i['tokens'] for i in ok) * USD_PER_M / 1e6, 'breakdown': {k: dict(v) for k, v in sorted(by.items())}}
    OUT.write_text(json.dumps({'summary': summary, 'failures': [i for i in items if not (i['p1'] and i['p2'])],
                               'highlight_misses': [i for i in items if i.get('highlight_ok') is False]},
                              ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False))
    for i in items:
        if not (i['p1'] and i['p2']):
            print(f"- {i['id']} labels={i.get('labels')} true={i.get('true_labels')} {i.get('reason') or ''}\n    {i['text']}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('command', choices=('run', 'score'))
    ap.add_argument('--workers', type=int, default=8)
    ap.add_argument('--limit', type=int, default=0)
    args = ap.parse_args()
    (run if args.command == 'run' else score)(args)


if __name__ == '__main__':
    main()
