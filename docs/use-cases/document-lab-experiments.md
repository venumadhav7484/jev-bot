---
id: document-lab-experiments
title: "Document Lab: six judgments around document agents"
category: quality
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Document Lab: six judgments around document agents

## What

Author tests script fact-checking, news ranking, PDF passage reranking, citation checking, review-note grouping and trace diagnosis.

## How Jev fits

Jev compares claims with supplied sources, ranks eight retrieved passages, checks cited text against answers and assigns predefined error categories. Retrieval, OCR and answer writing remain separate.

## Why and impact

Reported script checks: both models24/24, median0.41s versus1.68s. Feed top10:6 versus2 relevant items. Passage first-hit:7 versus1. Note categories:24/28 versus25/28, median0.35s versus4.85s.

## Limits and reuse

Small author-labeled sets; no independent run. Trace diagnosis prose reports19/24 versus20/24, while table reports9/14 versus10/14; unresolved contradiction. Citation checks cover a handful of altered answers. Source-consistency checks cannot prove source truth. Proposed automated repairs remain future work.

## Sources

- [https://isaacflath.com/writing/six-things-i-tried-with-jev](https://isaacflath.com/writing/six-things-i-tried-with-jev) — access: `fetched`; review: `article_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
