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

Jev Score/Noul/Choice setups rerank 30 BM25 candidates, truncated to 2,000 characters each. Of 2,327 queries, 1,617 have a labeled relevant candidate and enter the ranking comparison; separate NevIR tests evaluate negation.

## Why and impact

Author reports macro nDCG@10 0.692 for Jev rubric versus 0.691 Cohere with no clear difference; query-weighted results favor Cohere 0.756 versus 0.738. NevIR paired accuracy favors Jev rubric 71.1% versus 67.0%; ZeroEntropy is cheaper in the reported cost table.

## Limits and reuse

There is no clean winner. Aggregation method changes the apparent result; do not advertise universal superiority. Source review: Strong comparative evidence is workload-specific: macro ranking tie with Cohere, Cohere leads query-weighted average, ZeroEntropy cheaper. Candidate/order sensitivity and answer-absent confidence failures limit autonomous retrieval. Batching cost savings do not establish quality; validate support/contradiction judgments and thresholds on held-out application data.

## Sources

- Discord source — private provenance retained locally.
- [https://anessbelbati.com/blog/i-gave-jev-a-rerankers-job](https://anessbelbati.com/blog/i-gave-jev-a-rerankers-job) — access: `fetched`; review: `article_reviewed`.
- [https://x.com/anessbelbati/status/2100398911911248050?s=20](https://x.com/anessbelbati/status/2100398911911248050?s=20) — access: `fetched`; review: `post_text_reviewed_media_pending`.
- [https://anessbelbati.com/lab/jev-reranking/](https://anessbelbati.com/lab/jev-reranking/) — access: `fetched`; review: `metadata_only`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
