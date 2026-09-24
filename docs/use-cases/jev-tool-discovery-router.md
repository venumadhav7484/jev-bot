---
id: jev-tool-discovery-router
title: "Tool discovery router: expose a shortlist with a full-list fallback"
category: agents
evidence: author-reported
reviewed_on: 2026-09-24
independently_reproduced: false
---

# Tool discovery router: expose a shortlist with a full-list fallback

## What

A Jev router sits before external MCP tool-schema discovery.

## How Jev fits

The agent states a needed capability; Jev compares names and descriptions. A confident selected tool exposes its schema, while uncertainty falls back to the full list. The author describes none-of-the-above, large-inventory tournaments and timeout handling.

## Why and impact

Can reduce the tool surface supplied to a writing model while preserving a recovery path.

## Limits and reuse

Author explicitly had not measured actual token savings or compaction frequency. A shortlist can exclude the needed tool, and a 0.90 threshold is application policy rather than a guarantee. Read-only restrictions, tool permissions and session recovery must be enforced outside the judgment.

## Sources

- [GitHub - jackbarunz/jev-tool-router: Jev-powered MCP tool routing f...](https://github.com/jackbarunz/jev-tool-router) — access: `fetched`; review: `not_reviewed`.
- [https://x.com/Barunz5/status/2101778790103810282?s=20](https://x.com/Barunz5/status/2101778790103810282?s=20) — access: `fetched`; review: `not_reviewed`.
- [https://t.co/aOoAvWIREc](https://t.co/aOoAvWIREc) — access: `not_attempted`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
