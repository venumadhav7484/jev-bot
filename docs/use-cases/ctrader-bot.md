---
id: ctrader-bot
title: "cTrader: live-account decision integration"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# cTrader: live-account decision integration

## What

Work-in-progress bot connects to a cTrader trading account.

## How Jev fits

Uses previous five-minute and one-hour candles plus context; actions include wait, trail stop, move stop to breakeven, partial close and add positions.

## Why and impact

Demonstrates richer bounded action space than buy/sell.

## Limits and reuse

Author explicitly says forward testing needed. Account connection does not establish live fills, profitability, safe controls or suitability.

## Sources


Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
