---
id: cloaked-fields
title: "Cloaked: password-manager form classification"
category: browser
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Cloaked: password-manager form classification

## What

Identify fields across inconsistent website forms.

## How Jev fits

Jev receives sanitized HTML and about 60 possible control classifications; browser software owns form interaction.

## Why and impact

The author reports 564 pages and 4,831 controls: average page score 96.6% versus 74.3% for heuristics, 200 ms median API time.

## Limits and reuse

This is one author's fixture evaluation. Never confuse classification input with authorization to transmit passwords or complete forms.

## Sources

- Discord source — private provenance retained locally.
- [https://x.com/abhijay_cloaked/status/2100689866279252270?s=20](https://x.com/abhijay_cloaked/status/2100689866279252270?s=20) — access: `fetch_failed`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
