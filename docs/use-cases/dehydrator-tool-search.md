---
id: dehydrator-tool-search
title: "Dehydrator: client-side tool search with BM25, Jev or both"
category: agents
evidence: author-reported
reviewed_on: 2026-09-27
independently_reproduced: false
---

# Dehydrator: client-side tool search with BM25, Jev or both

## What

A wrapper for LLM APIs replaces a large tool list with one tool_search tool, so an agent can use thousands of tools without sending every definition each turn.

## How Jev fits

When the model searches, Dehydrator intercepts the call and ranks tools by BM25, by one Jev Choice with every tool as an option, or by BM25 for ten candidates followed by Jev, then re-calls the model with only the matches.

## Why and impact

On 139 real tools from six MCP servers and 30 hand-labelled queries, top-1 precision rose from 93.3% (BM25) to 100% (Jev or hybrid), at about $0.00002 per hybrid search and ~390 ms.

## Limits and reuse

Small, author-labelled query set. Jev puts almost all probability on its top pick, so positions 2-10 are effectively unordered; the hybrid keeps BM25's tail for multi-tool injection. Choice is capped at 255 options, and gateways returned 429s above about three concurrent requests.

## Sources

- [https://github.com/Arrmlet/dehydrator](https://github.com/Arrmlet/dehydrator) — access: `fetched`; review: `readme_reviewed`.
- [https://x.com/v_truba/status/2101772072091365592?s=20](https://x.com/v_truba/status/2101772072091365592?s=20) — access: `fetched`; review: `not_reviewed`.
- [https://github.com/Arrmlet/dehydrator/blob/main/BENCHMARKS.md](https://github.com/Arrmlet/dehydrator/blob/main/BENCHMARKS.md) — access: `fetched`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
