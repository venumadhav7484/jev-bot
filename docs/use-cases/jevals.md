---
id: jevals
title: "Jevals: local decision-model workbench"
category: developer-tools
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Jevals: local decision-model workbench

## What

A local tool tracks improvements and regressions in Jev requests.

## How Jev fits

Local workbench supports Noul, Choice, Score, mixed requests and seeded examples. Author also reports WebMCP support; implementation has not been executed here.

## Why and impact

Makes prompt and schema changes comparable over time.

## Limits and reuse

No evaluation was run here. Useful experiments need labeled cases, stable versions and held-out examples. Source review: Evaluation tooling supports explicit labels and saved traces; seeded examples and simulated tests are not a representative accuracy benchmark. Media review: Reviewed full narration and opening/middle/final frame samples. Jevals shows cases, editable question definitions/thresholds/state schema, SQLite-backed run history, optional human rationale, JSON export and mixed Noul/Choice results. Small seeded sandwich runs show6/6 and7/7 with Brier scores; those are not broad accuracy evidence. Author explicitly says run-diff/version comparison is missing at recording time; WebMCP capability is described, not executed here.

## Sources

- [https://x.com/Dayhaysoos/status/2100968892591968320](https://x.com/Dayhaysoos/status/2100968892591968320) — access: `fetched`; review: `demo_trace_reviewed`.
- [Jevals workbench repository](https://github.com/dayhaysoos/jevals) — discovered via [external source](https://x.com/Dayhaysoos/status/2100968892591968320); access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
