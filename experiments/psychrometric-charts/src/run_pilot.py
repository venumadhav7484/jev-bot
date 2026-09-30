"""Send each pilot question to Jev once (PLAN.md arm A). Resumable; only transport failures are retried.

Usage: python run_pilot.py [--workers 8] [--limit N]
Key: JEV_API_KEY, or jev_api_key in the repository's local .env.local (never committed).
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
from pathlib import Path
import threading
import time
import urllib.error
import urllib.request

HERE = Path(__file__).resolve().parents[1]
API, MODEL = 'https://api.typesafe.ai/v1/systemone', 'jev-1.13.0'
QUESTIONS, RAW = HERE / 'data/pilot_questions.jsonl', HERE / 'runs/pilot_raw.jsonl'

# Frozen before the run (PLAN.md). Keys are what Jev returns; descriptions guide it.
PROPERTIES = {
    'tdb': ('dry-bulb temperature', 'Dry-bulb temperature: the ordinary air temperature'),
    'twb': ('wet-bulb temperature', 'Wet-bulb temperature: the temperature read by a thermometer with a wet wick'),
    'tdp': ('dew-point temperature', 'Dew-point temperature: the temperature at which moisture in the air starts to condense'),
    'rh': ('relative humidity', 'Relative humidity: water vapour as a percentage of saturation'),
    'w': ('humidity ratio', 'Humidity ratio or moisture content: mass of water vapour per mass of dry air'),
    'h': ('specific enthalpy', 'Specific enthalpy: heat content of the air per mass of dry air'),
    'v': ('specific volume', 'Specific volume: volume of the air per mass of dry air'),
}
CRITERIA = {name: desc for name, desc in PROPERTIES.values()}
ORDINAL = ('first', 'second')


def payload(text, raws):
    questions = {f'value_{k + 1}': {'type': 'choice', 'criteria': CRITERIA, 'instructions':
                 f'`text` is a question about moist air (psychrometrics). Which property does the value "{raw}" '
                 f'(the {ORDINAL[k]} number in the text) state?'} for k, raw in enumerate(raws)}
    for key, (name, _) in PROPERTIES.items():
        questions[f'asked_{key}'] = {'type': 'noul', 'instructions':
            f'Does `text` ask for the {name} to be found? Count a request for all the other properties as asking for it. '
            f'A value that the text already states is not being asked for.'}
    return {'model': MODEL, 'state': {'text': text}, 'questions': questions}


def key():
    if os.environ.get('JEV_API_KEY'):
        return os.environ['JEV_API_KEY']
    env = HERE.parents[1] / '.env.local'
    for line in env.read_text().splitlines() if env.exists() else []:
        if line.startswith('jev_api_key='):
            return line.split('=', 1)[1].strip().strip('"\'')
    raise SystemExit('No Jev key: set JEV_API_KEY')


def call(body, secret, attempts=5):
    data = json.dumps(body, ensure_ascii=False).encode()
    for attempt in range(1, attempts + 1):
        req = urllib.request.Request(API, data=data, headers={'Authorization': 'Bearer ' + secret, 'Content-Type': 'application/json'})
        start = time.perf_counter()
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read()), time.perf_counter() - start, attempt
        except urllib.error.HTTPError as e:
            e.close()
            if e.code not in (408, 429, 500, 502, 503, 504, 529) or attempt == attempts:
                raise RuntimeError(f'HTTP {e.code}') from None
        except (urllib.error.URLError, TimeoutError):
            if attempt == attempts:
                raise RuntimeError('network') from None
        time.sleep(min(30, 2 ** attempt))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--workers', type=int, default=8)
    ap.add_argument('--limit', type=int, default=0)
    args = ap.parse_args()
    import sys
    sys.path.insert(0, str(HERE / 'src'))
    from questions import extract
    rows = [json.loads(l) for l in QUESTIONS.read_text(encoding='utf-8').splitlines()]
    RAW.parent.mkdir(exist_ok=True)
    done = {json.loads(l)['id'] for l in RAW.read_text().splitlines() if json.loads(l).get('ok')} if RAW.exists() else set()
    todo = [r for r in rows if r['id'] not in done][: args.limit or None]
    secret, lock = key(), threading.Lock()

    def one(row):
        raws = [f['raw'] for f in extract(row['text'])]
        rec = {'id': row['id']}
        try:
            response, seconds, attempts = call(payload(row['text'], raws), secret)
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


if __name__ == '__main__':
    main()
