"""Live Jev answers for the public Bharat test page (web/bharat.html).

Each request is one Jev Choice question with the exact instructions and options used in the Bharat test:
7 SIB-200 news topics or 60 MASSIVE voice-assistant intents. Visitor text is never logged or stored, and a
failed call is reported as a failure; it never falls back to a recorded or canned answer.
"""
import json
import time
import urllib.error
import urllib.request
from pathlib import Path

SPEC = json.loads(Path(__file__).with_name('bharat_spec.json').read_text(encoding='utf-8'))
API = 'https://api.typesafe.ai/v1/systemone'
TASKS = ('topic', 'intent')
SHOWN = {'topic': 7, 'intent': 5}  # ranked options returned to the page
RETRYABLE = (429, 500, 502, 503, 504, 529)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args):
        return None


class Unavailable(RuntimeError):
    """Jev did not answer. The message is written for visitors and contains no provider detail."""


def parse(body):
    """Validate a visitor request and return (task, text); raises ValueError."""
    if not isinstance(body, dict):
        raise ValueError('Expected a JSON object.')
    task, text = body.get('task'), body.get('text')
    if task not in TASKS or not isinstance(text, str):
        raise ValueError('Unknown task.')
    text = text.strip()
    if not 1 <= len(text) <= SPEC['max_chars']:
        raise ValueError('Text must be 1 to %d characters.' % SPEC['max_chars'])
    return task, text


def payload(task, text):
    question = SPEC[task]
    return {'model': SPEC['model'], 'state': {'text': text},
            'questions': {task: {'type': 'choice', 'instructions': question['instructions'],
                                 'criteria': question['criteria']}}}


def shape(task, response, seconds):
    """Reduce a Jev response to what the page shows: the choice, ranked options, time and cost."""
    criteria = SPEC[task]['criteria']
    answer = (response.get('answers') or {}).get(task)
    if not isinstance(answer, dict) or answer.get('choice') not in criteria:
        raise Unavailable('Jev returned an answer this page could not read. Please try again.')
    label = (lambda key: criteria[key]) if task == 'intent' else (lambda key: key)
    probs = answer.get('probabilities') or {}
    ranked = sorted(((k, float(v)) for k, v in probs.items() if k in criteria), key=lambda kv: -kv[1])[:SHOWN[task]]
    tokens = (response.get('usage') or {}).get('input_tokens')
    return {'task': task, 'choice': answer['choice'], 'label': label(answer['choice']),
            'confidence': answer.get('confidence'),
            'ranked': [{'key': k, 'label': label(k), 'p': round(p, 4)} for k, p in ranked],
            'seconds': round(seconds, 3), 'input_tokens': tokens if isinstance(tokens, int) else None,
            'usd': tokens * SPEC['usd_per_m_input'] / 1e6 if isinstance(tokens, int) else None,
            'model': response.get('model') or SPEC['model']}


def ask(task, text, key, timeout=8):
    """One live Jev call; one retry on a busy or failing gateway. Raises Unavailable on failure."""
    data = json.dumps(payload(task, text), ensure_ascii=False).encode()
    opener = urllib.request.build_opener(NoRedirect)
    for attempt in range(2):
        request = urllib.request.Request(API, data=data, headers={'Authorization': 'Bearer ' + key,
                                                                  'Content-Type': 'application/json'})
        start = time.perf_counter()
        try:
            with opener.open(request, timeout=timeout) as result:
                response = json.loads(result.read())
            return shape(task, response, time.perf_counter() - start)
        except urllib.error.HTTPError as exc:
            exc.close()
            if exc.code in RETRYABLE and attempt == 0:
                time.sleep(0.8)
                continue
            if exc.code == 403:
                raise Unavailable('Jev declined to answer this text. Try a different sentence.') from None
            raise Unavailable('Jev is busy or unavailable right now. Please try again in a moment.') from None
        except (urllib.error.URLError, TimeoutError, ValueError):
            raise Unavailable('Couldn’t reach Jev. Please try again in a moment.') from None
    raise Unavailable('Jev is busy or unavailable right now. Please try again in a moment.')
