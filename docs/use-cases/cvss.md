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

Correct arithmetic cannot repair incorrect field classification. Human review and version-specific CVSS definitions remain important.

## Sources

- Discord source — private provenance retained locally.
- [https://github.com/Red5d/jev-cvss](https://github.com/Red5d/jev-cvss) — access: `fetch_failed`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
