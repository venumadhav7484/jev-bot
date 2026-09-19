---
id: scripted-robotics-vision-claim
title: "Robotics demo: scripted state mistaken for vision"
category: robotics
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Robotics demo: scripted state mistaken for vision

## What

A PyBullet arm demonstration is presented as raw-RGB, zero-shot Jev perception. Source inspection contradicts that description.

## How Jev fits

The Jev path sends step-indexed text hints, target metadata and current joint positions. The image contributes only its encoded length. Choice selects one of four preset joint trajectories; code builds the displayed reasoning.

## Why and impact

Useful counterexample for separating a working API call from the capability a showcase claims. Scripted progress can make a demo look perceptually grounded without demonstrating image understanding.

## Limits and reuse

Source inspected, not executed. task_completed becomes true on target_acquired OR step >= 4, without independent goal verification; initialization can silently switch to mock. Safety/speed judgments are telemetry in the inspected Jev path, not proven physical safeguards. No native Jev vision, arbitrary motor generation, or safe physical control established. Code: https://github.com/opaielsheikh/zero-shot-vision-robotics/blob/main/vision_robotics/agent.py

## Sources

- Discord source — private provenance retained locally.
- [https://github.com/opaielsheikh/zero-shot-vision-robotics](https://github.com/opaielsheikh/zero-shot-vision-robotics) — access: `fetched`; review: `source_code_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
