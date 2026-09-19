---
id: sudoku
title: "Sudoku: decisions checked by a solver"
category: games
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Sudoku: decisions checked by a solver

## What

Choose puzzle recipes and digits interactively.

## How Jev fits

Jev selects; a local engine validates each move and verifies puzzle uniqueness.

## Why and impact

Strong composition example: semantic preferences around exact mathematical constraints.

## Limits and reuse

The correctness guarantee belongs to the local checker, not the model's judgment. Media review: Reviewed18 sampled frames: gentle Sudoku fills to81/81 with40moves and10.7s model-time display. Move cards describe only-candidate reasoning and local checking. The host validator, not confidence badges, establishes move legality and puzzle consistency; only one puzzle shown.

## Sources

- Discord source — private provenance retained locally.
- [https://x.com/alexpsouthwell/status/2100543705694560657](https://x.com/alexpsouthwell/status/2100543705694560657) — access: `fetched`; review: `demo_trace_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
