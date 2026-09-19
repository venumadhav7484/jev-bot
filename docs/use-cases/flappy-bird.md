---
id: flappy-bird
title: "Flappy Bird realtime controller"
category: games
evidence: author-reported
reviewed_on: 2026-09-19
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

State representation, score distribution and rate of failed runs are unspecified. Source review: Strong deterministic lookahead/pruning and safety overrides surround Jev. Reported gameplay cannot isolate model advantage; slow API replies remain a documented failure cause. Source review: Jev does not see images or invent trajectories. Deterministic planner does most feasibility work,so gameplay outcome cannotbeascribedtoJev alone. Latency spikes cause losses; comparativebaselineagainstsimulatortoprankmissing. Video itself not inspected.

## Sources

- Discord source — private provenance retained locally.
- [https://x.com/leftspace35/status/2100713588381925520](https://x.com/leftspace35/status/2100713588381925520) — access: `fetched`; review: `post_text_reviewed_media_pending`.
- [https://t.co/KeskDin4pV](https://t.co/KeskDin4pV) — access: `fetched`; review: `readme_reviewed`.
- [Author-linked implementation artifact](https://github.com/leftspace89/JevBird) — discovered via [external source](https://x.com/leftspace35/status/2100713588381925520); access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
