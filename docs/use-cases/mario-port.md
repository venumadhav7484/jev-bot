---
id: mario-port
title: "Rapid Mario harness port"
category: games
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Rapid Mario harness port

## What

A developer compares building a Jev game controller with their earlier PPO project.

## How Jev fits

Jev replaces a separately trained policy in a game-control experiment.

## Why and impact

Author reports about 30 minutes to build versus a week for the earlier PPO work.

## Limits and reuse

The 100% level-clear figure describes the earlier PPO model, not a verified Jev success rate. Build-time anecdote is not equal-quality benchmarking. Source review: Paused emulator differs from real-time control. Replay patches are not full-run completion or training; movement confidence is not survival probability. Smaller frame intervals increase calls; vanilla SMB1 decoding excludes ROM variants. Keep partial and failed runs visible.

## Sources

- Discord source — private provenance retained locally.
- [https://x.com/shantanugoel/status/2100455779627311352](https://x.com/shantanugoel/status/2100455779627311352) — access: `fetched`; review: `post_text_reviewed_media_pending`.
- [https://t.co/xwGtzkuDpu](https://t.co/xwGtzkuDpu) — access: `fetched`; review: `readme_reviewed`.
- [https://x.com/shantanugoel/status/2100455295801827769](https://x.com/shantanugoel/status/2100455295801827769) — access: `fetched`; review: `post_text_reviewed_media_pending`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
