"""Stage 1 metrics and pass/fail against PLAN.md section 5. Writes runs/results.json."""
import json
import statistics

from common import (ENGLISH, INDIAN, JEV_USD_PER_M_INPUT, MOST_SPOKEN, NAMES, ROOT, RUNS, latest, load_split,
                    read_jsonl)

P1_MIN_GPT4 = 40.0
P1_NEEDED = 14
P2_MIN_MEAN = 72.0


def main():
    published = json.loads((ROOT / 'src' / 'published.json').read_text())['scores']
    raw = latest(read_jsonl(RUNS / 'stage1_raw.jsonl'), lambda r: (r['lang'], r['id']))
    per_lang = {}
    for lang in [ENGLISH] + INDIAN:
        rows = load_split(lang, 'test')
        recs = [raw.get((lang, r['index_id'])) for r in rows]
        ok = [r for r in recs if r and r.get('ok')]
        correct = sum(1 for r in ok if r['choice'] == r['gold'])
        tokens = [r['usage'].get('input_tokens', 0) for r in ok]
        secs = sorted(r['seconds'] for r in ok)
        per_lang[lang] = {
            'name': NAMES[lang], 'n': len(rows), 'ok': len(ok), 'failed': len(rows) - len(ok),
            'accuracy': round(100 * correct / len(rows), 1),
            'gpt4': published[lang]['gpt4'], 'gpt35': published[lang]['gpt35'],
            'xlmr_supervised': published[lang]['xlmr_supervised'],
            'avg_input_tokens': round(statistics.mean(tokens), 1) if tokens else None,
            'seconds_p50': secs[len(secs) // 2] if secs else None,
        }
    eng_tokens = per_lang[ENGLISH]['avg_input_tokens']
    for lang in per_lang:
        t = per_lang[lang]['avg_input_tokens']
        per_lang[lang]['token_ratio_vs_english'] = round(t / eng_tokens, 2) if t and eng_tokens else None
        per_lang[lang]['beats_gpt4'] = per_lang[lang]['accuracy'] > per_lang[lang]['gpt4']

    p1_set = [l for l in INDIAN if published[l]['gpt4'] >= P1_MIN_GPT4]
    p1_wins = [l for l in p1_set if per_lang[l]['beats_gpt4']]
    p2_mean = round(statistics.mean(per_lang[l]['accuracy'] for l in MOST_SPOKEN), 2)
    gpt4_mean = round(statistics.mean(published[l]['gpt4'] for l in MOST_SPOKEN), 2)
    all_ok = [r for r in raw.values() if r.get('ok')]
    total_tokens = sum(r['usage'].get('input_tokens', 0) for r in all_ok)
    secs = sorted(r['seconds'] for r in all_ok)
    results = {
        'per_language': per_lang,
        'summary': {
            'requests_ok': len(all_ok), 'requests_failed': sum(v['failed'] for v in per_lang.values()),
            'jev_models': sorted({r.get('model') for r in all_ok}),
            'english_accuracy': per_lang[ENGLISH]['accuracy'],
            'p1_languages_counted': len(p1_set), 'p1_wins': len(p1_wins),
            'p1_losses': [l for l in p1_set if l not in p1_wins],
            'beats_gpt4_all_24': sum(per_lang[l]['beats_gpt4'] for l in INDIAN),
            'most_spoken_mean_jev': p2_mean, 'most_spoken_mean_gpt4': gpt4_mean,
            'indian_mean_jev': round(statistics.mean(per_lang[l]['accuracy'] for l in INDIAN), 2),
            'indian_mean_gpt4': round(statistics.mean(published[l]['gpt4'] for l in INDIAN), 2),
            'total_input_tokens': total_tokens,
            'total_usd': round(total_tokens * JEV_USD_PER_M_INPUT / 1e6, 4),
            'seconds_p50': secs[len(secs) // 2] if secs else None,
            'seconds_p95': secs[int(0.95 * len(secs))] if secs else None,
        },
        'pass': {'P1_beats_gpt4_in_14_of_21': len(p1_wins) >= P1_NEEDED,
                 'P2_most_spoken_mean_at_least_72': p2_mean >= P2_MIN_MEAN},
    }
    (RUNS / 'results.json').write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(f'{"language":24} {"Jev":>6} {"GPT-4":>6} {"win":>4} {"tokens x":>8}')
    for lang, v in sorted(per_lang.items(), key=lambda kv: -kv[1]['accuracy']):
        print(f'{v["name"]:24} {v["accuracy"]:6.1f} {v["gpt4"]:6.1f} {"yes" if v["beats_gpt4"] else "":>4} '
              f'{v["token_ratio_vs_english"] or 0:8.2f}')
    print(json.dumps({'summary': results['summary'], 'pass': results['pass']}, indent=2))


if __name__ == '__main__':
    main()
