---
id: robot-arm
title: "SO-101: vision-to-decision robotics simulation"
category: robotics
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# SO-101: vision-to-decision robotics simulation

## What

An SO-101 prototype uses Astra for two camera views, Jev for typed skills and unsafe/done judgments, and a local waypoint controller.

## How Jev fits

Images go to OpenAI; scene JSON and robot state go to TypeSafe. Jev cannot skip controller stages; stale observations cannot start motion.

## Why and impact

The architecture keeps perception, semantic judgments and motion constraints separate, making responsibilities inspectable.

## Limits and reuse

The offline demo is synthetic orchestration, not grasp proof. Physical motion still needs calibration; 30 Hz is a scheduling target, software hold is not an emergency stop, and thresholds are not safety certifications. The first implementation uses taught positions and lacks arbitrary object relocation.

## Sources

- Discord source — private provenance retained locally.
- [https://x.com/ali_uraish/status/2100425130082238682?s=46](https://x.com/ali_uraish/status/2100425130082238682?s=46) — access: `fetched`; review: `post_text_reviewed_media_pending`.
- [SO101 simulation repository](https://github.com/AliUraish/Jev_SO101) — discovered via [external source](https://x.com/ali_uraish/status/2100425130082238682); access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
