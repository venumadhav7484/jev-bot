---
id: code-catalog-search
title: "Code catalog semantic search"
category: retrieval
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Code catalog semantic search

## What

Find relevant code through existing catalog documentation.

## How Jev fits

Jev evaluates documented code candidates before the main model reads selected material. Existing Markdown catalog is maintained by an agent every 24 hours; retrieval depends on that catalog quality and freshness.

## Why and impact

The author reports half the LLM token use and roughly one-third faster execution without observed accuracy regressions.

## Limits and reuse

Workload size and regression definition were not supplied; stale catalog descriptions can hide relevant code.

## Sources


Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
