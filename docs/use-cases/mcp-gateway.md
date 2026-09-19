---
id: mcp-gateway
title: "Selective MCP tool exposure"
category: agents
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Selective MCP tool exposure

## What

A local gateway selects tools from multiple MCP servers.

## How Jev fits

Jev identifies the relevant tool; the main LLM fills arguments, avoiding exposure of every tool schema.

## Why and impact

Author reports 79% fewer input tokens on MCP-heavy tasks tested with 124 tools.

## Limits and reuse

No independent task-success or latency comparison. Validate tool recall and the overhead of the additional routing call.

## Sources

- Discord source — private provenance retained locally.
- [https://x.com/vpkxvoice/status/2100995268133146698](https://x.com/vpkxvoice/status/2100995268133146698) — access: `fetched`; review: `visible_post_text_reviewed`.
- [Author-linked implementation artifact](https://github.com/prasanth263/maza) — discovered via [external source](https://x.com/vpkxvoice/status/2100995268133146698); access: `fetched`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
