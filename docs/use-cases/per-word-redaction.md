---
id: per-word-redaction
title: "PII redaction: one binary question per word"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# PII redaction: one binary question per word

## What

Exploratory redaction marks individual word positions.

## How Jev fits

Split sentence into words and ask whether word X at index Y should be redacted with separate Noul questions.

## Why and impact

Simple bounded span-masking design; author explicitly calls it inefficient.

## Limits and reuse

No privacy-recall benchmark; multiword entities/context and API disclosure need attention. Distinct from database-side masking implementation.

## Sources

- [https://x.com/danmana/status/2100550435094278475](https://x.com/danmana/status/2100550435094278475) — access: `fetched`; review: `demo_trace_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
