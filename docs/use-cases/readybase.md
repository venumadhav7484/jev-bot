---
id: readybase
title: "ReadyBase: reranking code context"
category: retrieval
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# ReadyBase: reranking code context

## What

Choose code facts that fit an agent's context budget.

## How Jev fits

Jev ranks the existing candidate pool. Deterministic code reserves critical facts before filling remaining space with semantic ranking.

## Why and impact

On 28 author-labeled scenarios, plain Jev reduced critical-fact retention to 91.7%; reserving critical facts restored 95.2% and yielded 73.6% overall recall.

## Limits and reuse

The $0.0017 run and recall figures are author results. Relevance alone does not capture facts that must always remain in context.

## Sources

- Discord source — private provenance retained locally.
- [https://www.promptforce.ai/readybase](https://www.promptforce.ai/readybase) — access: `fetched`; review: `not_reviewed`.
- [https://github.com/PromptForcePrime/readybase-public/releases/tag/v1.6.0](https://github.com/PromptForcePrime/readybase-public/releases/tag/v1.6.0) — access: `fetch_failed`; review: `not_reviewed`.
- [https://promptforce.ai/rb-install.sh](https://promptforce.ai/rb-install.sh) — access: `fetch_failed`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
