---
id: jev-oas-sentinel
title: "OpenAPI Sentinel: review semantic changes hidden in prose"
category: developer-tools
evidence: author-reported
reviewed_on: 2026-09-24
independently_reproduced: false
---

# OpenAPI Sentinel: review semantic changes hidden in prose

## What

An OpenAPI-diff tool checks consumer-facing behavior changes that structural schema comparison may miss.

## How Jev fits

Structural checks and CI policy remain deterministic. Changed operation fragments go to Jev for bounded judgments about retries, pagination, ordering, authorization descriptions or error semantics.

## Why and impact

Adds a semantic review layer around existing API-contract checks, with CLI, GitHub Action, SARIF output and a no-key dry run.

## Limits and reuse

This is an author-reported implementation. A small semantic-routing benchmark does not establish complete breaking-change recall. Described authorization semantics are not actual authorization enforcement; missing cross-operation context and unchanged external code can remain invisible.

## Sources

- [GitHub - ShuhanSun/jev-oas-sentinel: Catch breaking API behavior hi...](https://github.com/ShuhanSun/jev-oas-sentinel) — access: `fetched`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
