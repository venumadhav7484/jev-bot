---
id: jev-compaction
title: "jev-compaction: retain original bytes with expandable pointers"
category: agents
evidence: author-reported
reviewed_on: 2026-09-24
independently_reproduced: false
---

# jev-compaction: retain original bytes with expandable pointers

## What

A context manager uses Jev judgments to retain or hide segments of coding-agent tool output without rewriting their text.

## How Jev fits

One request asks segment-level relevance, type, role, lifetime and injection questions. Application code stores original bytes, inserts pointers, tracks stale outputs, retrieves by lexical shortlist plus Jev reranking and weighs token savings against prompt-cache disruption.

## Why and impact

Author reports unchanged resolution counts of 20/23 in a small paired SWE-bench run, fewer later-needed code segments hidden when using role information and lower request size. The newer design explicitly prices cache invalidation instead of assuming it never happens.

## Limits and reuse

Exact byte recovery does not prove lossless task performance: the agent must know to recover omitted evidence. One run per arm, a small task set and planted injection tests are not general guarantees. The original claim that the prefix never invalidates cache is narrower than the later work-area rewrite design.

## Sources

- [GitHub - Waxmell114514/awesome-jev-compaction: A context compactor ...](https://github.com/Waxmell114514/awesome-jev-compaction) — access: `not_attempted`; review: `not_reviewed`.
- [https://github.com/Waxmell114514/jev-compaction](https://github.com/Waxmell114514/jev-compaction) — access: `fetched`; review: `sections_reviewed`.
- [https://waxmell114514.github.io/jev-compaction/](https://waxmell114514.github.io/jev-compaction/) — access: `fetched`; review: `not_reviewed`.
- [Related public project or article](https://waxmell114514.github.io/jev-compaction) — discovered via Discord source (private provenance retained locally); access: `fetched`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
