---
id: toolgate
title: "toolgate: tool-call risk policy"
category: security
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# toolgate: tool-call risk policy

## What

A hook or MCP proxy applies policy before coding-agent tool calls.

## How Jev fits

Static rules run first, then parallel Jev risk questions and authorization context feed deterministic allow, ask and deny rules. Missing model service defaults to asking; unattended asks can become denies.

## Why and impact

The README documents real false positives and policy changes, including truncated task context and legitimate server shutdowns being blocked.

## Limits and reuse

Not a sandbox or complete injection defense. The initial 151-decision usage report had a 40% ask rate; small frozen challenge sets do not establish broad reliability. Redaction can miss secrets, multi-step attacks remain a gap, and reported performance varies by version and network.

## Sources

- [github.com](https://github.com/RiskAverseTech/toolgate) — access: `fetched`; review: `sections_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
