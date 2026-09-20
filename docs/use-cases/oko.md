---
id: oko
title: "Oko: local search followed by Jev ranking"
category: retrieval
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Oko: local search followed by Jev ranking

## What

An MCP/CLI tool searches code locally and ranks selected snippets with Jev.

## How Jev fits

Local discovery limits candidate volume, then typed relevance judgments choose evidence for a coding agent. A local-only fallback can run without Jev.

## Why and impact

The author reports a 108-session pilot, including up to 46.2% fewer agent tokens with a warm cache.

## Limits and reuse

Token counts include cached input and exclude Jev, so they are not dollar savings. Cold runs were slower for Codex in the reported comparison. One observation per task/condition, grading caveats and no independent reproduction limit generalization.

## Sources

- [github.com](https://github.com/bartlomein/oko) — access: `fetched`; review: `sections_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
