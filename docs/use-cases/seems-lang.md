---
id: seems-lang
title: "Seems: typed uncertainty in Python-like programs"
category: agents
evidence: author-reported
reviewed_on: 2026-09-21
independently_reproduced: false
---

# Seems: typed uncertainty in Python-like programs

## What

A Python superset makes yes, no and unsure explicit branches for natural-language conditions.

## How Jev fits

A deterministic translator emits Python. Lazy judgments sharing state are batched and cached; Jev supplies typed decisions, while Python executes the selected branch.

## Why and impact

The language makes abstention part of control flow rather than treating every answer as a boolean. Its author reports small example workloads, not a production deployment.

## Limits and reuse

The existing customer-support automation predates this proposed adoption. Near-threshold responses can change branches; language tests do not validate judgments. Arithmetic, exact lookups and dates remain in Python. Latest source review: Documentation describes explicit true, false and unsure paths, lazy batching, short-circuiting and a cache keyed by model, state and question. Side-effecting calls must not execute early. The author reports probability drift; no interpreter or live model test was run here. Financial and destructive examples still require application authorization.

## Sources

- [kavehmz.github.io](https://kavehmz.github.io/seems-lang/) — access: `fetched`; review: `documentation_reviewed`.
- [github.com](https://github.com/kavehmz/seems-lang) — access: `fetched`; review: `sections_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
