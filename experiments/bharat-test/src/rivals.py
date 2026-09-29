"""Stage 3: the same SIB-200 sentences, instructions and topics sent to current general-purpose models.

Providers: glm (Z.ai), openai, gemini. Keys come from environment variables or a local .env (OPENAI_API_KEY, glm_key), and are never printed. Output: runs/rival_<provider>.jsonl (resumable). A reply that names no single
topic counts as wrong.

Usage: python rivals.py glm [--model glm-5.3] [--dev N | --langs a,b] [--workers 6]
"""
import argparse
import os
import json
import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from common import (ENGLISH, INDIAN, MOST_SPOKEN, ROOT, RUNS, TOPICS, ApiError, _env_file, append_jsonl, load_split,
                    post_json, read_jsonl)

PROMPT = ('Which topic best describes the sentence below? The sentence may be written in any language or script; '
          'judge its meaning.\n\nTopics:\n' + '\n'.join(f'- {k}: {v}' for k, v in TOPICS.items())
          + '\n\nSentence: {text}\n\nAnswer with exactly one topic name from the list and nothing else.')
DEFAULT_MODEL = {'glm': 'glm-5.3', 'openai': 'gpt-6-astra', 'gemini': 'gemini-3.1-pro-preview'}
# Standard list prices, USD per 1M tokens, from the official pricing pages checked 30 Sep 2026.
PRICES = {'glm-5.3': (1.40, 4.40), 'gpt-6-astra': (10.00, 50.00), 'gemini-3.1-pro-preview': (2.00, 12.00)}


def key_for(provider):
    name = {'glm': 'glm_key', 'openai': 'OPENAI_API_KEY', 'gemini': 'GEMINI_API_KEY'}[provider]
    return os.environ.get(name) or _env_file(ROOT / '.env').get(name)


def parse_topic(reply):
    text = reply.strip().lower()
    found = [t for t in TOPICS if t in text]
    if len(found) == 1:
        return found[0]
    exact = [t for t in TOPICS if re.fullmatch(r'\W*' + re.escape(t) + r'\W*', text)]
    return exact[0] if len(exact) == 1 else None


def call(provider, model, key, text):
    prompt = PROMPT.format(text=text)
    if provider == 'glm':
        body = {'model': model, 'stream': False, 'max_tokens': 1024, 'temperature': 0.0, 'reasoning_effort': 'low',
                'messages': [{'role': 'user', 'content': prompt}]}
        resp, secs, attempts = post_json('https://api.z.ai/api/paas/v4/chat/completions', body, key, timeout=120)
        u = resp.get('usage', {})
        return resp['choices'][0]['message'].get('content') or '', u.get('prompt_tokens', 0), u.get('completion_tokens', 0), secs
    if provider == 'openai':
        body = {'model': model, 'input': prompt, 'reasoning': {'effort': 'low'}}
        resp, secs, attempts = post_json('https://api.openai.com/v1/responses', body, key, timeout=120)
        out = ''.join(c.get('text', '') for item in resp.get('output', []) if item.get('type') == 'message'
                      for c in item.get('content', []))
        u = resp.get('usage', {})
        return out, u.get('input_tokens', 0), u.get('output_tokens', 0), secs
    if provider == 'gemini':
        raise NotImplementedError('gemini adapter is added once the key is present and the request shape is checked')
    raise ValueError(provider)


def run_one(provider, model, key, lang, row):
    rec = {'lang': lang, 'id': row['index_id'], 'gold': row['category'], 'model': model}
    try:
        reply, tin, tout, secs = call(provider, model, key, row['text'])
        rec.update(ok=True, reply=reply[:200], choice=parse_topic(reply), input_tokens=tin, output_tokens=tout,
                   seconds=round(secs, 3))
    except ApiError as e:
        rec.update(ok=False, error=f'HTTP {e.status}', detail=e.detail[:200])
    except Exception as e:
        rec.update(ok=False, error=type(e).__name__, detail=str(e)[:200])
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('provider', choices=['glm', 'openai', 'gemini'])
    ap.add_argument('--model', default='')
    ap.add_argument('--dev', type=int, default=0)
    ap.add_argument('--langs', default='')
    ap.add_argument('--workers', type=int, default=6)
    args = ap.parse_args()
    model = args.model or DEFAULT_MODEL[args.provider]
    key = key_for(args.provider)
    if not key:
        raise SystemExit(f'No key for {args.provider}.')
    langs = args.langs.split(',') if args.langs else [ENGLISH] + MOST_SPOKEN
    out = RUNS / (f'rival_{args.provider}_dev.jsonl' if args.dev else f'rival_{args.provider}.jsonl')
    done = {(r['lang'], r['id']) for r in read_jsonl(out) if r.get('ok')}
    todo = []
    for lang in langs:
        rows = load_split(lang, 'dev' if args.dev else 'test')
        rows = rows[:args.dev] if args.dev else rows
        todo += [(lang, r) for r in rows if (lang, r['index_id']) not in done]
    print(f'{args.provider}/{model}: {len(done)} done, {len(todo)} to run -> {out.name}')
    lock, n, bad = threading.Lock(), 0, 0
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for f in as_completed([pool.submit(run_one, args.provider, model, key, l, r) for l, r in todo]):
            rec = f.result()
            with lock:
                append_jsonl(out, rec)
                n += 1
                bad += 0 if rec['ok'] else 1
                if n % 250 == 0 or not rec['ok']:
                    print(f'{n}/{len(todo)} finished, {bad} failed' + ('' if rec['ok'] else f' ({rec["error"]} {rec.get("detail", "")[:100]})'))
                if not rec['ok'] and ('1113' in rec.get('detail', '') or 'insufficient' in rec.get('detail', '').lower()):
                    print('Billing/balance error: stopping.')
                    pool.shutdown(cancel_futures=True)
                    break
    rows = [r for r in read_jsonl(out) if r.get('ok')]
    if rows:
        pin, pout = PRICES.get(model, (None, None))
        tin = sum(r['input_tokens'] for r in rows) / len(rows)
        tout = sum(r['output_tokens'] for r in rows) / len(rows)
        acc = sum(r['choice'] == r['gold'] for r in rows) / len(rows)
        secs = sorted(r['seconds'] for r in rows)
        usd1k = (tin * pin + tout * pout) / 1e6 * 1000 if pin is not None else None
        print(json.dumps({'ok': len(rows), 'accuracy': round(acc, 3), 'avg_input_tokens': round(tin, 1),
                          'avg_output_tokens': round(tout, 1), 'usd_per_1000': usd1k and round(usd1k, 3),
                          'seconds_p50': secs[len(secs) // 2], 'unparsed': sum(r['choice'] is None for r in rows)}))


if __name__ == '__main__':
    main()
