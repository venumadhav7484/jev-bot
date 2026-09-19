---
id: cloaked-fields
title: "Cloaked: password-manager form classification"
category: browser
evidence: author-reported
reviewed_on: 2026-09-20
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

This is one author's fixture evaluation. Never confuse classification input with authorization to transmit passwords or complete forms. Media review: Reviewed opening/middle/final frame samples of Cloaked comparison. Corpus card identifies84original fixtures+480authored scenarios=564pages. Final score is equal-weight average over526pages with scored controls,74.3%heuristics versus96.6%Jev; field totals are2159/4831 versus4775/4831 (44.7%/98.8%). Median full API response213ms, not200ms exact. Corpus design, denominator and field-versus-page aggregation matter; no production or adversarial validation.

## Sources

- Discord source — private provenance retained locally.
- [https://x.com/abhijay_cloaked/status/2100689866279252270?s=20](https://x.com/abhijay_cloaked/status/2100689866279252270?s=20) — access: `fetched`; review: `demo_trace_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
