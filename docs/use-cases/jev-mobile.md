---
id: jev-mobile
title: "Jev Mobile: Android observe-decide-act"
category: browser
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Jev Mobile: Android observe-decide-act

## What

Operate Android apps from a high-level goal.

## How Jev fits

OpenClaw supplies goals, Jev selects fast UI actions, ADB/Mobile MCP executes them, and ChatGPT handles free text or complex reasoning when needed.

## Why and impact

Replaces a large model call on every tap with typed decisions and selective escalation.

## Limits and reuse

The post is an author description, not a reproduced task benchmark. Sensitive actions still require application-level authorization. Source review: Reported hardware validation covers narrow Keep/fixture scenarios, not arbitrary Android tasks. Reliability comes from journal/reconciliation and observable verification as well as Jev; optional recovery adds separate LLM cost. Health liveness is distinct from ready device/provider.

## Sources

- Discord source — private provenance retained locally.
- [https://github.com/Friedjof/jev-mobile](https://github.com/Friedjof/jev-mobile) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
