"""Stage 3: Jev vs current models on the same 5,100 SIB-200 test sentences. Writes runs/results_stage3.json.

No pass line (user decision): results are reported as measured. Failed or unparseable replies count as wrong.
"""
import json
import statistics

from common import ENGLISH, INDIAN, JEV_USD_PER_M_INPUT, MOST_SPOKEN, NAMES, RUNS, latest, load_split, read_jsonl
from rivals import PRICES

RIVALS = [('gpt-6-astra', 'openai'), ('glm-5.3', 'glm')]


def summarize(name, recs, price_in, price_out):
    per = {}
    for lang in [ENGLISH] + INDIAN:
        rows = load_split(lang)
        got = [recs.get((lang, r['index_id'])) for r in rows]
        per[lang] = round(100 * sum(1 for g in got if g and g.get('ok') and g.get('choice') == g['gold']) / len(rows), 1)
    ok = [r for r in recs.values() if r.get('ok')]
    tin = sum(r.get('input_tokens', 0) for r in ok)
    tout = sum(r.get('output_tokens', 0) for r in ok)
    secs = sorted(r['seconds'] for r in ok)
    usd = (tin * price_in + tout * price_out) / 1e6
    return {'model': name, 'per_language': per,
            'most_spoken_mean': round(statistics.mean(per[l] for l in MOST_SPOKEN), 2),
            'indian_mean': round(statistics.mean(per[l] for l in INDIAN), 2), 'english': per[ENGLISH],
            'requests_ok': len(ok), 'failed': 5100 - len(ok),
            'unparsed': sum(1 for r in ok if r.get('choice') is None),
            'input_tokens': tin, 'output_tokens': tout, 'usd_total': round(usd, 4),
            'usd_per_1000': round(usd / max(1, len(ok)) * 1000, 4),
            'seconds_p50': secs[len(secs) // 2] if secs else None}


def main():
    jev = latest(read_jsonl(RUNS / 'stage1_raw.jsonl'), lambda r: (r['lang'], r['id']))
    for r in jev.values():
        r['input_tokens'] = r.get('usage', {}).get('input_tokens', 0)
        r['output_tokens'] = 0  # Jev output is free
    models = [summarize('Jev', jev, JEV_USD_PER_M_INPUT, 0.0)]
    for name, provider in RIVALS:
        recs = latest(read_jsonl(RUNS / f'rival_{provider}.jsonl'), lambda r: (r['lang'], r['id']))
        models.append(summarize(name, recs, *PRICES[name]))
    j = models[0]
    for m in models[1:]:
        m['cost_ratio_vs_jev'] = round(m['usd_per_1000'] / j['usd_per_1000'], 1)
        m['speed_ratio_vs_jev'] = round(m['seconds_p50'] / j['seconds_p50'], 1)
        m['wins_vs_jev_24'] = sum(1 for l in INDIAN if m['per_language'][l] > j['per_language'][l])
        m['ties_vs_jev_24'] = sum(1 for l in INDIAN if m['per_language'][l] == j['per_language'][l])
    (RUNS / 'results_stage3.json').write_text(json.dumps({'models': models}, indent=2))
    print(f'{"language":24}' + ''.join(f'{m["model"]:>14}' for m in models))
    for lang in [ENGLISH] + INDIAN:
        print(f'{NAMES[lang]:24}' + ''.join(f'{m["per_language"][lang]:>14.1f}' for m in models))
    for key in ('most_spoken_mean', 'indian_mean', 'english', 'usd_per_1000', 'usd_total', 'seconds_p50', 'failed',
                'unparsed', 'cost_ratio_vs_jev', 'speed_ratio_vs_jev', 'wins_vs_jev_24', 'ties_vs_jev_24'):
        print(f'{key:24}' + ''.join(f'{str(m.get(key, "-")):>14}' for m in models))


if __name__ == '__main__':
    main()
