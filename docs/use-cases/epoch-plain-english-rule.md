---
id: epoch-plain-english-rule
title: "Epoch: a trading entry rule restated in plain English"
category: finance-experiments
evidence: author-reported
reviewed_on: 2026-09-27
independently_reproduced: false
---

# Epoch: a trading entry rule restated in plain English

## What

A backtesting platform replaced a coded entry function with a plain-English rule evaluated by Jev.

## How Jev fits

The rule: enter QQQ when the close is above its 200-day average, RSI(2) is below 20 and ADX(14) is below 25. Epoch built the features and Jev evaluated one row at a time; exits, holding periods and execution stayed in code.

## Why and impact

Across 752 sessions Jev matched every entry decision of the coded rule at about 255 ms per request, and the backtest matched exactly.

## Limits and reuse

Rule-following parity on precomputed features, not trading skill; the same author reported poor results when Jev made the trading decision itself. Numeric comparisons are exactly what code does more cheaply and reliably.

## Sources

- [We replaced a trading entry function in Epoch with a plain-English ...](https://lnkd.in/p/gJbWhAvP) — access: `fetched`; review: `post_text_reviewed`.
- [dms.licdn.com](https://dms.licdn.com/playlist/vid/v2/D5605AQHQCfPKjf0DFg/thumbnail-with-play-button-overlay-high/B56aDU2fvoH0C0-/0/1790277453393?e=2147483647&v=beta&t=LVl7GBw6tBkjDN70IEa3CEsNUgR2PNwj5p6S5MF50cI) — access: `not_attempted`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
