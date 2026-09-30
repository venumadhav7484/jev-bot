"""Live Jev reading of psychrometric questions for the public /psychro-data page.

The same pipeline as pilot v2 (experiments/psychrometric-charts/PLAN.md). Code finds the two numbers and their units.
Units narrow each number's options, and Jev picks the property for each remaining number plus the property to
highlight. The page then computes all seven properties exactly in the browser; Jev does no arithmetic. Visitor
text is never logged or stored, and a failed call is reported as a failure, never replaced by a guess.
"""
import json
import re
import time
import urllib.error
import urllib.request

API = 'https://api.typesafe.ai/v1/systemone'
MODEL = 'jev-1.13.0'
USD_PER_M_INPUT = 0.042
MAX_CHARS = 300
RETRYABLE = (429, 500, 502, 503, 504, 529)

PROPS = ('tdb', 'twb', 'tdp', 'rh', 'w', 'h', 'v')
PROPERTIES = {  # identical to the pilot (run_pilot.PROPERTIES)
    'tdb': ('dry-bulb temperature', 'Dry-bulb temperature: the ordinary air temperature'),
    'twb': ('wet-bulb temperature', 'Wet-bulb temperature: the temperature read by a thermometer with a wet wick'),
    'tdp': ('dew-point temperature', 'Dew-point temperature: the temperature at which moisture in the air starts to condense'),
    'rh': ('relative humidity', 'Relative humidity: water vapour as a percentage of saturation'),
    'w': ('humidity ratio', 'Humidity ratio or moisture content: mass of water vapour per mass of dry air'),
    'h': ('specific enthalpy', 'Specific enthalpy: heat content of the air per mass of dry air'),
    'v': ('specific volume', 'Specific volume: volume of the air per mass of dry air'),
}
NAME_TO_KEY = {name: key for key, (name, _) in PROPERTIES.items()}
TEMPS = ('tdb', 'twb', 'tdp')
BY_UNIT = {'°C': TEMPS, 'C': TEMPS, 'degrees': TEMPS, '°F': TEMPS, 'F': TEMPS, 'degrees F': TEMPS,
           '%': ('rh',), 'g/kg': ('w',), 'kJ/kg': ('h',), 'm³/kg': ('v',), '': PROPS}
ALL = 'all other properties'
ASKED = {**{name: desc for name, desc in PROPERTIES.values()}, ALL: 'All other properties: the text asks for every remaining property'}
ORDINAL = ('first', 'second')
NUMBER = re.compile(r'(?<![\w.])(-?\d+(?:\.\d+)?)\s?(°F|°C|degrees F|degrees|F|C|%|g/kg|kJ/kg|m³/kg)?(?![\w/])')


class Unavailable(RuntimeError):
    """Jev did not answer. The message is written for visitors and contains no provider detail."""


def extract(text):
    """Every number with the unit written right after it (the pilot's parser)."""
    text = text.replace('m3/kg', 'm³/kg').replace('m^3/kg', 'm³/kg')
    return [{'raw': m.group(0).strip(), 'value': float(m.group(1)), 'unit': m.group(2) or ''} for m in NUMBER.finditer(text)]


def parse(body):
    """Validate a visitor request and return (text, numbers); raises ValueError with a visitor-facing message."""
    if not isinstance(body, dict) or not isinstance(body.get('text'), str):
        raise ValueError('Type a question with two values.')
    text = body['text'].strip()
    if not 3 <= len(text) <= MAX_CHARS:
        raise ValueError('Type a question of up to 300 characters with two values.')
    numbers = extract(text)
    if len(numbers) != 2:
        raise ValueError('Give exactly two values, for example “DB 30 °C, WB 22 °C — dew point?”. '
                         f'This question has {len(numbers)}.')
    return text.replace('m3/kg', 'm³/kg').replace('m^3/kg', 'm³/kg'), numbers


def payload(text, numbers):
    questions = {}
    for k, n in enumerate(numbers):
        options = BY_UNIT[n['unit']]
        if len(options) > 1:
            questions[f'value_{k + 1}'] = {'type': 'choice', 'criteria': {PROPERTIES[p][0]: PROPERTIES[p][1] for p in options},
                'instructions': f'`text` is a question about moist air (psychrometrics). Which property does the value "{n["raw"]}" '
                                f'(the {ORDINAL[k]} number in the text) state?'}
    questions['asked_first'] = {'type': 'choice', 'criteria': ASKED, 'instructions':
        '`text` is a question about moist air (psychrometrics). Which property does it ask to find? If it asks for several, '
        'choose the first one it mentions. If it asks for all the other properties, choose that.'}
    return {'model': MODEL, 'state': {'text': text}, 'questions': questions}


