---
id: jev-codex-token-saver
title: "Codex investigations: select exact evidence first"
category: retrieval
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Codex investigations: select exact evidence first

## What

An MCP plugin selects bounded excerpts before large search/log results enter an agent’s context.

## How Jev fits

Local tools discover candidates, Jev judges relevance, and code returns exact excerpts with bounded follow-up reads. Small packets bypass Jev; failures use a labeled local fallback.

## Why and impact

Targets the point before context expands. The README reports a controlled 108-run evaluation with lower input-token use and a later correction to its quality rubric.

## Limits and reuse

Earlier pilots were invalidated and preserved. Current savings depend on task, baseline and version; input-token reduction is not automatically cost reduction. Follow-up/recovery limits partly rely on agent guidance. Source/privacy exclusions are not a complete secret detector; no independent reproduction here.

## Sources

- [github.com](https://github.com/jcressler/jev-codex-token-saver) — access: `fetched`; review: `sections_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
