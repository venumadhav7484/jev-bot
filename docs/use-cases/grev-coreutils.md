---
id: grev-coreutils
title: "grev: Unix filters that ask questions instead of matching patterns"
category: developer-tools
evidence: author-reported
reviewed_on: 2026-09-27
independently_reproduced: false
---

# grev: Unix filters that ask questions instead of matching patterns

## What

A set of command-line tools rebuilds grep, test, sort, cut, uniq and tr around typed questions answered by Jev.

## How Jev fits

Each tool passes records to Jev and keeps the input unchanged: grev prints records Jev says yes to, isv returns a yes/no as an exit status, tagv labels and routes, rank and sortv order, lookv bisects a log by meaning, and probabilities can be emitted as columns for awk.

## Why and impact

The README states a few thousand lines cost fractions of a cent and take seconds, and that output is always the original input, so the tools compose like ordinary filters.

## Limits and reuse

Author README; no accuracy benchmark. Meaning-based filters can silently drop relevant lines, so use them to narrow, not to prove absence. Using isv as a commit guard is only as good as the question and threshold.

## Sources

- [GitHub - aurorainfra/grev: Thinking coreutils](https://github.com/aurorainfra/grev) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
