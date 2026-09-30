"""Confirm-step test (PLAN.md, fourth section): v2's pipeline on 600 fresh questions, plus a confirmation flag on any
Jev reading below 0.75 confidence. The threshold is frozen from the v2 analysis.

Usage:
  python pilot_v3.py run [--workers 8]   -> runs/pilot3_raw.jsonl (resumable; transport retries only)
  python pilot_v3.py score               -> runs/pilot3_results.json
"""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from pathlib import Path
import statistics
import sys
import threading

sys.path.insert(0, str(Path(__file__).resolve().parent))
import psychro as ps
from pilot_v2 import NAME_TO_KEY, pipeline, plan, payload
from run_pilot import call, key
from score_pilot import TOL, USD_PER_M

HERE = Path(__file__).resolve().parents[1]
QUESTIONS, RAW, OUT = HERE / 'data/pilot3_questions.jsonl', HERE / 'runs/pilot3_raw.jsonl', HERE / 'runs/pilot3_results.json'
THRESHOLD = 0.75
LINES = {'C1_recall': 0.90, 'C2_burden': 0.10, 'C3_silent': 0.01}
UNIT = {'tdb': 1, 'twb': 1, 'tdp': 1, 'rh': 100, 'w': 1000, 'h': 1, 'v': 1}


def run(args):
    rows = [json.loads(l) for l in QUESTIONS.read_text(encoding='utf-8').splitlines()]
    RAW.parent.mkdir(exist_ok=True)
    done = {json.loads(l)['id'] for l in RAW.read_text().splitlines() if json.loads(l).get('ok')} if RAW.exists() else set()
    todo, secret, lock = [r for r in rows if r['id'] not in done], key(), threading.Lock()

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


def score(args):
    rows = {r['id']: r for r in map(json.loads, QUESTIONS.read_text(encoding='utf-8').splitlines())}
    raw = {}
    for line in RAW.read_text(encoding='utf-8').splitlines():
        rec = json.loads(line)
        if rec.get('ok') or rec['id'] not in raw:
            raw[rec['id']] = rec
    missing = [q for q in rows if not raw.get(q, {}).get('ok')]
    right_flagged = right_total = mis_flagged = 0
    misreads, silent, per_style, p1 = [], [], Counter(), 0
    p2 = 0
    for qid, row in rows.items():
        rec = raw.get(qid, {})
        if not rec.get('ok'):
            continue
        answers, truth_labels = rec['answers'], [g['prop'] for g in row['given']]
        labels, _, state, reason = pipeline(row['text'], answers)
        flagged_q = False
        for k, n in enumerate(plan(row['text'])):
            if len(n['options']) == 1:
                continue
            a = answers[f'value_{k + 1}']
            ok, flag = NAME_TO_KEY[a['choice']] == truth_labels[k], a['confidence'] < THRESHOLD
            flagged_q |= flag
            if ok:
                right_total += 1; right_flagged += flag
            else:
                mis_flagged += flag
                misreads.append({'id': qid, 'style': row['style'], 'text': row['text'], 'value': n['raw'], 'read_as': NAME_TO_KEY[a['choice']],
                                 'was': truth_labels[k], 'confidence': a['confidence'], 'flagged': flag})
        correct = state is not None and all(abs(state[p] - row['truth'][p]) <= TOL[p] for p in ps.PROPS)
        p1 += labels == truth_labels; p2 += correct
        per_style[row['style'] + (':ok' if correct else ':miss')] += 1
        if not correct and state is not None and not flagged_q:   # a wrong answer shown with no confirmation prompt
            silent.append({'id': qid, 'text': row['text'], 'abs_error': {p: round(abs(state[p] - row['truth'][p]) * UNIT[p], 3) for p in row['asked']}})
    n_ok = len(rows) - len(missing)
    c1 = mis_flagged / len(misreads) if misreads else None
    c2 = right_flagged / right_total
    c3 = len(silent) / n_ok
    summary = {'n': len(rows), 'answered': n_ok, 'missing': missing, 'threshold': THRESHOLD,
               'jev_labelled_numbers': right_total + len(misreads), 'misreads': len(misreads), 'misreads_flagged': mis_flagged,
               'correct_flagged': right_flagged, 'correct_total': right_total, 'silent_wrong_answers': len(silent),
               'C1_recall': c1, 'C1_pass': c1 is not None and c1 >= LINES['C1_recall'],
               'C2_burden': c2, 'C2_pass': c2 <= LINES['C2_burden'], 'C3_silent': c3, 'C3_pass': c3 <= LINES['C3_silent'],
               'p1': p1, 'p2': p2, 'by_style': dict(per_style),
               'misreads_by_style': dict(Counter(m['style'] for m in misreads)),
               'seconds_p50': statistics.median(raw[q]['seconds'] for q in rows if raw.get(q, {}).get('ok')),
               'usd_total': sum(raw[q]['usage']['input_tokens'] for q in rows if raw.get(q, {}).get('ok')) * USD_PER_M / 1e6}
    OUT.write_text(json.dumps({'summary': summary, 'misreads': misreads, 'silent': silent}, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False))
    for m in misreads:
        print(f"- {m['id']} {m['style']} “{m['value']}” read as {m['read_as']} (was {m['was']}) conf {m['confidence']} flagged={m['flagged']} | {m['text']}")
    for s in silent:
        print('  SILENT', s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('command', choices=('run', 'score'))
    ap.add_argument('--workers', type=int, default=8)
    args = ap.parse_args()
    (run if args.command == 'run' else score)(args)


if __name__ == '__main__':
    main()
