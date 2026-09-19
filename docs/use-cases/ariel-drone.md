---
id: ariel-drone
title: "Drone autopilot: Vercel AI SDK simulation"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Drone autopilot: Vercel AI SDK simulation

## What

Ariel Weinberger shares point-to-point drone autopilot with obstacle avoidance.

## How Jev fits

Jev decisions integrated through Vercel AI SDK; GitHub source linked from X post.

## Why and impact

Reported one-trip cost $0.01.

## Limits and reuse

Environment and control boundaries require source inspection; no real-world flight/safety qualification. Distinct from Roman Slack’s MuJoCo prototype. Source review: Code supplies mathematical state and enforces limits. Simulated navigation does not establish physical drone safety or broad success rate. Sampled recording shows simulated takeoff, traversal and descent; last sampled frame remains airborne, so these samples do not establish landed completion.

## Sources

- [https://x.com/arielweinberger/status/2100687687057285215?s=20](https://x.com/arielweinberger/status/2100687687057285215?s=20) — access: `public_media_extracted`; review: `demo_trace_reviewed`.
- [https://t.co/gNQZIbRP7E](https://t.co/gNQZIbRP7E) — access: `fetched`; review: `readme_reviewed`.
- [Author-linked implementation artifact](https://github.com/arielweinberger/jev-autopilot) — discovered via [external source](https://x.com/arielweinberger/status/2100687687057285215); access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
