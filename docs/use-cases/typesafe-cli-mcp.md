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

Developer publishes a command-line interface and MCP server for TypeSafe.

## How Jev fits

CLI exposes Noul, Choice and Score numeric/typed answers; MCP lets compatible agent hosts call decision tools. Exact parameter and error handling require repository inspection.

## Why and impact

Reduces integration work for scripts and agent hosts.

## Limits and reuse

Tool availability does not establish task accuracy or authorize execution. Keep host validation and permissions.

## Sources

- Discord source — private provenance retained locally.
- [https://github.com/y0usaf/typesafe-cli](https://github.com/y0usaf/typesafe-cli) — access: `fetched`; review: `not_reviewed`.
- [https://github.com/y0usaf/typesafe-mcp](https://github.com/y0usaf/typesafe-mcp) — access: `fetched`; review: `source_text_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
