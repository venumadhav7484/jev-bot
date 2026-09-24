---
id: jev-trust
title: "jev-trust: logging outcomes and inspecting calibration claims"
category: experiments
evidence: author-reported
reviewed_on: 2026-09-24
independently_reproduced: false
---

# jev-trust: logging outcomes and inspecting calibration claims

## What

A Python middleware project records typed answers, later labels, domain statistics and signed audit logs.

## How Jev fits

The wrapper computes author-defined confidence adjustments from observed bins or aggregate calibration statistics. A later documented mode asks both polarities and flags disagreements.

## Why and impact

Provides a concrete pattern for retaining predictions and joining them to later outcomes instead of assuming one threshold works in every domain.

## Limits and reuse

Reported calibration numbers and adjustment formulas remain unverified. Before reusing them, audit whether the measured field is a selected-option probability, a Noul probability or the API confidence statistic; these are not interchangeable. Small bins, signatures and polarity agreement do not prove future correctness, independence of evidence or safety. Held from default recommendations pending field/formula and raw-artifact review.

## Sources

- [jev-trust](https://pypi.org/project/jev-trust/) — access: `fetched`; review: `scoped_package_documentation_reviewed`.
- [nautilus-compass/sdks/jev-trust at main · chunxiaoxx/nautilus-compass](https://github.com/chunxiaoxx/nautilus-compass/tree/main/sdks/jev-trust) — access: `fetched`; review: `sections_reviewed`.
- [Independent two-study validation of hosted Jev (jev-1.13.0) — cal...](https://github.com/chunxiaoxx/nautilus-compass/discussions/59) — access: `fetched`; review: `not_reviewed`.
- [https://compass.nautilus.social/dcr.html](https://compass.nautilus.social/dcr.html) — access: `fetched`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
