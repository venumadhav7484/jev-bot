---
id: jevrouter
title: "JevRouter: tool shortlist"
category: agents
evidence: author-reported
reviewed_on: 2026-09-24
independently_reproduced: false
---

# JevRouter: tool shortlist

## What

JevRouter proposes routing among models, tools and subagents with Jev.

## How Jev fits

Its benchmark compares Jev serial routing against DeepSeek V4.1 Flash on first-five-tool-call predictions for ten tasks.

## Why and impact

The page reports 38% position-wise hits versus 24% baseline, 1.58 versus 8.65 seconds per task and lower estimated cost.

## Limits and reuse

The headline 99.97% token saving is explicitly directional and workflow-dependent; it compares a different baseline from the tool-call benchmark. September 24 README adds mixed-primitive evaluation, sequence search, explicit decision receipts and execution feedback. Its decompose/thread configuration reports 44% positional tool hits on the cited small routing evaluation; this remains distinct from end-to-end task success. The dashboard correctly leaves outcomes uncollected until host feedback exists. Repeated announcements and repository stars do not add independent validation.

## Sources

- [http://jevrouter.co/](http://jevrouter.co/) — access: `fetched`; review: `source_text_reviewed`.
- [https://github.com/BillionsBobby/JevRouter](https://github.com/BillionsBobby/JevRouter) — access: `fetched`; review: `sections_reviewed`.
- [JevRouter — Faster Agent Decisions](https://www.jevrouter.co/) — access: `fetched`; review: `duplicate_landing_page`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
