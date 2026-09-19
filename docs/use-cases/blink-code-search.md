---
id: blink-code-search
title: "Blink: Jev-powered codebase search CLI"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Blink: Jev-powered codebase search CLI

## What

Blink searches a codebase using Jev and an ensemble of filesystem walkers.

## How Jev fits

Jev scores file and folder names; walkers allocate toward likely paths. Results show the fraction of starting walkers ending at each file.

## Why and impact

Saved traces retain every choice, probability and destination, while metadata records token usage and cost.

## Limits and reuse

Walker percentages are search-allocation outcomes, not calibrated correctness or content verification; name scoring may miss semantically relevant files. The documented tests use fake API responses.

## Sources

- [https://github.com/ellipsis-dev/blink](https://github.com/ellipsis-dev/blink) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
