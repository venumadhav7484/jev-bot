---
id: typesafe-cli-mcp
title: "Shell CLI and MCP adapter for TypeSafe"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Shell CLI and MCP adapter for TypeSafe

## What

typesafe-cli exposes Jev Noul, Choice and Score through shell commands.

## How Jev fits

The ask command batches questions in one request; it validates documents before sending and accepts structured state.

## Why and impact

An example reports three answers, 404 input tokens and 74 output tokens in 0.29 seconds. Field naming reportedly changes results across a handful of runs, explicitly not a study.

## Limits and reuse

The README says 429 and 5xx failures retry twice; requests therefore need billing/error accounting. The statement that only state is sent conflicts with the displayed request containing questions; treat that privacy wording as incomplete. External correction: current official Models documentation (https://docs.typesafe.ai/models), checked 2026-09-19, specifies 64k combined request tokens and 32k for state plus the longest question, unlike the README’s blanket 32k wording.

## Sources

- [https://github.com/y0usaf/typesafe-cli](https://github.com/y0usaf/typesafe-cli) — access: `fetched`; review: `readme_reviewed`.
- [https://github.com/y0usaf/typesafe-mcp](https://github.com/y0usaf/typesafe-mcp) — access: `fetched`; review: `source_text_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
