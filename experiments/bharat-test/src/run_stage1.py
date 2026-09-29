"""Stage 1: one Jev Choice request per SIB-200 sentence, English plus 24 Indian-language sets. Resumable.

Usage: python run_stage1.py [--dev N] [--langs eng_Latn,hin_Deva] [--workers 6]
  --dev N  runs the first N dev sentences per language into runs/dev.jsonl (smoke test only)
"""
import argparse
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from common import (ENGLISH, INDIAN, JEV_API, RUNS, ApiError, append_jsonl, jev_key, load_split, parse, payload,
                    post_json, read_jsonl)


def run_one(key, lang, row):
    record = {'lang': lang, 'id': row['index_id'], 'gold': row['category']}
    try:
        response, seconds, attempts = post_json(JEV_API, payload(row['text']), key, timeout=60)
        choice, probs, confidence = parse(response)
        record.update(ok=True, choice=choice, probs=probs, confidence=confidence, model=response.get('model'),
                      seconds=round(seconds, 3), attempts=attempts, usage=response.get('usage', {}))
    except ApiError as error:
        record.update(ok=False, error=f'HTTP {error.status}', detail=error.detail[:200])
    except Exception as error:
        record.update(ok=False, error=type(error).__name__, detail=str(error)[:200])
    return record


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dev', type=int, default=0)
    ap.add_argument('--langs', default='')
    ap.add_argument('--workers', type=int, default=6)
    args = ap.parse_args()

    langs = args.langs.split(',') if args.langs else [ENGLISH] + INDIAN
    split = 'dev' if args.dev else 'test'
    out = RUNS / ('dev.jsonl' if args.dev else 'stage1_raw.jsonl')
    RUNS.mkdir(exist_ok=True)
    done = {(r['lang'], r['id']) for r in read_jsonl(out) if r.get('ok')}
    todo = []
    for lang in langs:
        rows = load_split(lang, split)
        rows = rows[:args.dev] if args.dev else rows
        todo += [(lang, r) for r in rows if (lang, r['index_id']) not in done]
    print(f'{len(done)} done, {len(todo)} to run -> {out.name}')

    key, lock, finished, failed = jev_key(), threading.Lock(), 0, 0
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for future in as_completed([pool.submit(run_one, key, lang, r) for lang, r in todo]):
            record = future.result()
            with lock:
                append_jsonl(out, record)
                finished += 1
                failed += 0 if record['ok'] else 1
                if finished % 500 == 0 or not record['ok']:
                    print(f'{finished}/{len(todo)} finished, {failed} failed'
                          + ('' if record['ok'] else f' (last: {record["lang"]} {record["error"]} {record.get("detail", "")[:80]})'))
    print(f'done: {finished} finished, {failed} failed')


if __name__ == '__main__':
    main()
