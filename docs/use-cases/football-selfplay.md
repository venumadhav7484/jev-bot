---
id: football-selfplay
title: "Football self-play"
category: games
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Football self-play

## What

Two Jev-controlled players compete in a football-game prototype.

## How Jev fits

Each controller selects actions; both input feeds are visible in the shared demo. Only one player slot per side is Jev-controlled; remaining teammates use ordinary game AI. Host calculates reachable passes and exact aim/power.

## Why and impact

Preview reports ten completed passes and a touchdown.

## Limits and reuse

First test only; future CPU-player integration is a plan. No broad game-skill result. Initial controller completed zero passes; action-space and catch-facing changes preceded the reported 6/8 and 4/6 passes across 246 calls averaging 234ms. Media review: Reviewed63 sampled frames. False Start match shows both typed input panels, passing, catches, incomplete passes and final Red Zone win6–0. Only one controlled slot per side; ordinary game AI controls teammates and host computes reachable passes/aim. Single self-play result does not isolate model skill or independently verify aggregate pass/call statistics.

## Sources

- Discord source — private provenance retained locally.
- [https://x.com/attractmodeio/status/2100723340021276739?s=46&t=Lue6-owbwjO2j3Lmk4ra-A](https://x.com/attractmodeio/status/2100723340021276739?s=46&t=Lue6-owbwjO2j3Lmk4ra-A) — access: `fetched`; review: `demo_trace_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
