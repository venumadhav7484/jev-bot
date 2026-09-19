---
id: task-file-filter
title: "Relevant-file selection before code generation"
category: retrieval
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Relevant-file selection before code generation

## What

A proof of concept filters and sorts repository files for a task.

## How Jev fits

Jev selects relevant files; a generative LLM receives that subset to edit, write or explain code.

## Why and impact

Reduces irrelevant context reaching a slower model.

## Limits and reuse

No retrieval recall, cost or latency measurements supplied. Validate that important dependency and instruction files survive filtering.

## Sources

- Discord source — private provenance retained locally.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
