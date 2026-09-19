---
id: jod-schemas
title: "Jod: local schema checks and semantic typed answers"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Jod: local schema checks and semantic typed answers

## What

mateonunez/jod connects Zod-like validation to Jev judgments.

## How Jev fits

Validate state locally, then project semantic typed answers from TypeSafe.

## Why and impact

Separates data-shape guarantees from probabilistic semantic judgments.

## Limits and reuse

Early user reports missing API-key input path. Source review needed; schema validity does not guarantee semantic correctness. Source review: Schema validation protects shape, not truth or adversarial input. Historical aliases-only observation must not override successful pinned jev1.13 calls/currentdocs. Confidence not correctness; SDK retry behavior inherited. Installation/publish availability and skipped-live-test status need separate verification.

## Sources

- Discord source — private provenance retained locally.
- [https://github.com/mateonunez/jod](https://github.com/mateonunez/jod) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
