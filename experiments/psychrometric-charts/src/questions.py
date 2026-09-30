"""Generate the pilot questions (see PLAN.md) and the parser the pipeline uses to pull out numbers and units.

Usage: python questions.py   -> data/pilot_questions.jsonl (fixed seed), after checking the parser on every question.
"""
from itertools import combinations
import json
from pathlib import Path
import random
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import psychro as ps

HERE = Path(__file__).resolve().parents[1]
SEED, N = 20260930, 200
PAIRS = [tuple(sorted(c)) for c in combinations(ps.PROPS, 2)
         if set(c) not in ps.DEPENDENT and set(c) not in ps.ILL_CONDITIONED]
STYLES = ('textbook', 'shorthand', 'chat')

# How each property is named in each style (several variants, picked at random).
NAMES = {
    'textbook': {'tdb': ['dry-bulb temperature', 'dry bulb temperature'], 'twb': ['wet-bulb temperature', 'thermodynamic wet-bulb temperature'],
                 'tdp': ['dew-point temperature', 'dew point'], 'rh': ['relative humidity'],
                 'w': ['humidity ratio', 'moisture content'], 'h': ['specific enthalpy', 'enthalpy'], 'v': ['specific volume']},
    'shorthand': {'tdb': ['DB', 'DBT', 'Tdb'], 'twb': ['WB', 'WBT', 'Twb'], 'tdp': ['DP', 'DPT', 'Tdp'], 'rh': ['RH'],
                  'w': ['W', 'HR'], 'h': ['h', 'H'], 'v': ['v', 'SV']},
    'chat': {'tdb': ['air temperature', 'dry bulb', 'temperature'], 'twb': ['wet bulb', 'wet-bulb reading'],
             'tdp': ['dew point', 'dewpoint'], 'rh': ['humidity', 'relative humidity'],
             'w': ['moisture content', 'humidity ratio'], 'h': ['enthalpy', 'heat content'], 'v': ['specific volume', 'volume per kg of air']},
}


def fmt(prop, si, fahrenheit, style, rng):
    """Value as written in the question, and the SI value it states."""
    if prop in ('tdb', 'twb', 'tdp'):
        whole = style == 'shorthand' or rng.random() < 0.5
        if fahrenheit:
            f = round(si * 1.8 + 32, 0 if whole else 1)
            return f'{f:g}{rng.choice(["°F", " °F", "F"]) if style != "chat" else rng.choice([" °F", " F", " degrees F"])}', (f - 32) / 1.8
        c = round(si, 0 if whole else 1)
        unit = {'textbook': ' °C', 'shorthand': rng.choice(['', 'C', '°C']), 'chat': rng.choice([' °C', ' C', ' degrees'])}[style]
        return f'{c:g}{unit}', c
    if prop == 'rh':
        r = round(si * 100)
        return f'{r}{"" if style == "shorthand" and rng.random() < 0.5 else "%"}', r / 100
    if prop == 'w':
        g = round(si * 1000, 1)
        return f'{g:g} g/kg', g / 1000
    if prop == 'h':
        h = round(si, 1)
        return f'{h:g} kJ/kg', h
    v = round(si, 3)
    return f'{v:.3f} m³/kg', v


def ask_text(asked, style, rng, given):
    names = [rng.choice(NAMES[style][p]) for p in asked]
    if len(asked) == 5:
        return {'textbook': 'Determine all of its other psychrometric properties.',
                'shorthand': 'Rest of the properties?', 'chat': 'can you give me all the other values?'}[style]
    joined = names[0] if len(names) == 1 else f'{names[0]} and {names[1]}'
    return {'textbook': rng.choice([f'Find the {joined}.', f'Determine the {joined}.', f'What is the {joined}?']),
            'shorthand': rng.choice([f'{joined}?', f'Need {joined}.', f'-> {joined}?']),
            'chat': rng.choice([f"what's the {joined}?", f'how do I get the {joined}?', f'can you tell me the {joined}?'])}[style]


