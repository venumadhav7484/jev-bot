---
id: jarviscore-decision-models
title: "JarvisCore: routing and passage decisions"
category: agents
evidence: author-reported
reviewed_on: 2026-09-21
independently_reproduced: false
---

# JarvisCore: routing and passage decisions

## What

An agent framework adds optional typed decisions, specialist routing, model-tier routing and RAG passage review.

## How Jev fits

Deterministic routes run first. Optional Jev judgments use explicit state; four independent RAG predicates can run together. Low-confidence decisions stay available to the planning path.

## Why and impact

Offers a concrete pattern for screening retrieved evidence before an LLM reads it. The author reports concurrent-call timing from one developer environment.

## Limits and reuse

Injection scores remain filters, not a security boundary. Accepted text stays untrusted; thresholds and fallback behavior need workload tests. No independent retrieval-quality or production benchmark was run here. Latest source review: Repository documentation reviewed, not independently executed. The author reports about 434 ms for a warm call and 1.28 seconds for three parallel calls in an eight-probe experiment; those observations are not a general latency guarantee. Async integration, retrieval, planning, persistence and execution remain application responsibilities.

## Sources

- [github.com](https://github.com/Prescott-Data/jarviscore-framework) — access: `fetched`; review: `sections_reviewed`.
- [jarviscore.developers.prescottdata.io](https://jarviscore.developers.prescottdata.io/concepts/decision-models/) — access: `fetched`; review: `documentation_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
