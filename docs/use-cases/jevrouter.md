---
id: jevrouter
title: "JevRouter: tool shortlist"
category: agents
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# JevRouter: tool shortlist

## What

Shortlist tools for an agent.

## How Jev fits

Jev supplies Choice distributions over capabilities; host policy filters permissions, risk, availability and confirmation without renormalizing those distributions. Low confidence can return no_decision. Serial, batched and externally decomposed plans have different costs and dependencies.

## Why and impact

README reports first-five-tool prediction on ten Toolathlon tasks: 38% serial or 44% decomposed position hits versus 24% comparator. Serial took 1.58s versus 8.65s; decomposed took 10.6s.

## Limits and reuse

Ordered tool prediction is not end-to-end task completion. Do not combine decomposed accuracy with serial speed into one result. No independent run, code audit or host-compatibility validation.

## Sources

- Discord source — private provenance retained locally.
- [http://jevrouter.co/](http://jevrouter.co/) — access: `fetched`; review: `not_reviewed`.
- [https://github.com/BillionsBobby/JevRouter](https://github.com/BillionsBobby/JevRouter) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
