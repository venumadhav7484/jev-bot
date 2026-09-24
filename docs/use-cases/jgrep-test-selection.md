---
id: jgrep-test-selection
title: "jgrep: select potentially affected tests from a diff"
category: developer-tools
evidence: author-reported
reviewed_on: 2026-09-24
independently_reproduced: false
---

# jgrep: select potentially affected tests from a diff

## What

A semantic grep tool extends code-chunk screening to selecting test files that might be affected by a change.

## How Jev fits

One Noul per candidate asks whether supplied diff evidence affects that test; shared-state requests contain up to 16 chunks. Code returns file locations and probabilities.

## Why and impact

Author reports selecting 12% of tests with 92% recall over 60 commits from five repositories, using historically edited tests as the reference set.

## Limits and reuse

Tests edited by a patch author are an imperfect proxy for every test that should run. Whole-library checks such as bundle size were missed. This is a subset-selection aid, not evidence that omitted tests are safe to skip in every release. Distinct project from allebee/jevgrep.

## Sources

- [GitHub - kyu1204/jgrep: grep for what code does, not what it's call...](https://github.com/kyu1204/jgrep) — access: `fetched`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
