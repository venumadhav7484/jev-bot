---
id: wince
title: "Wince: route human review attention"
category: quality
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Wince: route human review attention

## What

Decide how carefully a diff should be reviewed and by whom.

## How Jev fits

Jev evaluates blast radius, auth/data writes and contract breaks. Deterministic code computes final review routing.

## Why and impact

Useful when review capacity is limited and semantic risk signals complement exact metadata.

## Limits and reuse

The project explicitly does not review code correctness. Do not turn its green label into permission to merge. Source review: Review score is policy weighting, not probability of a bug. Small private dataset and follow-up-fix proxy limit generalization; hunk ranking negative result must remain visible. No review generation or merge approval. Hard flags, excluded files and failed calls block green; diff-only context misses ticket intent.

## Sources

- [https://github.com/TinyFrontier/wince](https://github.com/TinyFrontier/wince) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
