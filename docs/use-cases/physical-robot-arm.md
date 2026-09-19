---
id: physical-robot-arm
title: "Physical robotic arm: reported zero-shot control"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Physical robotic arm: reported zero-shot control

## What

Author reports Jev participating in control of a physical robotic arm, outside simulation.

## How Jev fits

Follow-up clarifies that another model orchestrates and supplies constant positional feedback; Jev operates around one request per second.

## Why and impact

Extends community evidence beyond simulator-only reports.

## Limits and reuse

No verified low-level controller, success distribution, autonomy scope or safety protocol. Zero-shot does not mean Jev-only perception or execution. Media review: Reviewed physical-arm recording's 16 sampled frames: gripper moves among colored objects and yellow object ends near orange. No instruction, API trace, or repeated-trial denominator visible; exact task success cannot be judged. Another model provides orchestration/position feedback per author reply; not Jev-only raw perception.

## Sources

- [https://x.com/zaidbul/status/2100949713138729135](https://x.com/zaidbul/status/2100949713138729135) — access: `fetched`; review: `demo_trace_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
