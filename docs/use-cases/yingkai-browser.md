---
id: yingkai-browser
title: "Browser automation: LLM planner with paced Jev actions"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Browser automation: LLM planner with paced Jev actions

## What

Browser library, CLI and MCP server from Ying-Kai-Liao/jev-browser.

## How Jev fits

LLM plans; Jev decides bounded actions. Author adds rate limiter because decisions outpace browser readiness and builds for Claude Code.

## Why and impact

Illustrates pacing and observation requirements in fast control loops.

## Limits and reuse

Author explicitly says Jev cannot handle whole workflow alone. No representative task success benchmark.

## Sources

- Discord source — private provenance retained locally.
- [https://github.com/Ying-Kai-Liao/jev-browser/tree/main](https://github.com/Ying-Kai-Liao/jev-browser/tree/main) — access: `fetched`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
