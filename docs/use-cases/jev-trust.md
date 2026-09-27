---
id: jev-trust
title: "jev-trust: logging outcomes and inspecting calibration claims"
category: experiments
evidence: author-reported
reviewed_on: 2026-09-27
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

Reported calibration numbers and adjustment formulas remain unverified. Before reusing them, audit whether the measured field is a selected-option probability, a Noul probability or the API confidence statistic; these are not interchangeable. Small bins, signatures and polarity agreement do not prove future correctness, independence of evidence or safety. Held from default recommendations pending field/formula and raw-artifact review. Later posts measured the same instrument on three task types (n=120 each): reading code to predict exceptions 100%, patch behaviour 92.5%, a written four-rule spec over joint-angle sequences 50%. Reversing the spec's polarity turned an all-yes collapse (60/60 clean sequences flagged) into rubber-stamping (28/60 defects missed); rules needing computation over the numbers were the ones missed. A pre-registered adversarial study (negation, near-boundary numbers, irrelevant premises, huge numbers) found no calibration collapse.

## Sources

- [jev-trust](https://pypi.org/project/jev-trust/) — access: `fetched`; review: `scoped_package_documentation_reviewed`.
- [nautilus-compass/sdks/jev-trust at main · chunxiaoxx/nautilus-compass](https://github.com/chunxiaoxx/nautilus-compass/tree/main/sdks/jev-trust) — access: `fetched`; review: `sections_reviewed`.
- [Independent two-study validation of hosted Jev (jev-1.13.0) — cal...](https://github.com/chunxiaoxx/nautilus-compass/discussions/59) — access: `fetched`; review: `not_reviewed`.
- [https://compass.nautilus.social/dcr.html](https://compass.nautilus.social/dcr.html) — access: `fetched`; review: `not_reviewed`.
- [nautilus-compass/runtime/jev_trust_domain3_20260922 at main · chun...](https://github.com/chunxiaoxx/nautilus-compass/tree/main/runtime/jev_trust_domain3_20260922) — access: `fetched`; review: `not_reviewed`.
- [nautilus-compass/runtime/jev_trust_domain4_20260922 at main · chun...](https://github.com/chunxiaoxx/nautilus-compass/tree/main/runtime/jev_trust_domain4_20260922) — access: `fetched`; review: `not_reviewed`.
- [nautilus-compass/runtime/jev_advcal_20260922 at main · chunxiaoxx/...](https://github.com/chunxiaoxx/nautilus-compass/tree/main/runtime/jev_advcal_20260922) — access: `fetched`; review: `not_reviewed`.
- [nautilus-compass/docs/wall/GENESIS_HOSTED_JEV_ADVCAL.md at main · ...](https://github.com/chunxiaoxx/nautilus-compass/blob/main/docs/wall/GENESIS_HOSTED_JEV_ADVCAL.md) — access: `fetched`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
