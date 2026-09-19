---
id: drone-sim
title: "Jev Drone: MuJoCo autopilot experiment"
category: robotics
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Jev Drone: MuJoCo autopilot experiment

## What

Fly a simulated drone using a judgment loop.

## How Jev fits

The repository preview describes a camera-based MuJoCo environment with Jev in a 2.5 Hz loop.

## Why and impact

The author reports roughly ten cents spent during prototype work.

## Limits and reuse

Camera-based system does not imply native image input to Jev. Perception conversion and control quality need source inspection. README clarifies successful course evidence is one65-second run against three weaker greedy baselines; an earlier matched three-seed comparison showed no advantage. Separate no-reflex tunnel experiment remains unreliable despite21decisions/s throughput and best-run94%target visibility. Source review: Simulation only, no native Jev vision or physical-flight safety proof. Controller repairs, state design, wall-clock pacing and weak baseline confound headline improvements. One successful-looking run is not a matched-seed average; tunnel remains incomplete. Media review: Reviewed 16 sampled frames: simulated drone follows red target between pillars and pipes with depth/free-space and tactical bars. No Slack UI or collision event proof visible; rendering overlap cannot establish hitbox behavior. Existing repository's mixed-baseline and failed tunnel findings still apply.

## Sources

- [https://github.com/RomanSlack/jev-drone](https://github.com/RomanSlack/jev-drone) — access: `fetched`; review: `readme_reviewed`.
- [https://x.com/RomanSlack1/status/2100335978229690683](https://x.com/RomanSlack1/status/2100335978229690683) — access: `fetched`; review: `demo_trace_reviewed`.
- [https://t.co/b2ytFvehTV](https://t.co/b2ytFvehTV) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
