---
id: pgjev
title: "pg-jev: semantic SQL predicates"
category: data
evidence: author-reported
reviewed_on: 2026-09-19
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

This is semantic evaluation, not an index replacement with constant cost. Avoid discriminatory inferred-personal-attribute predicates; use task-relevant evidence. Source review: Demo uses invented data. Reported cheap reruns rely on session cache; changing data/conditions needs evaluation and appropriate cache invalidation.

## Sources

- Discord source — private provenance retained locally.
- [https://pgjev.zachi.dev/](https://pgjev.zachi.dev/) — access: `fetched`; review: `source_text_reviewed`.
- [https://x.com/iam_zachi/status/2100679300756435135](https://x.com/iam_zachi/status/2100679300756435135) — access: `fetched`; review: `post_text_reviewed_media_pending`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
