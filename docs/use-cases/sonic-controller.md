---
id: sonic-controller
title: "Sonic 3 & Knuckles: paced emulator controller"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Sonic 3 & Knuckles: paced emulator controller

## What

Chalkers shares Jev controlling Sonic 3 & Knuckles.

## How Jev fits

Recorded asynchronous Jev decisions combine cached actions, fallback while waiting, discarded replies and deterministic recovery/heading control around emulator.

## Why and impact

Trace shows movement, rings and score300after restart; illustrates pacing and recovery engineering.

## Limits and reuse

Nineteen sampled frames show bridge failure, death/restart and late stall without levelcompletion. Faster-than-realtime claim not a success-rate benchmark; emulatorFPS and model latency differ. Host recovery and heading repair contribute outcomes.

## Sources

- Discord source — private provenance retained locally.
- [https://x.com/chalkers/status/2100429696941080886?s=46&t=9d3OZDM6CF17OmY-xxEvPg](https://x.com/chalkers/status/2100429696941080886?s=46&t=9d3OZDM6CF17OmY-xxEvPg) — access: `fetched`; review: `demo_trace_reviewed`.
- [https://x.com/chalkers/status/2100466530459017458?s=46&t=9d3OZDM6CF17OmY-xxEvPg](https://x.com/chalkers/status/2100466530459017458?s=46&t=9d3OZDM6CF17OmY-xxEvPg) — access: `fetched`; review: `demo_trace_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
