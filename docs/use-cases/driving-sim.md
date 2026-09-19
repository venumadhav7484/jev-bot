---
id: driving-sim
title: "Structured-state driving simulation"
category: robotics
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Structured-state driving simulation

## What

Choose driving behavior in a simulated road environment.

## How Jev fits

Structured sensor state feeds typed decisions about steering, braking, overtaking, pedestrians and speed limits.

## Why and impact

The author reports about 300 ms decision latency.

## Limits and reuse

A simulator is not validated autonomous driving. Exact control, timing and safety constraints cannot be delegated to this demonstration. Source review: Requested camera coverage does not establish native Jev vision. This document is a specification, not proof of successful driving, overtaking or pedestrian safety. Media review: Reviewed34 sampled frames: car follows, overtakes, returns lane and slows around crossing/speed-limit changes, with typed maneuver and radar-state inspector. No crash/outcome report or physical-road evaluation. Camera thumbnails in UI do not prove native image input; autonomous-driving safety cannot be inferred from one scripted simulator trace.

## Sources

- Discord source — private provenance retained locally.
- [https://x.com/kavehmz/status/2100616111771238881](https://x.com/kavehmz/status/2100616111771238881) — access: `fetched`; review: `demo_trace_reviewed`.
- [Author-linked implementation artifact](https://github.com/kavehmz/typesafe-playground/blob/main/driving-simultion.md) — discovered via [external source](https://x.com/kavehmz/status/2100616111771238881); access: `fetched`; review: `proposal_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
