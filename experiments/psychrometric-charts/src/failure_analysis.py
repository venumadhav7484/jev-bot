"""What went wrong in pilot v2's misses, and how wrong the answers were.

For every question the pipeline got wrong: what Jev read and with what confidence, then what the pipeline returned.
The return is either a refusal (the misread values describe no possible air) or a state, and for a state the absolute
error of each property against the truth. Also reports the error when the reading was right, which should be zero:
the maths is exact.

Usage: python failure_analysis.py  -> runs/failure_analysis.json
"""
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import psychro as ps
from pilot_v2 import QUESTIONS, RAW, pipeline

HERE = Path(__file__).resolve().parents[1]
UNITS = {'tdb': ('°C', 1), 'twb': ('°C', 1), 'tdp': ('°C', 1), 'rh': ('% RH', 100), 'w': ('g/kg', 1000), 'h': ('kJ/kg', 1), 'v': ('m³/kg', 1)}
NAMES = {'tdb': 'dry-bulb', 'twb': 'wet-bulb', 'tdp': 'dew point', 'rh': 'relative humidity', 'w': 'humidity ratio', 'h': 'enthalpy', 'v': 'specific volume'}


def main():
    rows = {r['id']: r for r in map(json.loads, QUESTIONS.read_text(encoding='utf-8').splitlines())}
    raw = {}
    for line in RAW.read_text(encoding='utf-8').splitlines():
        rec = json.loads(line)
        if rec.get('ok'):
            raw[rec['id']] = rec
    misses, exact_max = [], 0.0
    for qid, row in rows.items():
        answers = raw[qid]['answers']
        labels, _, state, reason = pipeline(row['text'], answers)
        truth = row['truth']
        true_labels = [g['prop'] for g in row['given']]
        if labels == true_labels and state:
            exact_max = max(exact_max, max(abs(state[p] - truth[p]) * UNITS[p][1] for p in ('tdb', 'twb', 'tdp')))
            continue
        wrong = [(k, labels[k], true_labels[k]) for k in (0, 1) if labels[k] != true_labels[k]]
        conf = [answers.get(f'value_{k + 1}', {}).get('confidence') for k, *_ in wrong]
        item = {'id': qid, 'text': row['text'], 'style': row['style'],
                'misread': [f'“{row["given"][k]["raw"]}” read as {NAMES[got]} (it was {NAMES[want]})' for k, got, want in wrong],
                'confidence': conf, 'asked': row['asked']}
        if state is None:
            item.update(outcome='refused', why=reason)
        else:
            err = {p: abs(state[p] - truth[p]) * UNITS[p][1] for p in ps.PROPS}
            asked_err = {p: round(err[p], 3) for p in row['asked']}
            item.update(outcome='wrong answer', abs_error_asked=asked_err, abs_error_all={p: round(v, 3) for p, v in err.items()},
                        units={p: UNITS[p][0] for p in ps.PROPS})
        misses.append(item)
    out = {'n': len(rows), 'misses': len(misses), 'refused': sum(m['outcome'] == 'refused' for m in misses),
           'wrong_answers': sum(m['outcome'] == 'wrong answer' for m in misses),
           'max_error_when_read_right_C': exact_max, 'items': misses}
    (HERE / 'runs/failure_analysis.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: v for k, v in out.items() if k != 'items'}))
    for m in misses:
        print('-', m['id'], m['style'], '|', m['text'], '|', '; '.join(m['misread']), '| conf', m['confidence'], '|', m['outcome'],
              m.get('abs_error_asked') or m.get('why'))


if __name__ == '__main__':
    main()
