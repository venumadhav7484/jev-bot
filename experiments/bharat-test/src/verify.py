"""Independent re-check of stage 1. Does not import common.py or report.py.

1. Recomputes per-language accuracy from the raw log and the original TSV files.
2. Re-checks every published GPT-4 / GPT-3.5 / XLM-R value against the paper's extracted text.
3. Re-evaluates both pass lines.
"""
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER_TEXT = Path(sys.argv[1]) if len(sys.argv) > 1 else None


def main():
    results = json.loads((ROOT / 'runs/results.json').read_text())
    published = json.loads((ROOT / 'src/published.json').read_text())['scores']
    raw = {}
    for line in open(ROOT / 'runs/stage1_raw.jsonl', encoding='utf-8'):
        r = json.loads(line)
        if r.get('ok') or (r['lang'], r['id']) not in raw:
            raw[(r['lang'], r['id'])] = r
    ok_all = True
    for lang, reported in results['per_language'].items():
        with open(ROOT / 'data' / lang / 'test.tsv', encoding='utf-8', newline='') as f:
            gold = {row['index_id']: row['category'] for row in csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE)}
        correct = sum(1 for i, g in gold.items() if raw.get((lang, i), {}).get('ok') and raw[(lang, i)]['choice'] == g)
        acc = round(100 * correct / len(gold), 1)
        same = acc == reported['accuracy'] and len(gold) == 204
        ok_all &= same
        if not same:
            print(f'MISMATCH {lang}: recomputed {acc} vs reported {reported["accuracy"]}')
    print(f'accuracy recomputed for {len(results["per_language"])} sets:', 'all match' if ok_all else 'MISMATCHES')

    if PAPER_TEXT and PAPER_TEXT.exists():
        text = PAPER_TEXT.read_text(errors='replace')
        bad = 0
        for lang, v in published.items():
            m = re.search(re.escape(lang) + r'.*?Asia 2|' + re.escape(lang) + r'.*?Europe 1', text)
            line = next((l for l in text.splitlines() if lang in l and ('Asia' in l or 'Europe' in l)), '')
            nums = re.findall(r'\d+(?:\.\d+)?', line.split('Asia 2')[-1] if 'Asia 2' in line else line.split('Europe 1')[-1])
            # columns: MLP, XLM-R base, XLM-R, eng, ara, zho, GPT-3.5, GPT-4
            if len(nums) < 8 or float(nums[-1]) != v['gpt4'] or float(nums[-2]) != v['gpt35'] or float(nums[2]) != v['xlmr_supervised']:
                bad += 1
                print(f'PAPER MISMATCH {lang}: {nums} vs {v}')
        print('published values vs paper text:', 'all 25 match' if bad == 0 else f'{bad} mismatches')
        ok_all &= bad == 0

    counted = [l for l, v in published.items() if l != 'eng_Latn' and v['gpt4'] >= 40.0]
    wins = sum(1 for l in counted if results['per_language'][l]['accuracy'] > published[l]['gpt4'])
    top10 = ['hin_Deva', 'ben_Beng', 'mar_Deva', 'tel_Telu', 'tam_Taml', 'guj_Gujr', 'urd_Arab', 'kan_Knda',
             'ory_Orya', 'mal_Mlym']
    mean10 = sum(results['per_language'][l]['accuracy'] for l in top10) / 10
    print(f'P1: {wins} of {len(counted)} (need 14) -> {"PASS" if wins >= 14 else "FAIL"}')
    print(f'P2: mean {mean10:.2f} (need 72.0) -> {"PASS" if mean10 >= 72.0 else "FAIL"}')
    print('ALL CHECKS PASS' if ok_all and wins >= 14 and mean10 >= 72.0 else 'CHECK FAILURES ABOVE')


if __name__ == '__main__':
    main()
