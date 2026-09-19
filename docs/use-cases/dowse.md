---
id: dowse
title: "Dowse: search, rerank, answer"
category: retrieval
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Dowse: search, rerank, answer

## What

Find relevant evidence before generating an answer.

## How Jev fits

Search produces candidates, Jev ranks them and Gemini handles the final generative step.

## Why and impact

Direct precedent for Jev-bot's resource-selection layer.

## Limits and reuse

No evaluation was reproduced. Retrieval coverage and citation faithfulness remain separate requirements. Source review: Jev does not browse or write summaries. Reranking is opt-in and fail-open, so injection filtering is not a security boundary. Citation numbering preserves links but does not establish claim support. No measured retrieval or answer-quality improvement supplied.

## Sources

- [https://x.com/felixnjenga_/status/2100704201797939569](https://x.com/felixnjenga_/status/2100704201797939569) — access: `fetched`; review: `demo_trace_reviewed`.
- [Author-linked implementation artifact](http://github.com/arttivhq/dowse) — discovered via [external source](https://x.com/felixnjenga_/status/2100704201797939569); access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
