---
id: werkfaden-feedback
title: "Atomic claim feedback for coding patches"
category: quality
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Atomic claim feedback for coding patches

## What

A coding workflow checks proposed patches as individual claims.

## How Jev fits

Two scripts around Werkfaden decompose a patch attempt into claims, query Jev with Nouls, and return the list to the coding LLM.

## Why and impact

Provides focused feedback on unsupported assumptions.

## Limits and reuse

Author says better data is still pending. Decomposition errors and incorrect judgments can mislead the revising model.

## Sources

- Discord source — private provenance retained locally.
- [https://github.com/Question86/Werkfaden](https://github.com/Question86/Werkfaden) — access: `fetched`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
