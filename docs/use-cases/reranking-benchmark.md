---
id: reranking-benchmark
title: "Jev versus dedicated rerankers"
category: retrieval
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Jev versus dedicated rerankers

## What

Evaluate search-result reranking across multiple datasets.

## How Jev fits

The author compares 30 candidates per query across eight datasets and 2,327 questions, including negation tests.

## Why and impact

Dataset-average nDCG@10: Jev 0.692 versus Cohere 0.691. Query-average: Jev 0.738 versus Cohere 0.756.

## Limits and reuse

There is no clean winner. Aggregation method changes the apparent result; do not advertise universal superiority.

## Sources

- Discord source — private provenance retained locally.
- [https://anessbelbati.com/blog/i-gave-jev-a-rerankers-job](https://anessbelbati.com/blog/i-gave-jev-a-rerankers-job) — access: `fetch_failed`; review: `not_reviewed`.
- [https://x.com/anessbelbati/status/2100398911911248050?s=20](https://x.com/anessbelbati/status/2100398911911248050?s=20) — access: `fetch_failed`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
