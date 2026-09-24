---
id: jevgrep
title: "jevgrep: ordered log filtering with named state entries"
category: filtering
evidence: author-reported
reviewed_on: 2026-09-24
independently_reproduced: false
---

# jevgrep: ordered log filtering with named state entries

## What

A command-line filter asks whether each log line matches a user-supplied condition.

## How Jev fits

One Noul refers to each named line in shared state. Micro-batches and concurrent requests preserve output order; an optional Claude stage explains selected lines.

## Why and impact

Author reports mean F1 rising from about 0.75 with array-index references to 0.90 with named keys on 195 labelled lines and three questions. This is evidence to test state addressing, not a universal preferred batch size.

## Limits and reuse

Fuzzy definitions and lines describing themselves still cause errors. The README says lines longer than 500 characters are truncated for judgment but printed in full, so decisive text can be unseen. Timing includes buffering; reported speed/cost and model comparisons are author measurements, not reproduced here.

## Sources

- [GitHub - allebee/jevgrep: grep by meaning: pipe in any text, ask a ...](https://github.com/allebee/jevgrep) — access: `fetched`; review: `sections_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
