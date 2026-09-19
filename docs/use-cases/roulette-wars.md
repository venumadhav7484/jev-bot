---
id: roulette-wars
title: "Roulette Wars: game playtesting"
category: games
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Roulette Wars: game playtesting

## What

Automate playtests in a fictional betting-based combat game.

## How Jev fits

Jev selects bets from game state. A later update implements a risk-taking score and four player archetypes: fortress, gambler, tactician and wildcard.

## Why and impact

The author reports three recorded wins against a 1000-HP boss in thirteen to fourteen rounds.

## Limits and reuse

Author reports strong action bias: EVEN selected in 65/94 decisions and zero in 8/25 risky bets. Safe and risky bets showed similar confidence near 0.11. Three game wins do not prove randomness, calibration, broad game skill or profitable gambling; collapsed thread sections remain incomplete. Later playtesting exposed an almost unbeatable low-risk strategy; author patched balance so Jev could lose. That supports bug discovery in this game, not gambling profitability. Media review: Reviewed39 sampled frames: risk-match panel updates aggressive/conservative/balanced classifications during human betting and ends with Wildcard profile after five spins. These are game-state interpretations, not psychological validation or Jev winning at gambling. Reviewed40 sampled frames: patched Roulette Wars shows Jev repeatedly choosing EVEN, round-specific focus choices and declining boss HP, but clip ends during round11 without final win/loss. Balance patch is author-reported; sampled trace does not quantify pre/post win-rate or establish random action distribution. Media review: Original accelerated clip repeatedly selects EVEN, reduces boss HP from1000 to18 and later bets zero, but ends mid-round without final win. This supports action bias in this trace; author reports of3/3wins and decision-frequency totals were not independently reproduced.

## Sources

- [https://x.com/NicoSaraintaris/status/2100745151622664392](https://x.com/NicoSaraintaris/status/2100745151622664392) — access: `fetched`; review: `demo_trace_reviewed`.
- [https://x.com/NicoSaraintaris/status/2100962598237749648](https://x.com/NicoSaraintaris/status/2100962598237749648) — access: `fetched`; review: `demo_trace_reviewed`.
- [https://x.com/NicoSaraintaris/status/2100938146175152323](https://x.com/NicoSaraintaris/status/2100938146175152323) — access: `fetched`; review: `demo_trace_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
