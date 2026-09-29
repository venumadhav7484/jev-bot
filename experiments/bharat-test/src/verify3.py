"""Independent re-check of stage 3 (does not import report3.py or rivals.py): per-model accuracy on the 10
most-spoken languages and cost per 1,000 sentences, recomputed from raw logs and the original TSV files."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOP10 = ['hin_Deva', 'ben_Beng', 'mar_Deva', 'tel_Telu', 'tam_Taml', 'guj_Gujr', 'urd_Arab', 'kan_Knda', 'ory_Orya',
         'mal_Mlym']
PRICE = {'Jev': (0.042, 0.0), 'gpt-6-astra': (10.0, 50.0), 'glm-5.3': (1.40, 4.40)}
FILES = {'Jev': 'stage1_raw.jsonl', 'gpt-6-astra': 'rival_openai.jsonl', 'glm-5.3': 'rival_glm.jsonl'}


def main():
    reported = {m['model']: m for m in json.loads((ROOT / 'runs/results_stage3.json').read_text())['models']}
    ok_all = True
    for name, fname in FILES.items():
        recs = {}
        for line in open(ROOT / 'runs' / fname, encoding='utf-8'):
            r = json.loads(line)
            if r.get('ok') or (r['lang'], r['id']) not in recs:
                recs[(r['lang'], r['id'])] = r
        accs = []
        for lang in TOP10:
            with open(ROOT / 'data' / lang / 'test.tsv', encoding='utf-8', newline='') as f:
                gold = {row['index_id']: row['category'] for row in csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE)}
            accs.append(round(100 * sum(1 for i, g in gold.items() if recs.get((lang, i), {}).get('ok')
                                        and recs[(lang, i)].get('choice') == g) / len(gold), 1))
        mean10 = round(sum(accs) / 10, 2)
        ok = [r for r in recs.values() if r.get('ok')]
        tin = sum((r.get('usage') or {}).get('input_tokens', r.get('input_tokens', 0)) for r in ok)
        tout = 0 if name == 'Jev' else sum(r.get('output_tokens', 0) for r in ok)
        usd1k = round((tin * PRICE[name][0] + tout * PRICE[name][1]) / 1e6 / len(ok) * 1000, 4)
        good = abs(mean10 - reported[name]['most_spoken_mean']) < 0.01 and abs(usd1k - reported[name]['usd_per_1000']) < 0.0001
        ok_all &= good
        print(f'{"OK " if good else "MISMATCH"} {name}: top-10 mean {mean10} vs {reported[name]["most_spoken_mean"]}; '
              f'$/1000 {usd1k} vs {reported[name]["usd_per_1000"]}; requests ok {len(ok)}')
    print('ALL CHECKS PASS' if ok_all else 'CHECK FAILURES ABOVE')


if __name__ == '__main__':
    main()
