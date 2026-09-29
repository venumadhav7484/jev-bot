"""Stage 2 (MASSIVE) metrics and pass/fail: Jev beats XLM-R zero-shot in >= 5 of 7 Indian locales."""
import json
import statistics

from common import JEV_USD_PER_M_INPUT, ROOT, RUNS, latest, read_jsonl
from run_stage2 import LOCALES, load

PASS_NEEDED = 5


def main():
    spec = json.loads((ROOT / 'src' / 'intents.json').read_text())['published_xlmr_base']
    raw = latest(read_jsonl(RUNS / 'stage2_raw.jsonl'), lambda r: (r['locale'], r['id']))
    per = {}
    for loc in LOCALES:
        rows = load(loc)
        recs = [raw.get((loc, r['id'])) for r in rows]
        ok = [r for r in recs if r and r.get('ok')]
        correct = sum(1 for r in ok if r['choice'] == r['gold'])
        per[loc] = {'n': len(rows), 'ok': len(ok), 'failed': len(rows) - len(ok),
                    'accuracy': round(100 * correct / len(rows), 1),
                    'xlmr_zero': spec[loc].get('zero'), 'xlmr_full': spec[loc].get('full'),
                    'avg_input_tokens': round(statistics.mean(r['usage']['input_tokens'] for r in ok), 1) if ok else None}
        z = per[loc]['xlmr_zero']
        per[loc]['beats_xlmr_zero'] = z is not None and per[loc]['accuracy'] > z
    indian = [l for l in LOCALES if l != 'en-US']
    wins = [l for l in indian if per[l]['beats_xlmr_zero']]
    all_ok = [r for r in raw.values() if r.get('ok')]
    tokens = sum(r['usage'].get('input_tokens', 0) for r in all_ok)
    secs = sorted(r['seconds'] for r in all_ok)
    results = {'per_locale': per,
               'summary': {'requests_ok': len(all_ok), 'requests_failed': sum(v['failed'] for v in per.values()),
                           'wins_vs_xlmr_zero': len(wins), 'of': len(indian),
                           'indian_mean_jev': round(statistics.mean(per[l]['accuracy'] for l in indian), 2),
                           'indian_mean_xlmr_zero': round(statistics.mean(per[l]['xlmr_zero'] for l in indian), 2),
                           'indian_mean_xlmr_full': round(statistics.mean(per[l]['xlmr_full'] for l in indian), 2),
                           'total_input_tokens': tokens, 'total_usd': round(tokens * JEV_USD_PER_M_INPUT / 1e6, 4),
                           'seconds_p50': secs[len(secs) // 2] if secs else None},
               'pass': {'P3_beats_xlmr_zero_in_5_of_7': len(wins) >= PASS_NEEDED}}
    (RUNS / 'results_stage2.json').write_text(json.dumps(results, indent=2))
    print(f'{"locale":8} {"Jev":>6} {"XLM-R zero":>11} {"XLM-R full":>11}')
    for loc, v in per.items():
        print(f'{loc:8} {v["accuracy"]:6.1f} {str(v["xlmr_zero"]):>11} {str(v["xlmr_full"]):>11} {"win" if v["beats_xlmr_zero"] else ""}')
    print(json.dumps({'summary': results['summary'], 'pass': results['pass']}, indent=2))


if __name__ == '__main__':
    main()
