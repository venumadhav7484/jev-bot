---
id: alien-embodiment
title: "Simulated alien creature: embodied-agent report"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Simulated alien creature: embodied-agent report

## What

Orin, a simulated underwater predator, chooses actions to find food and avoid starvation.

## How Jev fits

Host sends goals, body conditions and sensory state, pauses the deterministic simulation for Jev, then executes selected swim/whip/eat/rest commands.

## Why and impact

Author reports one run with four meals and 100% energy, roughly 0.7 seconds per decision and four million tokens for $0.16 over two hours.

## Limits and reuse

Changing sensory representation produced a run that avoided walls but starved. Simulation pauses during network calls; proposed local 24 FPS is not measured. Video and code not inspected; no general embodied-agent guarantee.

## Sources

- Discord source — private provenance retained locally.
- [https://x.com/k3o_exp/status/2100065796240073215](https://x.com/k3o_exp/status/2100065796240073215) — access: `fetched`; review: `visible_post_text_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
