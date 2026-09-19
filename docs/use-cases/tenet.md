---
id: tenet
title: "Tenet: natural-language code review rules"
category: quality
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Tenet: natural-language code review rules

## What

Check agent-written commits against repository conventions.

## How Jev fits

Developers define rules in .tenet/config.yml; Jev judges bounded changed-line windows. Code applies thresholds, localizes findings, records clean receipts and feeds results into an agent correction loop.

## Why and impact

Targets semantic conventions that ordinary syntax linting misses.

## Limits and reuse

The project was early-stage in its post. A passing judgment does not establish functional correctness or replace tests. Source review: Diff-only semantic lint complements tests and whole-program review. Calibrate on held-out examples, inspect repeated threshold crossings, and do not equate faster calls with equal defect recall. Exemptions/baselines and hook bypasses limit enforcement.

## Sources

- Discord source — private provenance retained locally.
- [https://github.com/zoidsh/tenet](https://github.com/zoidsh/tenet) — access: `fetched`; review: `repository_documentation_reviewed`.
- [https://github.com/zoidsh/tenetlint](https://github.com/zoidsh/tenetlint) — access: `fetched`; review: `duplicate_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
