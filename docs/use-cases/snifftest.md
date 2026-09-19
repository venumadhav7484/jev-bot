---
id: snifftest
title: "SniffTest: document claim checks"
category: quality
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# SniffTest: document claim checks

## What

Flag problematic passages through bounded checks.

## How Jev fits

The author describes ten Boolean judgments per paragraph and a published evaluation note.

## Why and impact

Reports 63/80 planted issues found, one false flag in 54 clean cases and 182 ms timing.

## Limits and reuse

Also reports 13/166 missing answers. Missing-output handling and rotation behavior matter; these results are author-reported. Source review: Cheap prose judgments trade recall for cost; no rewriting or authorship detection. Small seeded and partly tuned-on corpus cannot establish general quality. Missing answers/neutral readings must remain unknown, not clean passes; headline Jev row differs from same-rotation measurement.

## Sources

- [https://github.com/DanRWilloughby/snifftest](https://github.com/DanRWilloughby/snifftest) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
