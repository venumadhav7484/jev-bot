---
id: jevguess
title: "Jev Guess: character-guessing game"
category: games
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Jev Guess: character-guessing game

## What

A bounded character-guessing demo has a 48-character catalog; its captured page is explicitly in offline fixture mode.

## How Jev fits

The described live mode uses Jev for candidate ranking and next-question selection; ordinary code maintains state, without submitting the secret target.

## Why and impact

A guess counts as a win only after player confirmation.

## Limits and reuse

No AI runs in the captured fixture mode; relative weights and confidence are explicitly not verified truth or game accuracy.

## Sources

- [https://jevguess.susonsapkota.com/](https://jevguess.susonsapkota.com/) — access: `fetched`; review: `source_text_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
