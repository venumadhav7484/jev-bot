---
id: wordle-strategies
title: "Wordle: action-space design comparison"
category: games
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Wordle: action-space design comparison

## What

Compare ways of framing word selection.

## How Jev fits

The author tests letter-by-letter decisions, five letters together and whole-word choices.

## Why and impact

Letter-level strategies behaved greedily or repeated SEEEE; whole-word selection reportedly solved in three guesses.

## Limits and reuse

One experiment illustrates representation sensitivity, not a universal solving guarantee. Source review: Independent questions cannot coordinate letters into a coherent word. Whole valid candidates plus deterministic clue filtering are the supported pattern; no general win-rate claim.

## Sources

- Discord source — private provenance retained locally.
- [https://x.com/sid19arya0/status/2100679099723223341?s=20](https://x.com/sid19arya0/status/2100679099723223341?s=20) — access: `fetched`; review: `demo_trace_reviewed`.
- [https://t.co/7L6t4B6K7X](https://t.co/7L6t4B6K7X) — access: `fetched`; review: `source_text_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
