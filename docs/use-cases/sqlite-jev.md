---
id: sqlite-jev
title: "SQLite: batched natural-language judgments"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# SQLite: batched natural-language judgments

## What

mgaitan/sqlite-jev embeds semantic judgments in SQLite workflows.

## How Jev fits

Batches questions over database records and includes a comparison table.

## Why and impact

Accessible SQL integration for local data processing.

## Limits and reuse

Source review needed for concurrency, null/error behavior, data disclosure and claimed savings. Source review: Semantic full scan is not index; prefilter/materialize selected columns first. Cache lifetime only connection, keyedcontent/model/questions. Database rows leave machine; adversarial row text can steer judgments. Keep arithmetic/counting inSQL; live contract smoke does not establish classification quality or current competitor feature parity.

## Sources

- [https://github.com/mgaitan/sqlite-jev](https://github.com/mgaitan/sqlite-jev) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
