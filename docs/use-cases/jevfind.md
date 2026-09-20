---
id: jevfind
title: "JevFind: semantic code search"
category: retrieval
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# JevFind: semantic code search

## What

Find source files and line ranges from a natural-language question.

## How Jev fits

The CLI filters files locally, scores paths with Jev, then evaluates bounded overlapping code windows. Application code returns exact snippets and line ranges.

## Why and impact

Can narrow context before an agent opens full files, especially when names do not match the query.

## Limits and reuse

Path screening can discard relevant files with surprising names. Windows can overlap and duplicate results. Source snippets leave the machine; the author calls this an imperfect demo, not exhaustive search.

## Sources

- [github.com](https://github.com/Peu77/JevFind) — access: `fetched`; review: `sections_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
