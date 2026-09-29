"""Write video/data.js from runs/results.json and real test sentences, so every on-screen number is measured."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from common import load_split  # noqa: E402

results = json.loads((ROOT / 'runs' / 'results.json').read_text())
per = results['per_language']
raw = {}
for line in open(ROOT / 'runs' / 'stage1_raw.jsonl', encoding='utf-8'):
    r = json.loads(line)
    raw[(r['lang'], r['id'])] = r

NATIVE = {'hin_Deva': 'हिन्दी', 'ben_Beng': 'বাংলা', 'mar_Deva': 'मराठी', 'tel_Telu': 'తెలుగు', 'tam_Taml': 'தமிழ்',
          'guj_Gujr': 'ગુજરાતી', 'urd_Arab': 'اردو', 'kan_Knda': 'ಕನ್ನಡ', 'ory_Orya': 'ଓଡ଼ିଆ', 'mal_Mlym': 'മലയാളം',
          'pan_Guru': 'ਪੰਜਾਬੀ', 'asm_Beng': 'অসমীয়া'}
ROWS = ['tel_Telu', 'guj_Gujr', 'pan_Guru', 'mar_Deva', 'urd_Arab', 'hin_Deva', 'ory_Orya', 'tam_Taml', 'ben_Beng',
        'kan_Knda', 'mal_Mlym', 'asm_Beng']
# One real sentence per card: (language, SIB index_id). All were answered correctly with confidence >= 0.9.
CARDS = [('tel_Telu', '11'), ('hin_Deva', '1097'), ('tam_Taml', '558'), ('ben_Beng', '1161'), ('guj_Gujr', '1221'),
         ('kan_Knda', '818')]

cards = []
for lang, idx in CARDS:
    text = next(r['text'] for r in load_split(lang) if r['index_id'] == idx)
    rec = raw[(lang, idx)]
    assert rec['ok'] and rec['choice'] == rec['gold'], (lang, idx)
    cards.append({'lang': per[lang]['name'], 'text': text, 'topic': rec['choice'],
                  'confidence': rec['confidence'], 'seconds': rec['seconds']})

s = results['summary']


def half_up(x, places=1):
    from decimal import ROUND_HALF_UP, Decimal
    return float(Decimal(str(x)).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP))


data = {
    'rows': [{'native': NATIVE[l], 'name': per[l]['name'], 'jev': per[l]['accuracy'], 'gpt4': per[l]['gpt4']}
             for l in ROWS],
    'cards': cards,
    'stats': {'beats': s['beats_gpt4_all_24'], 'of': 24, 'jev10': half_up(s['most_spoken_mean_jev']),
              'gpt10': half_up(s['most_spoken_mean_gpt4']), 'sentences': s['requests_ok'],
              'usd': half_up(s['total_usd'], 2), 'p50': s['seconds_p50'],
              'santali': per['sat_Olck']['accuracy']},
    'english': {'jev': per['eng_Latn']['accuracy'], 'gpt4': per['eng_Latn']['gpt4']},
}
# Stage 2 (MASSIVE voice requests): measured Jev vs published XLM-R trained on English only / on each language.
s2 = json.loads((ROOT / 'runs' / 'results_stage2.json').read_text())
spec = json.loads((ROOT / 'src' / 'intents.json').read_text())
VNATIVE = {'hi-IN': ('हिन्दी', 'Hindi'), 'ml-IN': ('മലയാളം', 'Malayalam'), 'te-IN': ('తెలుగు', 'Telugu'),
           'kn-IN': ('ಕನ್ನಡ', 'Kannada'), 'ur-PK': ('اردو', 'Urdu'), 'bn-BD': ('বাংলা', 'Bengali'),
           'ta-IN': ('தமிழ்', 'Tamil')}
vrows = sorted(((loc, v) for loc, v in s2['per_locale'].items() if loc != 'en-US'), key=lambda kv: -kv[1]['accuracy'])
raw2 = {}
for line in open(ROOT / 'runs' / 'stage2_raw.jsonl', encoding='utf-8'):
    r = json.loads(line)
    raw2[(r['locale'], r['id'])] = r
utts = {}
for line in open(ROOT / 'data' / 'massive' / '1.1' / 'data' / 'te-IN.jsonl', encoding='utf-8'):
    r = json.loads(line)
    utts[r['id']] = r['utt']
# (MASSIVE id, English translation shown to the viewer)
VEX = [('4313', 'Will it rain in Hyderabad tomorrow?'), ('12121', 'Book me a taxi to Guntur in half an hour')]
vexamples = []
for vid, gloss in VEX:
    rec = raw2[('te-IN', vid)]
    assert rec['ok'] and rec['choice'] == rec['gold'], vid
    vexamples.append({'text': utts[vid], 'gloss': gloss, 'intent': spec['intents'][rec['choice']],
                      'confidence': rec['confidence']})
data['voice'] = {
    'rows': [{'native': VNATIVE[loc][0], 'name': VNATIVE[loc][1], 'jev': v['accuracy'], 'zero': v['xlmr_zero'],
              'full': v['xlmr_full']} for loc, v in vrows],
    'examples': vexamples,
    'stats': {'jev': half_up(s2['summary']['indian_mean_jev']), 'zero': half_up(s2['summary']['indian_mean_xlmr_zero']),
              'full': half_up(s2['summary']['indian_mean_xlmr_full']), 'n': s2['summary']['requests_ok']},
}

# Stage 3: Jev vs today's models (same 5,100 requests), and the conclusion drawn from it.
s3 = json.loads((ROOT / 'runs' / 'results_stage3.json').read_text())
M = {m['model']: m for m in s3['models']}
names = [('Jev', 'Jev'), ('gpt-6-astra', 'gpt-6-astra'), ('glm-5.3', 'GLM 5.3')]
data['rivals'] = {
    'subtitle': 'Same 5,100 requests and instructions, zero-shot · 30 Sep 2026',
    'models': [{'name': label, 'acc': half_up(M[k]['most_spoken_mean']), 'usd': M[k]['usd_per_1000'],
                'sec': M[k]['seconds_p50']} for k, label in names],
    'maxUsd': max(M[k]['usd_per_1000'] for k, _ in names), 'maxSec': max(M[k]['seconds_p50'] for k, _ in names),
}
jv, gp = M['Jev'], M['gpt-6-astra']
data['conclusion'] = {
    'points': [f'Big Indian languages: a half-second model matched today\'s flagship, '
               f'<b>{half_up(jv["most_spoken_mean"])}%</b> vs {half_up(gp["most_spoken_mean"])}%.',
               f'At about <b>1/{gp["cost_ratio_vs_jev"]:.0f}th</b> of the cost and <b>{gp["speed_ratio_vs_jev"]:.0f}×</b> faster.',
               f'Rare scripts still need big models: Santali {half_up(jv["per_language"]["sat_Olck"])}% vs '
               f'{half_up(gp["per_language"]["sat_Olck"])}%.'],
    'footnote': ('Narrow tasks: topic tagging and intent routing. GPT-4 = gpt-4-0613 as published in the SIB-200 paper '
                 '(different prompts). Public benchmarks, so training overlap can\'t be ruled out. Jev jev-1.13.0, '
                 'gpt-6-astra and GLM 5.3, zero-shot, 29–30 Sep 2026. Data: SIB-200 (CC BY-SA 4.0), MASSIVE (CC BY 4.0).'),
}

(ROOT / 'video' / 'data.js').write_text('window.DATA = ' + json.dumps(data, ensure_ascii=False, indent=1) + ';\n',
                                        encoding='utf-8')
print(json.dumps(data['stats']), len(cards), 'cards', len(data['rows']), 'rows')
