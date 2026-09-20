---
id: jev-watch
title: "jev-watch: regression checks for typed decisions"
category: quality
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# jev-watch: regression checks for typed decisions

## What

Replay saved decision cases and detect answer or confidence changes.

## How Jev fits

The CLI compares returned Choice/Score values with expected values and tolerances. The README records a prior adapter bug that incorrectly mapped Score onto Noul.

## Why and impact

Keeps API wiring failures and model drift visible before downstream routing changes silently.

## Limits and reuse

A baseline is only as correct as its labels. Synthetic tests validate comparison logic, not Jev accuracy. Some examples are aligned to current model answers, and the confidence check uses an absolute floor rather than a stored previous confidence.

## Sources

- [github.com](https://github.com/akanthed/jev-watch) — access: `fetched`; review: `sections_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
