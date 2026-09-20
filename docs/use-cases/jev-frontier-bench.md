---
id: jev-frontier-bench
title: "Four-dataset typed-decision comparison"
category: quality
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Four-dataset typed-decision comparison

## What

A public benchmark compares Jev with five LLMs on 200 decisions.

## How Jev fits

Fifty items each cover intent routing, grounded yes/no, star rating and ambiguous entailment. The repository reports prompts, hosts, raw responses and item hashes; Jev uses native typed questions.

## Why and impact

Author reports 72.5% aggregate accuracy for Jev, 94% on BoolQ, and lower per-decision cost/latency in this run.

## Limits and reuse

Confident errors matter: 18 of 55 errors had top probability at least 0.9. On ambiguous human labels, reported distribution agreement was worse than uniform guessing. Only 50 items/task, one region/run; cascade threshold was selected in-sample. Top probability is distinct from Choice confidence. No independent reproduction.

## Sources

- [medium.com](https://medium.com/@manjunath.shiva/i-tested-typesafes-jev-a-470-cheaper-decision-model-against-claude-gpt-6-kimi-minimax-and-d36ed152e861) — access: `access_failed`; review: `not_reviewed`.
- [github.com](https://github.com/manjunathshiva/jev-frontier-bench) — access: `fetched`; review: `sections_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