def sentence(style, given_parts, asked_text, rng):
    (n1, t1), (n2, t2) = given_parts
    if style == 'textbook':
        return rng.choice([f'Moist air at sea level has a {n1} of {t1} and a {n2} of {t2}. {asked_text}',
                           f'For air at standard atmospheric pressure with a {n1} of {t1} and a {n2} of {t2}: {asked_text}'])
    if style == 'shorthand':
        return rng.choice([f'{n1} {t1}, {n2} {t2}. {asked_text}', f'Site reading {n1} {t1} / {n2} {t2}. {asked_text}',
                           f'{n1} {t1} {n2} {t2} {asked_text}'])
    return rng.choice([f'hey, in the server room the {n1} is {t1} and the {n2} is {t2}, {asked_text}',
                       f'quick one: {n1} {t1} and {n2} {t2} at the AHU inlet, {asked_text}',
                       f'I measured {n1} = {t1} and {n2} = {t2}. {asked_text}'])


NUMBER = re.compile(r'(?<![\w.])(-?\d+(?:\.\d+)?)\s?(°F|°C|degrees F|degrees|F|C|%|g/kg|kJ/kg|m³/kg)?(?![\w/])')


def extract(text):
    """Pipeline parser: every number with the unit written right after it. Knows units, not property names."""
    return [{'raw': m.group(0).strip(), 'value': float(m.group(1)), 'unit': m.group(2) or ''} for m in NUMBER.finditer(text)]


def generate(seed=SEED, n=N):
    rng = random.Random(seed)
    pairs = PAIRS * (n // len(PAIRS) + 1)
    rng.shuffle(pairs)
    out = []
    while len(out) < n:
        i = len(out)
        pair, style, fahrenheit = list(pairs[i]), STYLES[i % 3], rng.random() < 0.25
        rng.shuffle(pair)
        t, rh = rng.uniform(10, 40), rng.uniform(0.20, 0.90)
        base = ps.state(t, ps.w_at(t, 'rh', rh, ps.P_SEA))
        shown = [fmt(p, base[p], fahrenheit, style, rng) for p in pair]
        try:
            truth = ps.solve((pair[0], shown[0][1]), (pair[1], shown[1][1]))
        except ValueError:
            continue
        others = [p for p in ps.PROPS if p not in pair]
        roll = rng.random()
        asked = others if roll >= 0.9 else rng.sample(others, 2 if roll >= 0.6 else 1)
        asked = [p for p in ps.PROPS if p in asked]
        names = [rng.choice(NAMES[style][p]) for p in pair]
        text = sentence(style, [(names[0], shown[0][0]), (names[1], shown[1][0])], ask_text(asked, style, rng, pair), rng)
        found = extract(text)
        if [f['raw'] for f in found] != [shown[0][0].strip(), shown[1][0].strip()]:
            raise SystemExit(f'parser mismatch on question {i}: {text!r} -> {found}')
        out.append({'id': f'q{i:03d}', 'text': text, 'style': style, 'fahrenheit': fahrenheit,
                    'given': [{'prop': p, 'raw': s[0].strip(), 'si': s[1]} for p, s in zip(pair, shown)],
                    'asked': asked, 'truth': truth})
    return out


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--seed', type=int, default=SEED)
    ap.add_argument('--out', default='pilot_questions.jsonl')
    ap.add_argument('--n', type=int, default=N)
    args = ap.parse_args()
    rows = generate(args.seed, args.n)
    path = HERE / 'data' / args.out
    path.parent.mkdir(exist_ok=True)
    path.write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows), encoding='utf-8')
    from collections import Counter
    print(f'{len(rows)} questions; parser matched all. styles {dict(Counter(r["style"] for r in rows))}; '
          f'°F {sum(r["fahrenheit"] for r in rows)}; asked sizes {dict(Counter(len(r["asked"]) for r in rows))}; '
          f'pairs {len(Counter(tuple(sorted(g["prop"] for g in r["given"])) for r in rows))}')


if __name__ == '__main__':
    main()