def shape(response, numbers, seconds):
    answers = response.get('answers') or {}
    out = []
    for k, n in enumerate(numbers):
        options = BY_UNIT[n['unit']]
        item = {**n, 'options': list(options)}
        if len(options) == 1:
            item.update(label=options[0], source='unit')
        else:
            a = answers.get(f'value_{k + 1}') or {}
            if a.get('choice') not in NAME_TO_KEY:
                raise Unavailable('Jev returned an answer this page could not read. Please try again.')
            item.update(label=NAME_TO_KEY[a['choice']], source='jev', confidence=a.get('confidence'),
                        probabilities={NAME_TO_KEY[c]: round(float(p), 4) for c, p in (a.get('probabilities') or {}).items() if c in NAME_TO_KEY})
        out.append(item)
    first = (answers.get('asked_first') or {}).get('choice')
    if first not in ASKED:
        raise Unavailable('Jev returned an answer this page could not read. Please try again.')
    tokens = (response.get('usage') or {}).get('input_tokens')
    return {'numbers': out, 'highlight': 'all' if first == ALL else NAME_TO_KEY[first],
            'highlight_confidence': answers['asked_first'].get('confidence'), 'seconds': round(seconds, 3),
            'input_tokens': tokens if isinstance(tokens, int) else None,
            'usd': tokens * USD_PER_M_INPUT / 1e6 if isinstance(tokens, int) else None, 'model': response.get('model') or MODEL}


def ask(text, numbers, key, timeout=8):
    """One live Jev call; one retry on a busy or failing gateway. Raises Unavailable on failure."""
    data = json.dumps(payload(text, numbers), ensure_ascii=False).encode()
    opener = urllib.request.build_opener(_NoRedirect)
    for attempt in range(2):
        request = urllib.request.Request(API, data=data, headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'})
        start = time.perf_counter()
        try:
            with opener.open(request, timeout=timeout) as result:
                response = json.loads(result.read())
            return shape(response, numbers, time.perf_counter() - start)
        except urllib.error.HTTPError as exc:
            exc.close()
            if exc.code in RETRYABLE and attempt == 0:
                time.sleep(0.8)
                continue
            if exc.code == 403:
                raise Unavailable('Jev declined to answer this text. Try rephrasing.') from None
            raise Unavailable('Jev is busy or unavailable right now. Please try again in a moment.') from None
        except (urllib.error.URLError, TimeoutError, ValueError):
            raise Unavailable('Couldn’t reach Jev. Please try again in a moment.') from None
    raise Unavailable('Jev is busy or unavailable right now. Please try again in a moment.')


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args):
        return None


# ---------- Uploaded charts: Jev reads the chart's OCR text (the image never leaves the visitor's browser) ----------
CHART_MAX_CHARS = 3000
UNITS = {'SI units': 'SI units: temperatures in °C, humidity ratio in g/kg or kg/kg, enthalpy in kJ/kg',
         'IP units': 'IP (US) units: temperatures in °F, humidity ratio in grains/lb or lb/lb, enthalpy in Btu/lb'}
KINDS = {'psychrometric chart': 'A psychrometric chart: dry-bulb temperature along the bottom axis, humidity ratio up the side',
         'Mollier diagram': 'A Mollier h-x diagram: humidity ratio along the horizontal axis, temperature up the side',
         'not a psychrometric chart': 'Some other chart, diagram or picture'}


def parse_chart(body):
    """OCR text of an uploaded chart; raises ValueError with a visitor-facing message."""
    text = body.get('chart_text') if isinstance(body, dict) else None
    if not isinstance(text, str) or not 3 <= len(text.strip()) <= CHART_MAX_CHARS:
        raise ValueError('Couldn’t read enough text on this chart. Try a clearer image.')
    return ' '.join(text.split())


def chart_payload(text):
    prefix = '`text` is the text an OCR engine read from an uploaded image; it may be noisy or out of order. '
    return {'model': MODEL, 'state': {'text': text}, 'questions': {
        'kind': {'type': 'choice', 'criteria': KINDS, 'instructions': prefix + 'What kind of chart is it?'},
        'units': {'type': 'choice', 'criteria': UNITS, 'instructions': prefix + 'Which unit system does the chart use?'}}}


def ask_chart(text, key, timeout=8):
    data = json.dumps(chart_payload(text), ensure_ascii=False).encode()
    opener = urllib.request.build_opener(_NoRedirect)
    for attempt in range(2):
        request = urllib.request.Request(API, data=data, headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'})
        start = time.perf_counter()
        try:
            with opener.open(request, timeout=timeout) as result:
                response = json.loads(result.read())
            answers = response.get('answers') or {}
            kind, units = (answers.get('kind') or {}), (answers.get('units') or {})
            if kind.get('choice') not in KINDS or units.get('choice') not in UNITS:
                raise Unavailable('Jev returned an answer this page could not read. Please try again.')
            tokens = (response.get('usage') or {}).get('input_tokens')
            return {'kind': kind['choice'], 'kind_confidence': kind.get('confidence'), 'units': units['choice'],
                    'units_confidence': units.get('confidence'), 'seconds': round(time.perf_counter() - start, 3),
                    'input_tokens': tokens if isinstance(tokens, int) else None,
                    'usd': tokens * USD_PER_M_INPUT / 1e6 if isinstance(tokens, int) else None, 'model': response.get('model') or MODEL}
        except urllib.error.HTTPError as exc:
            exc.close()
            if exc.code in RETRYABLE and attempt == 0:
                time.sleep(0.8)
                continue
            raise Unavailable('Jev is busy or unavailable right now. Please try again in a moment.') from None
        except (urllib.error.URLError, TimeoutError, ValueError):
            raise Unavailable('Couldn’t reach Jev. Please try again in a moment.') from None
    raise Unavailable('Jev is busy or unavailable right now. Please try again in a moment.')
