---
id: jev-libero
title: "LIBERO: Jev chooses among physics-previewed robot actions"
category: robotics
evidence: author-reported
reviewed_on: 2026-09-24
independently_reproduced: false
---

# LIBERO: Jev chooses among physics-previewed robot actions

## What

A simulation demo uses Jev to select robot actions in three bundled LIBERO tasks.

## How Jev fits

MuJoCo and collision geometry preview candidate moves. Task-derived state feeds layered choices of intent, motion family and one atomic input; code executes then observes again.

## Why and impact

Saved requests, controls and simulator states make individual episodes inspectable. Author records one successful initial-state example per task.

## Limits and reuse

Simulator previews do substantial physical reasoning; Jev does not infer robot dynamics from images. One seed per task is not a success-rate estimate or evidence for real hardware. Replay/media and full runner were not independently executed.

## Sources

- [Jev × LIBERO — Small decisions. Physical outcomes.](https://dimweaker.github.io/jev-libero/) — access: `fetched`; review: `implementation_report_reviewed`.
- [GitHub - Dimweaker/jev-libero: Fine-grained robot control with Jev,...](https://github.com/Dimweaker/jev-libero) — access: `fetched`; review: `sections_reviewed`.
- [Related public project or article](https://dimweaker.github.io/jev-libero) — discovered via Discord source (private provenance retained locally); access: `fetched`; review: `implementation_report_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
