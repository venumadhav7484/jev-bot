---
id: doom-launch
title: "Doom: launch demonstration"
category: games
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Doom: launch demonstration

## What

Control a Doom player in real time.

## How Jev fits

The author built on ViZDoom. The discussion describes remembered item locations and a tactical decision layer; game state is supplied through a harness.

## Why and impact

The launch post reports about ten calls per second and roughly $7 per hour.

## Limits and reuse

Structured game state comes from a harness; no native image input established. Vendor recording shows Jev decision inspector; separately linked game-wrapper code alone does not prove Jev integration. No general gameplay benchmark reproduced. Media review: Vendor recording shows structured health/enemy/projectile state, typed tactical decisions and changed behavior after do-not-fire/dodge instruction. Vertical aiming is automatic in the harness. Later exploration reaches an exit-door button, without a level-completion banner. About100ms per question battery/10Hz is narrated, not independently measured; no win-rate or hourly-cost reproduction.

## Sources

- Discord source — private provenance retained locally.
- [https://x.com/CompleteSkeptic/status/2099925687465570372](https://x.com/CompleteSkeptic/status/2099925687465570372) — access: `fetched`; review: `demo_trace_reviewed`.
- [https://github.com/robault/skilldoom](https://github.com/robault/skilldoom) — access: `fetched`; review: `context_only_not_jev_evidence`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
