---
id: jarviscore-decision-models
title: "JarvisCore: routing and passage decisions"
category: agents
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# JarvisCore: routing and passage decisions

## What

An agent framework adds optional typed decisions, specialist routing, model-tier routing and RAG passage review.

## How Jev fits

After FAISS retrieval, independent Nouls judge relevance, usable evidence, premise conflict and injection risk. Code retains accepted/conflicting material and excludes selected text from generation.

## Why and impact

Offers a concrete pattern for screening retrieved evidence before an LLM reads it. The author reports concurrent-call timing from one developer environment.

## Limits and reuse

Injection scores remain filters, not a security boundary. Accepted text stays untrusted; thresholds and fallback behavior need workload tests. No independent retrieval-quality or production benchmark was run here.

## Sources

- [github.com](https://github.com/Prescott-Data/jarviscore-framework) — access: `fetched`; review: `sections_reviewed`.
- [jarviscore.developers.prescottdata.io](https://jarviscore.developers.prescottdata.io/concepts/decision-models/) — access: `not_attempted`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
