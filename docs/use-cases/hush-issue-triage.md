---
id: hush-issue-triage
title: "Hush: issue triage with abstention"
category: quality
evidence: author-reported
reviewed_on: 2026-09-21
independently_reproduced: false
---

# Hush: issue triage with abstention

## What

A GitHub Action withholds automatic issue triage below configured thresholds.

## How Jev fits

Four typed questions share one Jev request; code decides which verdicts to apply and reports the associated scores.

## Why and impact

The author reports a first issue falling below thresholds, so no action was posted. This makes doing nothing an explicit outcome.

## Limits and reuse

The inspected README reports an 800-issue evaluation with 78% default precision, rising to 88% when question labels are excluded; these are author results, not independently reproduced. Duplicate search is capped at 40 candidates. PR handling uses metadata rather than full diffs, and its three-PR sample is too small for a broad claim. Abstention and maintainer review remain important.

## Sources

- [Hush repository](https://github.com/emreozyoruk/hush) — discovered via Discord source (private provenance retained locally); access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
