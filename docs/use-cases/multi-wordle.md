---
id: multi-wordle
title: "Parallel Wordle boards"
category: games
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Parallel Wordle boards

## What

Choose shared guesses across 32 hidden-word boards.

## How Jev fits

Jev chooses informative guesses; deterministic candidate elimination finishes boards once only one answer remains.

## Why and impact

The author reports seven model calls, 35 guesses, 5.4 seconds and $0.00068 estimated API cost.

## Limits and reuse

Video reaches 32/32 solved in 35 guesses with seven model calls; later guesses need no Jev call because host has unique candidates. Solve timing differs from replay animation. One run cannot establish seed-averaged solve rate; deterministic elimination contributes materially.

## Sources

- Discord source — private provenance retained locally.
- [https://x.com/richardcsuwandi/status/2100603807894053252?s=20](https://x.com/richardcsuwandi/status/2100603807894053252?s=20) — access: `fetched`; review: `demo_trace_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
