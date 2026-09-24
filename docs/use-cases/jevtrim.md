---
id: jevtrim
title: "jevtrim: compare relevance selection at matched context budgets"
category: retrieval
evidence: author-reported
reviewed_on: 2026-09-24
independently_reproduced: false
---

# jevtrim: compare relevance selection at matched context budgets

## What

A context-selection experiment compares Jev judgments with embedding retrieval across conversation segmentations and token budgets.

## How Jev fits

Jev scores chunks; Python selects within the budget; a separate reader answers questions. The README distinguishes question-conditioned compaction from one compaction per conversation.

## Why and impact

On 486 LoCoMo questions from ten conversations, the author reports Jev ahead in 14 of 16 raw conditioned cells. The best 35%-budget result was 0.644 accuracy versus 0.671 for full context: about 96% of baseline accuracy, not 96% absolute accuracy.

## Limits and reuse

Matched budgets help comparison but do not establish general coding-memory quality. Segmentation and reader performance still affect results; coarsest chunks lose some comparisons. Source claims, not independently reproduced; recorded selection can replay deterministically, live Jev judgments are not deterministic.

## Sources

- [GitHub - pdrpinto/jevtrim: Jev as a context judge, benchmarked: sel...](https://github.com/pdrpinto/jevtrim) — access: `fetched`; review: `sections_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
