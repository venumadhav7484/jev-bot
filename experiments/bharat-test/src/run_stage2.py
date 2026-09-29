"""Stage 2: MASSIVE intent routing, one Jev Choice (60 intents) per utterance. Separate experiment. Resumable.

Usage: python run_stage2.py [--dev N] [--locales en-US,hi-IN] [--workers 8]
"""
import argparse
import json
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from common import DATA, JEV_API, JEV_MODEL, ROOT, RUNS, ApiError, append_jsonl, jev_key, post_json, read_jsonl

LOCALES = ['en-US', 'hi-IN', 'te-IN', 'ta-IN', 'kn-IN', 'ml-IN', 'bn-BD', 'ur-PK']
SPEC = json.loads((ROOT / 'src' / 'intents.json').read_text())


def load(locale, partition='test'):
    with open(DATA / 'massive' / '1.1' / 'data' / f'{locale}.jsonl', encoding='utf-8') as f:
        return [r for r in map(json.loads, f) if r['partition'] == partition]


def body(text):
    return {'model': JEV_MODEL, 'state': {'text': text},
            'questions': {'intent': {'type': 'choice', 'instructions': SPEC['instructions'],
                                     'criteria': SPEC['intents']}}}


def run_one(key, locale, row):
    record = {'locale': locale, 'id': row['id'], 'gold': row['intent']}
    try:
        response, seconds, attempts = post_json(JEV_API, body(row['utt']), key, timeout=60)
        answer = response['answers']['intent']
        if answer.get('choice') not in SPEC['intents']:
            raise ValueError('unknown intent')
        top = sorted(answer.get('probabilities', {}).items(), key=lambda kv: -kv[1])[:3]
        record.update(ok=True, choice=answer['choice'], confidence=answer.get('confidence'), top3=top,
                      model=response.get('model'), seconds=round(seconds, 3), attempts=attempts,
                      usage=response.get('usage', {}))
    except ApiError as error:
        record.update(ok=False, error=f'HTTP {error.status}', detail=error.detail[:200])
    except Exception as error:
        record.update(ok=False, error=type(error).__name__, detail=str(error)[:200])
    return record


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dev', type=int, default=0)
    ap.add_argument('--locales', default='')
    ap.add_argument('--workers', type=int, default=8)
    args = ap.parse_args()
    locales = args.locales.split(',') if args.locales else LOCALES
    out = RUNS / ('stage2_dev.jsonl' if args.dev else 'stage2_raw.jsonl')
    done = {(r['locale'], r['id']) for r in read_jsonl(out) if r.get('ok')}
    todo = []
    for loc in locales:
        rows = load(loc, 'dev' if args.dev else 'test')
        rows = rows[:args.dev] if args.dev else rows
        todo += [(loc, r) for r in rows if (loc, r['id']) not in done]
    print(f'{len(done)} done, {len(todo)} to run -> {out.name}')
    key, lock, finished, failed = jev_key(), threading.Lock(), 0, 0
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for future in as_completed([pool.submit(run_one, key, loc, r) for loc, r in todo]):
            record = future.result()
            with lock:
                append_jsonl(out, record)
                finished += 1
                failed += 0 if record['ok'] else 1
                if finished % 2000 == 0 or not record['ok']:
                    print(f'{finished}/{len(todo)} finished, {failed} failed'
                          + ('' if record['ok'] else f' (last: {record["locale"]} {record["error"]} {record.get("detail", "")[:80]})'))
    print(f'done: {finished} finished, {failed} failed')


if __name__ == '__main__':
    main()
