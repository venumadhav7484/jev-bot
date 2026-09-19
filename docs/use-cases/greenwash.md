---
id: greenwash
title: "Greenwash: detecting superficial coding fixes"
category: quality
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Greenwash: detecting superficial coding fixes

## What

A GitHub app reviews PRs where CI passes but the reported problem may remain.

## How Jev fits

Per changed hunk, Jev answers narrow Noul questions about weakened assertions, disabled tests, swallowed errors and weakened CI; application thresholds generate line-specific annotations.

## Why and impact

Targets a gap between test success and actually fixing the issue.

## Limits and reuse

No regression-reproduction or review-recall results supplied. Deterministic repro tests remain important. Media review: Reviewed37 sampled frames plus transcript: Greenwash presentation shows assertion weakened, skipped tests, swallowed exception, hardcoded input and CI continue-on-error; per-hunk Noul questions feed policy thresholds and line annotations.99%/98% are example model probabilities, not precision/recall. Promotional presentation with code excerpt, not independent execution. Community-built; video wording 'from TypeSafe' corrected by author.

## Sources

- Discord source — private provenance retained locally.
- [https://x.com/itsayush__/status/2100600179615518918?s=20](https://x.com/itsayush__/status/2100600179615518918?s=20) — access: `fetched`; review: `demo_trace_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
