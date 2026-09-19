---
id: mario-memory
title: "Mario controller using NES memory"
category: games
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Mario controller using NES memory

## What

A Mario experiment drives gameplay with Jev.

## How Jev fits

Reads structured NES memory rather than pixels and asks one action question: run, hop, jump, wait or go back.

## Why and impact

Author reports clearing level 1-1 in 193 calls.

## Limits and reuse

Specific run claim only. Environment memory access and action timing materially affect the result; this does not show native vision. The author explicitly pauses the game during inference: 193 calls at roughly 300ms cleared World 1-1. Video game speed must not be described as wall-clock speed. Media review: Reviewed 15 sampled frames: Mario reaches flag, level-clear banner at 193 decisions, then World 1-2. Inspector reports average 323 ms/call. This supports this recorded run, not continuous real-time play: game pauses for inference, and structured NES memory supplies state.

## Sources

- [https://x.com/rherton/status/2101005942913729001?s=20](https://x.com/rherton/status/2101005942913729001?s=20) — access: `fetched`; review: `demo_trace_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
