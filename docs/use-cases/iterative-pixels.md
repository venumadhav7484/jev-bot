---
id: iterative-pixels
title: "Iterative pixel-color decisions"
category: creative
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Iterative pixel-color decisions

## What

An experiment repeatedly repaints an image with Jev decisions.

## How Jev fits

Each pixel receives neighbor colors from the previous iteration and a reduced global map as context.

## Why and impact

Recorded32x32palette-choice loop visibly degrades over repeated passes; last sample displays42.06Mtokens,$1.767 and267seconds before final completion.

## Limits and reuse

Twelve sampled frames, UI-reported counters, no independent quality metric or invoice. Ten requested iterations do not mean ten completed passes at last sampled frame. Not native image generation; repeated calls can increase cost while reducing quality.

## Sources

- Discord source — private provenance retained locally.
- [https://x.com/crossiBuilds/status/2100972788164985043](https://x.com/crossiBuilds/status/2100972788164985043) — access: `fetched`; review: `demo_trace_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
