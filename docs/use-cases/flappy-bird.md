---
id: flappy-bird
title: "Flappy Bird realtime controller"
category: games
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Flappy Bird realtime controller

## What

A clone uses Jev to control the bird.

## How Jev fits

Jev repeatedly selects actions during gameplay.

## Why and impact

Demonstrates short-latency control in a simple environment.

## Limits and reuse

Strong deterministic lookahead, candidate pruning and safety overrides surround Jev. No independent comparison against the simulator-only top-ranked action; latency spikes remain a documented failure cause. Media review: Recording reaches score97 then Game Over around150s and restarts. HUD shows13 safety-flap saves,89calls and off6 at game-over; terminal shows a request timeout around restart. Host simulator ranks candidate trajectories and supplies safety overrides. This is not97pipes attributable to Jev alone; precise cause of loss and score distribution remain unverified.

## Sources

- [https://x.com/leftspace35/status/2100713588381925520](https://x.com/leftspace35/status/2100713588381925520) — access: `fetched`; review: `demo_trace_reviewed`.
- [https://t.co/KeskDin4pV](https://t.co/KeskDin4pV) — access: `fetched`; review: `readme_reviewed`.
- [Author-linked implementation artifact](https://github.com/leftspace89/JevBird) — discovered via [external source](https://x.com/leftspace35/status/2100713588381925520); access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
