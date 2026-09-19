---
id: monad-kuru-trading
title: "Monad/Kuru: on-chain trading decision demo"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Monad/Kuru: on-chain trading decision demo

## What

Author claims a Jev-driven trading integration with Monad/Kuru; reviewed UI and recording display dry-run mode.

## How Jev fits

Jev receives an asset-pair price feed and selects buy/sell; host integration submits orders on a reported 300ms block cadence.

## Why and impact

Shows rapid bounded buy/sell decisions and a host trading interface; live transaction execution remains unverified.

## Limits and reuse

Recording explicitly says dry run and shows negative simulated P&L around -5.20% to -5.27%, conflicting with the post claim of real orders. No transaction audit, realized return, unbiased backtest or risk-control validation. Forced buy/sell offers no abstention; roughly 100 ms displayed average does not establish predictive edge.

## Sources

- [https://x.com/jarrodwatts/status/2100356151468585346](https://x.com/jarrodwatts/status/2100356151468585346) — access: `public_media_extracted`; review: `demo_trace_reviewed`.
- [https://t.co/vwl2SUu4jm](https://t.co/vwl2SUu4jm) — access: `fetched`; review: `source_text_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
