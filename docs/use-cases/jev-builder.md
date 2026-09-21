---
id: jev-builder
title: "Jev Builder: compose requests from text"
category: interfaces
evidence: author-reported
reviewed_on: 2026-09-21
independently_reproduced: false
---

# Jev Builder: compose requests from text

## What

A request-building interface preserves pasted text while producing Jev JSON.

## How Jev fits

The user selects a typed question template; application code handles escaping and request assembly. The author describes 34 templates and a simple robustness check.

## Why and impact

Reduces manual quoting and newline errors when testing transcripts or paragraphs.

## Limits and reuse

Template availability and robustness probes do not establish task accuracy. The source report requires local configuration for API execution; no installation or live tool test was performed here.

## Sources

- [collapseindex.github.io](https://collapseindex.github.io/jev-builder/) — access: `fetched`; review: `demo_interface_reviewed`.
- [github.com](https://github.com/collapseindex/jev-builder) — access: `fetched`; review: `sections_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
