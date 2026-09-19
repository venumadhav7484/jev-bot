---
id: greenwash
title: "Greenwash: detecting superficial coding fixes"
category: quality
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Greenwash: detecting superficial coding fixes

## What

A GitHub app reviews PRs where CI passes but the reported problem may remain.

## How Jev fits

Jev supplies semantic review judgments over the change.

## Why and impact

Targets a gap between test success and actually fixing the issue.

## Limits and reuse

No regression-reproduction or review-recall results supplied. Deterministic repro tests remain important.

## Sources

- Discord source — private provenance retained locally.
- [https://x.com/itsayush__/status/2100600179615518918?s=20](https://x.com/itsayush__/status/2100600179615518918?s=20) — access: `fetch_failed`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
