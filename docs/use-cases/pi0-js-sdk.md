---
id: pi0-js-sdk
title: "Alternative JavaScript SDK for typed questions"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Alternative JavaScript SDK for typed questions

## What

Advocaat offers typed Jev question helpers for probabilities, choices and scores.

## How Jev fits

Shared-state ask batches questions; standalone awaited tags each send a request. Boolean conversion defaults to strictly above 0.5.

## Why and impact

The client supports direct TypeSafe and Vercel AI Gateway with a common answer shape.

## Limits and reuse

Requests are not retried, repeated awaits send another request, and gateway confidence is computed locally with a stated discrepancy for scores of four or more levels.

## Sources

- Discord source — private provenance retained locally.
- [Github](https://github.com/pithings/advocaat) — access: `fetched`; review: `readme_reviewed`.
- [https://x.com/_pi0_/status/2100362008856010789](https://x.com/_pi0_/status/2100362008856010789) — access: `fetched`; review: `visible_post_text_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
