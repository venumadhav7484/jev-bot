---
id: gluten-labels
title: "GlutenOrNot: product-label screening"
category: domain-review
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# GlutenOrNot: product-label screening

## What

Flag gluten-related signals in multilingual product labels.

## How Jev fits

The author compares Jev and Opus on about 1,000 Open Food Facts labels and links a sandbox.

## Why and impact

Reports matching flags, around $0.03 versus $8.45 and 0.17 versus 2.89 seconds.

## Limits and reuse

Agreement with another model is not medical validation. Missing ingredients, cross-contact and inaccurate source labels remain outside this evidence. Source review: Captured implementation uses Claude and separate OCR, not demonstrated Jev. Potential Jev substitution would be a proposal. Label extraction/ingredient checks do not establish clinical or cross-contamination safety; no medical rules were validated in this source review.

## Sources

- Discord source — private provenance retained locally.
- [https://github.com/amr05008/glutenornot.com](https://github.com/amr05008/glutenornot.com) — access: `fetched`; review: `context_only_not_jev_evidence`.
- [https://github.com/amr05008/jev-sandbox](https://github.com/amr05008/jev-sandbox) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
