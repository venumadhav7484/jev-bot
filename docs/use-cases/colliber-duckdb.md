---
id: colliber-duckdb
title: "DuckDB extension: judgments as SQL types"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# DuckDB extension: judgments as SQL types

## What

colliber/duckdb-jev embeds typed Jev answers into DuckDB queries.

## How Jev fits

SQL functions return native typed values rather than prose.

## Why and impact

Lets analytical workflows combine deterministic queries with semantic predicates.

## Limits and reuse

Separate Query.Farm implementation; source review needed for batching, retries, nulls and secrets handling.

## Sources

- [https://github.com/colliber/duckdb-jev](https://github.com/colliber/duckdb-jev) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
