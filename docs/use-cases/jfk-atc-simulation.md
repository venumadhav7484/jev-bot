---
id: jfk-atc-simulation
title: "JFK simulation: voice agents with ATC decision checks"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# JFK simulation: voice agents with ATC decision checks

## What

Airport simulation combines pilot and air-traffic-controller voice agents with Jev decisions.

## How Jev fits

GPT realtime voice supplies conversation; Jev handles ATC choices and traffic conflicts over structured simulation state.

## Why and impact

Illustrates separating voice generation from bounded simulation decisions.

## Limits and reuse

Simulator only; no conflict-detection evaluation or real aviation validation. Media review: Reviewed full narration and opening/middle/final frame samples. JFK simulation uses JSON airport/aircraft state for clearances/conflict choices, separate voice models for radio. Visible simulator and inspector run; author says20–30minutes without conflict, but clip does not establish that duration or conflict-detection reliability. Later Agent Zero example returns billing/refund/urgency typed judgments. Neither is aviation safety validation.

## Sources

- [https://x.com/alessandro_a0/status/2100573356294607245?s=20](https://x.com/alessandro_a0/status/2100573356294607245?s=20) — access: `fetched`; review: `demo_trace_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
