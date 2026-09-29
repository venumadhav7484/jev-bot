"""Independent re-check of stage 2 (does not import report2.py): accuracies from raw log + original MASSIVE files,
and the published XLM-R numbers against the paper's extracted Table 8 text."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER_TEXT = Path(sys.argv[1]) if len(sys.argv) > 1 else None


def main():
    res = json.loads((ROOT / 'runs/results_stage2.json').read_text())
    raw = {}
    for line in open(ROOT / 'runs/stage2_raw.jsonl', encoding='utf-8'):
        r = json.loads(line)
        if r.get('ok') or (r['locale'], r['id']) not in raw:
            raw[(r['locale'], r['id'])] = r
    ok_all = True
    for loc, v in res['per_locale'].items():
        gold = {}
        for line in open(ROOT / 'data/massive/1.1/data' / f'{loc}.jsonl', encoding='utf-8'):
            r = json.loads(line)
            if r['partition'] == 'test':
                gold[r['id']] = r['intent']
        correct = sum(1 for i, g in gold.items() if raw.get((loc, i), {}).get('ok') and raw[(loc, i)]['choice'] == g)
        acc = round(100 * correct / len(gold), 1)
        same = acc == v['accuracy'] and len(gold) == 2974
        ok_all &= same
        print(f'{"OK " if same else "MISMATCH"} {loc}: recomputed {acc} vs {v["accuracy"]} (n={len(gold)})')
    if PAPER_TEXT and PAPER_TEXT.exists():
        text = PAPER_TEXT.read_text(errors='replace')
        start = text.index('Intent Accuracy (%)')
        table = text[start:text.index('Table 8', start)]
        spec = json.loads((ROOT / 'src/intents.json').read_text())['published_xlmr_base']
        for loc, v in spec.items():
            if loc == 'source':
                continue
            line = next(l for l in table.splitlines() if l.strip().startswith(loc))
            nums = [float(x) for x in re.findall(r'(\d+\.\d) ±', line)]
            full_ok = nums[2] == v['full']
            zero_ok = v.get('zero') is None or nums[5] == v['zero']
            ok_all &= full_ok and zero_ok
            print(f'{"OK " if full_ok and zero_ok else "MISMATCH"} published {loc}: {nums} vs {v}')
    indian = [l for l in res['per_locale'] if l != 'en-US']
    wins = sum(1 for l in indian if res['per_locale'][l]['accuracy'] > res['per_locale'][l]['xlmr_zero'])
    print(f'P3: {wins} of {len(indian)} (need 5) -> {"PASS" if wins >= 5 else "FAIL"}')
    print('ALL CHECKS PASS' if ok_all else 'CHECK FAILURES ABOVE')


if __name__ == '__main__':
    main()
