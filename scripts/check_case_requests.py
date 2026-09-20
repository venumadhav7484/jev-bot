"""Exercise prebuilt teaching requests; receipts stay private, never benchmarks.

Resumes by payload hash. Does not execute any suggested application action.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
from case_designs import CACHE, ROOT, read_current
from jev_triage import api_key, evaluate

WORK = ROOT / 'research/case-designs/request-checks'


def check(ident, index, payload, expected, key):
    fingerprint = hashlib.sha256(json.dumps(payload, ensure_ascii=False).encode()).hexdigest()
    path = WORK / (fingerprint + '.json')
    if path.exists():
        saved = json.loads(path.read_text())
    else:
        try:
            response = evaluate(payload, key)
            saved = {'request_hash': fingerprint, 'response': response, 'status': 'complete'}
        except (RuntimeError, ValueError, KeyError) as error:
            saved = {'request_hash': fingerprint, 'status': 'failed', 'error': str(error)}
        path.write_text(json.dumps(saved, indent=2)); path.chmod(0o600)
    actual = saved.get('response', {}).get('answers', {}).get('decision', {}).get('choice')
    return {'id': ident, 'example': index, 'expected': expected, 'actual': actual,
            'status': saved['status'], 'matches': expected == actual, 'request_hash': fingerprint}


def main():
    rows = json.loads((ROOT / 'docs/bot-cases.json').read_text())
    WORK.mkdir(parents=True, exist_ok=True)
    tasks = []
    key = api_key()
    with ThreadPoolExecutor(max_workers=4) as pool:
        for row in rows:
            saved = read_current(row)
            if not saved:
                continue
            design = saved['blueprint']
            for i, example in enumerate(design['examples']):
                payload = {**design['request'], 'state': example['state']}
                tasks.append(pool.submit(check, row['id'], i, payload, example['output']['decision'], key))
        results = [future.result() for future in as_completed(tasks)]
    (WORK / 'summary.json').write_text(json.dumps(results, indent=2))
    print(json.dumps({'requests': len(results), 'matches': sum(r['matches'] for r in results),
                      'failed': sum(r['status'] != 'complete' for r in results),
                      'differences': [r for r in results if not r['matches']]}, indent=2))


if __name__ == '__main__': main()
