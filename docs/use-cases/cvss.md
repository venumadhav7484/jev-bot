---
id: cvss
title: "Jev CVSS: classify fields, compute scores"
category: domain-review
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Jev CVSS: classify fields, compute scores

## What

Assist vulnerability severity scoring.

## How Jev fits

Jev classifies CVSS field values; deterministic code performs the score calculation.

## Why and impact

Keeps semantic interpretation separate from exact arithmetic.

## Limits and reuse

Reported zero mismatches on 300 randomized v3.1 vectors and 154 v4 comparisons concern deterministic arithmetic given metric values. They do not measure Jev metric-selection accuracy. Missing description facts and omitted environmental metrics remain gaps; NVD-inspired criteria are prompt tuning, not evidence of probability calibration.

## Sources

- Discord source — private provenance retained locally.
- [https://github.com/Red5d/jev-cvss](https://github.com/Red5d/jev-cvss) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
