"""Shared pieces for the Bharat test: languages, data loading, Jev client and topic question.

Keys come from environment variables or a local, git-ignored .env; never printed.
"""
import csv
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
RUNS = ROOT / 'runs'

JEV_API = 'https://api.typesafe.ai/v1/systemone'
JEV_MODEL = 'jev-1.13.0'
JEV_USD_PER_M_INPUT = 0.042

ENGLISH = 'eng_Latn'
INDIAN = ['asm_Beng', 'awa_Deva', 'ben_Beng', 'bho_Deva', 'guj_Gujr', 'hin_Deva', 'hne_Deva', 'kan_Knda',
          'kas_Arab', 'kas_Deva', 'mag_Deva', 'mai_Deva', 'mal_Mlym', 'mar_Deva', 'mni_Beng', 'npi_Deva',
          'ory_Orya', 'pan_Guru', 'san_Deva', 'sat_Olck', 'snd_Arab', 'tam_Taml', 'tel_Telu', 'urd_Arab']
MOST_SPOKEN = ['hin_Deva', 'ben_Beng', 'mar_Deva', 'tel_Telu', 'tam_Taml', 'guj_Gujr', 'urd_Arab', 'kan_Knda',
               'ory_Orya', 'mal_Mlym']
NAMES = {'eng_Latn': 'English', 'asm_Beng': 'Assamese', 'awa_Deva': 'Awadhi', 'ben_Beng': 'Bengali',
         'bho_Deva': 'Bhojpuri', 'guj_Gujr': 'Gujarati', 'hin_Deva': 'Hindi', 'hne_Deva': 'Chhattisgarhi',
         'kan_Knda': 'Kannada', 'kas_Arab': 'Kashmiri (Arabic)', 'kas_Deva': 'Kashmiri (Devanagari)',
         'mag_Deva': 'Magahi', 'mai_Deva': 'Maithili', 'mal_Mlym': 'Malayalam', 'mar_Deva': 'Marathi',
         'mni_Beng': 'Meitei (Bengali script)', 'npi_Deva': 'Nepali', 'ory_Orya': 'Odia', 'pan_Guru': 'Punjabi',
         'san_Deva': 'Sanskrit', 'sat_Olck': 'Santali (Ol Chiki)', 'snd_Arab': 'Sindhi', 'tam_Taml': 'Tamil',
         'tel_Telu': 'Telugu', 'urd_Arab': 'Urdu'}

TOPICS = {
    'science/technology': 'Science and technology: research, discoveries, computing, space, the natural sciences',
    'travel': 'Travel and tourism: trips, visiting places, getting around, advice for travellers',
    'politics': 'Politics and government: elections, leaders, laws, policy, international relations, conflict',
    'sports': 'Sports: games, athletes, teams, competitions and results',
    'health': 'Health and medicine: illness, the body, treatment, nutrition, wellbeing',
    'entertainment': 'Entertainment and culture: music, film, television, the arts, festivals, celebrities',
    'geography': 'Geography: places, landforms, climate, oceans, countries and their physical features',
}
INSTRUCTIONS = ('Which topic best describes the sentence in `text`? The sentence may be written in any '
                'language or script; judge its meaning.')


def load_split(lang, split='test'):
    with open(DATA / lang / f'{split}.tsv', encoding='utf-8', newline='') as f:
        rows = list(csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE))
    labels = (DATA / lang / 'labels.txt').read_text(encoding='utf-8').split()
    assert set(r['category'] for r in rows) <= set(labels) == set(TOPICS), lang
    return rows


def payload(text):
    return {'model': JEV_MODEL, 'state': {'text': text},
            'questions': {'topic': {'type': 'choice', 'instructions': INSTRUCTIONS, 'criteria': TOPICS}}}


def parse(response):
    answer = (response.get('answers') or {}).get('topic')
    if not isinstance(answer, dict) or answer.get('choice') not in TOPICS:
        raise ValueError('missing or unknown choice')
    probs = answer.get('probabilities') or {}
    if set(probs) != set(TOPICS):
        raise ValueError('incomplete probabilities')
    return answer['choice'], {k: float(v) for k, v in probs.items()}, answer.get('confidence')


def read_jsonl(path):
    path = Path(path)
    if not path.exists():
        return []
    with open(path, encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]


def append_jsonl(path, row):
    with open(path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(row, ensure_ascii=False) + '\n')


def latest(rows, key):
    out = {}
    for r in rows:
        if r.get('ok') or key(r) not in out:
            out[key(r)] = r
    return out


def _env_file(path):
    values = {}
    if Path(path).exists():
        for line in Path(path).read_text().splitlines():
            if '=' in line and not line.lstrip().startswith('#'):
                name, value = line.split('=', 1)
                values[name.strip()] = value.strip().strip('"').strip("'")
    return values


def jev_key():
    key = os.environ.get('JEV_API_KEY') or _env_file(ROOT / '.env').get('JEV_API_KEY')
    if not key:
        raise SystemExit('Set JEV_API_KEY in the environment or in a local .env file (git-ignored).')
    return key


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class ApiError(RuntimeError):
    def __init__(self, status, detail):
        super().__init__(f'HTTP {status}')
        self.status, self.detail = status, detail


RETRYABLE = {408, 429, 500, 502, 503, 504, 529}


def post_json(url, body, key, timeout=60, attempts=5):
    """POST with bounded exponential backoff. Returns (json, seconds, attempts)."""
    data = json.dumps(body).encode()
    opener = urllib.request.build_opener(NoRedirect)
    for attempt in range(1, attempts + 1):
        req = urllib.request.Request(url, data=data, headers={
            'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'})
        start = time.perf_counter()
        try:
            with opener.open(req, timeout=timeout) as response:
                result = json.loads(response.read())
            return result, time.perf_counter() - start, attempt
        except urllib.error.HTTPError as error:
            detail = error.read()[:300].decode('utf-8', 'replace')
            if error.code not in RETRYABLE or attempt == attempts:
                raise ApiError(error.code, detail) from None
        except (urllib.error.URLError, TimeoutError, ConnectionError):
            if attempt == attempts:
                raise
        time.sleep(min(30, 2 ** attempt))
    raise RuntimeError('unreachable')
