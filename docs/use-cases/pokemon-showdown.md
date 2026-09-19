---
id: pokemon-showdown
title: "Competitive Pokémon: bounded battle choices"
category: games
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Competitive Pokémon: bounded battle choices

## What

Choose battle actions against another model.

## How Jev fits

Host enumerates legal battle moves, switches and Terastallization options; one Jev Choice question selects an action and exposes a probability distribution. Recorded 33-turn battle ends in a Jev win.

## Why and impact

The author reports Jev winning one game with $0.0029 and 37 seconds thinking, versus Opus $2.35 and 6m29s.

## Limits and reuse

One accelerated random battle cannot establish relative strategic strength. Final video card reports $0.0029/37s thinking versus $2.35/6m39s; these are creator telemetry, not independently reproduced billing or end-to-end timings. Its 824x claim is not recoverable exactly from rounded displayed costs. Opponent configuration and randomized teams confound comparisons.

## Sources

- Discord source — private provenance retained locally.
- [https://x.com/sid19arya0/status/2100458351440048258?s=20](https://x.com/sid19arya0/status/2100458351440048258?s=20) — access: `fetched`; review: `demo_trace_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
