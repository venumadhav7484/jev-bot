---
id: tool-door-handoff
title: "Tool doors: bounded dispatch around a generative planner"
category: agents
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Tool doors: bounded dispatch around a generative planner

## What

Architecture separates model planning, typed tool choices and execution.

## How Jev fits

Generative model supplies intent and open text; Jev chooses a tool door and enumerated knobs, with a gate. Low certainty returns to model/human; code owns thresholds, execution and MCP dispatch.

## Why and impact

Reusable pattern for narrow decisions without asking Jev to author arbitrary commands.

## Limits and reuse

Diagram only; no implementation audit or security evaluation. Diagram wording conflates Noul probability with confidence; preserve primitive semantics in actual code. Scores cannot replace authorization.

## Sources


Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
