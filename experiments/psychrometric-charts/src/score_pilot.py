"""Score the pilot against PLAN.md: P1 (both numbers labelled right) and P2 (final answer correct).

Usage: python score_pilot.py  -> runs/pilot_results.json and a printed summary.
"""
from collections import Counter, defaultdict
import json
from pathlib import Path
import statistics
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import psychro as ps
from questions import extract
from run_pilot import PROPERTIES, QUESTIONS, RAW

HERE = Path(__file__).resolve().parents[1]
NAME_TO_KEY = {name: key for key, (name, _) in PROPERTIES.items()}
TOL = {'tdb': 0.2, 'twb': 0.2, 'tdp': 0.2, 'rh': 0.01, 'w': 0.0002, 'h': 0.5, 'v': 0.002}
PASS = 194
USD_PER_M = 0.042


def to_si(prop, value, unit):
    """Unit conversion driven by Jev's label. None when the label does not fit the unit (a pipeline failure)."""
    if prop in ('tdb', 'twb', 'tdp'):
        if unit in ('°C', 'C', 'degrees', ''):
            return value
        if unit in ('°F', 'F', 'degrees F'):
            return (value - 32) / 1.8
        return None
    if prop == 'rh':
        return value / 100 if unit in ('%', '') else None
    if prop == 'w':
        return value / 1000 if unit == 'g/kg' else None
    if prop == 'h':
        return value if unit == 'kJ/kg' else None
    return value if unit == 'm³/kg' else None


def pipeline(row, answers):
    """What the deployed pipeline would return: (labels, asked set, state or None, failure reason)."""
    nums = extract(row['text'])
    labels = [NAME_TO_KEY[answers[f'value_{k}']['choice']] for k in (1, 2)]
    asked = {p for p in ps.PROPS if answers[f'asked_{p}']['noul'] >= 0.5} - set(labels)
    si = [to_si(p, n['value'], n['unit']) for p, n in zip(labels, nums)]
    if None in si:
        return labels, asked, None, 'label does not fit the unit'
    try:
        return labels, asked, ps.solve((labels[0], si[0]), (labels[1], si[1])), None
    except ValueError as e:
        return labels, asked, None, str(e)


def main():
    rows = {r['id']: r for r in map(json.loads, QUESTIONS.read_text(encoding='utf-8').splitlines())}
    raw = {}
    for line in RAW.read_text(encoding='utf-8').splitlines():
        rec = json.loads(line)
        if rec.get('ok') or rec['id'] not in raw:
            raw[rec['id']] = rec
    missing = [i for i in rows if not raw.get(i, {}).get('ok')]
    items, by = [], defaultdict(Counter)
    for qid, row in rows.items():
        rec = raw.get(qid, {})
        if not rec.get('ok'):
            items.append({'id': qid, 'p1': False, 'p2': False, 'reason': 'no answer'})
            continue
        labels, asked, state, reason = pipeline(row, rec['answers'])
        true_labels = [g['prop'] for g in row['given']]
        p1 = labels == true_labels
        asked_ok = asked == set(row['asked'])
        values_ok = state is not None and all(abs(state[p] - row['truth'][p]) <= TOL[p] for p in row['asked'])
        p2 = asked_ok and values_ok
        conf = [rec['answers'][f'value_{k}'].get('confidence') for k in (1, 2)]
        items.append({'id': qid, 'p1': p1, 'p2': p2, 'asked_ok': asked_ok, 'labels': labels, 'true_labels': true_labels,
                      'asked': sorted(asked), 'true_asked': row['asked'], 'reason': reason, 'confidence': conf,
                      'seconds': rec['seconds'], 'tokens': rec['usage']['input_tokens'], 'text': row['text'], 'style': row['style'],
                      'fahrenheit': row['fahrenheit'], 'pair': '+'.join(sorted(true_labels))})
        for dim in ('style', 'pair'):
            by[dim + ':' + items[-1][dim]]['n'] += 1
            by[dim + ':' + items[-1][dim]]['p1'] += p1
            by[dim + ':' + items[-1][dim]]['p2'] += p2
        by['unit:' + ('°F' if row['fahrenheit'] else '°C')]['n'] += 1
        by['unit:' + ('°F' if row['fahrenheit'] else '°C')]['p1'] += p1
        by['unit:' + ('°F' if row['fahrenheit'] else '°C')]['p2'] += p2
    ok = [i for i in items if 'seconds' in i]
    p1, p2 = sum(i['p1'] for i in items), sum(i['p2'] for i in items)
    wrong_conf = [c for i in ok if not i['p1'] for c, l, t in zip(i['confidence'], i['labels'], i['true_labels']) if l != t]
    summary = {'n': len(items), 'answered': len(ok), 'missing': missing,
               'p1': p1, 'p1_pass': p1 >= PASS, 'p2': p2, 'p2_pass': p2 >= PASS, 'pass_line': PASS,
               'asked_set_correct': sum(i.get('asked_ok', False) for i in items),
               'seconds_p50': statistics.median(i['seconds'] for i in ok) if ok else None,
               'input_tokens_mean': round(statistics.mean(i['tokens'] for i in ok)) if ok else None,
               'usd_total': sum(i['tokens'] for i in ok) * USD_PER_M / 1e6,
               'confidence_on_wrong_labels': wrong_conf,
               'breakdown': {k: dict(v) for k, v in sorted(by.items())}}
    out = HERE / 'runs/pilot_results.json'
    out.write_text(json.dumps({'summary': summary, 'failures': [i for i in items if not (i['p1'] and i['p2'])]},
                              ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: v for k, v in summary.items() if k != 'breakdown'}, ensure_ascii=False))
    for i in items:
        if not (i['p1'] and i['p2']):
            print(f"- {i['id']} p1={i['p1']} p2={i['p2']} labels={i.get('labels')} true={i.get('true_labels')} "
                  f"asked={i.get('asked')} true_asked={i.get('true_asked')} {i.get('reason') or ''}\n    {i.get('text', '')}")


if __name__ == '__main__':
    main()
