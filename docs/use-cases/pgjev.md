---
id: pgjev
title: "pg-jev: semantic SQL predicates"
category: data
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# pg-jev: semantic SQL predicates

## What

Filter database rows using natural-language conditions.

## How Jev fits

A PostgreSQL extension asks Jev to judge each candidate row; SQL handles filtering and result composition.

## Why and impact

The author reports 129 rows in about one second for $0.0009.

## Limits and reuse

Full-table semantic scans are not an index replacement with constant cost. Video shows 129 rows batched into four requests at roughly one second; 4.8ms repeat comes from session cache, not a fresh Jev call. Cache must include row content, condition, model and question version. No large-table scalability or accuracy benchmark reproduced. Demo uses invented data; avoid inferred-personal-attribute predicates for consequential decisions.

## Sources

- Discord source — private provenance retained locally.
- [https://pgjev.zachi.dev/](https://pgjev.zachi.dev/) — access: `fetched`; review: `source_text_reviewed`.
- [https://x.com/iam_zachi/status/2100679300756435135](https://x.com/iam_zachi/status/2100679300756435135) — access: `fetched`; review: `demo_trace_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
