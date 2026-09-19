---
id: calibre-labels
title: "Calibre tagging with increasing label counts"
category: quality
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Calibre tagging with increasing label counts

## What

An informal book-tagging experiment explores high-cardinality classification.

## How Jev fits

The author increases candidate labels from 10 to 241 using a noisy Calibre-derived dataset.

## Why and impact

Reported accuracy falls from 92% at 10 labels to 40% at 241, while per-call latency stays around 250 ms. Haiku also performs poorly on the largest set.

## Limits and reuse

Dataset quality and unequal call counts/concurrency limit comparisons. Numeric option limits do not guarantee constant accuracy; test real candidate distributions.

## Sources


Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
