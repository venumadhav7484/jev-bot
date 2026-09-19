---
id: things-vs-stuff
title: "Things versus Stuff: semantic combat rules"
category: games
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Things versus Stuff: semantic combat rules

## What

Decide interactions between user-invented towers and enemies.

## How Jev fits

The inspected README describes about 17 independent questions in one TypeSafe request per new concept, mapped to game statistics. The host handles combat and rendering. Results are cached by day, concept and enemy set, with server-side rate and budget controls.

## Why and impact

Natural-language inventions become gameplay mechanics. The README reports roughly 200 ms per verdict; this was not measured independently.

## Limits and reuse

Players question balance in source replies; semantic plausibility does not guarantee fair mechanics. README exposes decision traces and a headless playtest harness. Live UI confirms a zero-call initial trace and invention controls; no judgment request, balancing experiment or headless harness was executed in this review.

## Sources

- [https://github.com/cpaczek/things-vs-stuff](https://github.com/cpaczek/things-vs-stuff) — access: `fetched`; review: `readme_reviewed`.
- [https://things.iar.dev/](https://things.iar.dev/) — access: `fetched`; review: `demo_trace_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
