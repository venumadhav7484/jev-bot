---
id: gbrain
title: "GBrain: optional relevance reranker"
category: retrieval
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# GBrain: optional relevance reranker

## What

Add Jev as a document reranking provider.

## How Jev fits

Score questions judge query relevance, with context-aware batching and concurrent execution through the existing provider architecture.

## Why and impact

One synthetic 100-document run reported 1.90 seconds versus 14.40 seconds for Voyage, excluding quota waits, at roughly equal nominal cost.

## Limits and reuse

One run per provider; different batching and free-tier pacing affect comparison. A linked PR is not proof of merge or production deployment. Source review: Open PR is proposed integration, not merged availability. Large-pool wall-speed ratios reflect account quotas and collector batching; no universal Jev cost win or held-out quality equivalence. Synthetic single query and repeated background text do not validate downstream score thresholds. Detailed raw evidence not independently recomputed here. Source review: Current main README does not establish shipped Jev integration. Keep open Jev-rerank PR evidence separate from this adjacent knowledge-store architecture and its synthetic graph benchmark.

## Sources

- [GBrain](https://github.com/garrytan/gbrain) — access: `fetched`; review: `context_repository_reviewed`.
- [https://github.com/garrytan/gbrain/pull/5178](https://github.com/garrytan/gbrain/pull/5178) — access: `fetched`; review: `pull_request_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
