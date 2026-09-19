---
id: almost-certain
title: "Almost Certain: guess the model’s confidence"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Almost Certain: guess the model’s confidence

## What

Browser game invites players to guess model certainty for random descriptions.

## How Jev fits

Uses Jev judgments as game targets; supplied examples contrast juggling two versus three balls. Exact prompt, primitive and scoring implementation require demo inspection.

## Why and impact

A low-stakes way to explore how wording and descriptions affect model judgment. No calibration benchmark is supplied.

## Limits and reuse

Predicting a model value is not validating that value against real outcomes. Treat displayed percentages as model behavior. Screenshot gives3% for a coin explicitly described as55%heads. Follow-up uses explicit0-9 probability bins and selects50-59% with100%confidence. Different schemas, not a controlled repeat; confidence over a bin is distinct from event probability. Preserve both results.

## Sources

- Discord source — private provenance retained locally.
- [https://almost-certain.vercel.app/](https://almost-certain.vercel.app/) — access: `fetched`; review: `source_text_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
