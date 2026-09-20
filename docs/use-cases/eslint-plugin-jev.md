---
id: eslint-plugin-jev
title: "ESLint: natural-language semantic rules"
category: quality
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# ESLint: natural-language semantic rules

## What

Extend conventional linting with semantic questions about functions.

## How Jev fits

Jev judges function-level criteria while ESLint reports warnings and probabilities. Caching avoids repeating unchanged judgments.

## Why and impact

Complements syntax checks with questions about naming, comments and behavior.

## Limits and reuse

Source goes to a hosted API. Skipped requests and unavailable service can leave code unchecked; absence of warnings is not approval. No automatic semantic fix or proof of correctness follows from the score.

## Sources

- [x.com](https://x.com/ShahriarBijoy/status/2101468251372781601) — access: `fetched`; review: `not_reviewed`.
- [github.com](https://github.com/ShahriarBijoy/eslint-plugin-jev) — access: `fetched`; review: `sections_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
