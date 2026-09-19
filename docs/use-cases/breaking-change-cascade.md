---
id: breaking-change-cascade
title: "Filtering pull-request diffs before deeper review"
category: quality
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Filtering pull-request diffs before deeper review

## What

A CLI workflow scans pull requests for breaking changes.

## How Jev fits

Jev filters candidates; Sonnet reviews the smaller subset. The displayed run uses 25 Jev calls and two Sonnet calls with a 0.70 confidence bar.

## Why and impact

Author reports reducing roughly 99,000 input tokens to 8,300 for Sonnet and a 15.6-second run. The example includes a dismissed migration false positive.

## Limits and reuse

One run only. Missed breaking changes are not measured; token totals and cost accounting differ between models and need careful comparison.

## Sources

- Discord source — private provenance retained locally.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
