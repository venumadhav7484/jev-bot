---
id: wellposed
title: "Wellposed: semantic request linting"
category: quality
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Wellposed: semantic request linting

## What

Catch valid JSON requests that ask ill-posed questions.

## How Jev fits

The inspected README combines deterministic structural checks with optional Jev semantic checks over request meaning.

## Why and impact

The author demonstrates a wrong Choice at confidence 1.00 when no escape hatch exists; adding other changes the result.

## Limits and reuse

The 40-request corpus was generated and labeled by one model. Confidence gating alone cannot catch missing-option failures; this tool is not a correctness proof.

## Sources

- [https://github.com/suraj-phanindra/wellposed](https://github.com/suraj-phanindra/wellposed) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
