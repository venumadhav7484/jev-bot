---
id: btc-direction-experiment
title: "BTC direction: multi-horizon exploratory probabilities"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# BTC direction: multi-horizon exploratory probabilities

## What

Experiment continuously predicts Bitcoin direction over several timeframes.

## How Jev fits

Supplies fixed market data from Binance and requests Jev probabilities. Author considers decomposed feature questions with host-side weighting as future work.

## Why and impact

Public demo and repository enable investigation. Author notices high certainty on longer horizons but supplies no calibrated outcome analysis.

## Limits and reuse

Author says prior backtests were biased and logging is still being built. Live public page on review date waits for its first forecast, providing no performance data. README establishes no predictive advantage; different quote assets and overlapping legacy forecasts must not be pooled indiscriminately. Jev confidence is distribution concentration, not forecasting validity. App never prepares or places trades.

## Sources

- Discord source — private provenance retained locally.
- [https://lab.rokogrga.com/btc-jev](https://lab.rokogrga.com/btc-jev) — access: `fetched`; review: `demo_interface_reviewed`.
- [https://github.com/WebGrga/btc-jev-signal](https://github.com/WebGrga/btc-jev-signal) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
