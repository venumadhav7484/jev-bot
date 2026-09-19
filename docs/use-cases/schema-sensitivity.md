---
id: schema-sensitivity
title: "Choice labels and ordering can change probabilities"
category: quality
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Choice labels and ordering can change probabilities

## What

Community experiments probe representation-sensitive decisions.

## How Jev fits

Authors change criterion names and insertion order, compare identical duplicates, and repeat requests. A follow-up uses 1,617 labeled reranking queries.

## Why and impact

The follow-up reports duplicate agreement within 0.005 but larger shifts for uncertain passages across label pairs; high-confidence passages move less.

## Limits and reuse

This is author-reported evidence, not independent reproduction. Version labels, order, instructions, preprocessing and model together; do not infer which representation is better calibrated without outcome labels. The author distinguishes repeated-call noise from stable schema effects and explicitly says correctness requires ground-truth evaluation. Different primitives and labels are not interchangeable measurements.

## Sources

- Discord source — private provenance retained locally.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
