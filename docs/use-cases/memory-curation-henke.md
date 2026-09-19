---
id: memory-curation-henke
title: "Memory curation: batched judgments and latency report"
category: agents
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Memory curation: batched judgments and latency report

## What

Author tests Jev for memory selection and fact-merge decisions in a bot.

## How Jev fits

15 or35 Noul judgments share one request; fact merge uses a single Choice rubric.

## Why and impact

Reported15-item curation711ms versus4.4-6s baseline;35-item739ms versus baseline6s timeout. Single-probe median239ms across five runs.

## Limits and reuse

No memory quality comparison, ground truth or inspected code. Baseline mixes averages, p90s and timeouts; do not treat timeout as completed latency or claim general speedup.

## Sources


Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
