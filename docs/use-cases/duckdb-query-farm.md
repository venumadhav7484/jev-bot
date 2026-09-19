---
id: duckdb-query-farm
title: "Query.Farm: Jev inside analytical queries"
category: data
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Query.Farm: Jev inside analytical queries

## What

Apply semantic judgments to analytical data.

## How Jev fits

The linked DuckDB integration exposes Jev to queries; the example evaluates Hacker News content.

## Why and impact

The author reports 500 items in 17 seconds for under one cent.

## Limits and reuse

The full query workload, token size and concurrency determine cost; no independent benchmark was run. Source review: Metadata-only interest filtering has no measured recommendation accuracy or user engagement. Cost and timing are author measurements; proposed autonomous thresholds need task-specific validation. Source review: Filter rows deterministically before API calls and materialize results to avoid repeat billing. Question batching and row concurrency are different. Confidence is not proof a row can safely auto-act; dynamic errors may quote row content. Reported live contract tests do not establish semantic SQL ranking quality.

## Sources

- Discord source — private provenance retained locally.
- [https://github.com/Query-farm/vgi-typesafe](https://github.com/Query-farm/vgi-typesafe) — access: `fetched`; review: `readme_reviewed`.
- [https://query.farm/blog/a-where-clause-for-taste/](https://query.farm/blog/a-where-clause-for-taste/) — access: `fetched`; review: `article_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
