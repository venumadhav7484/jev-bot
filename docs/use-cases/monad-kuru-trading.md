---
id: monad-kuru-trading
title: "Monad/Kuru: on-chain trading decision demo"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Monad/Kuru: on-chain trading decision demo

## What

Author reports a bot placing real orders on Kuru’s on-chain order book on Monad.

## How Jev fits

Jev receives an asset-pair price feed and selects buy/sell; host integration submits orders on a reported 300ms block cadence.

## Why and impact

Demonstrates typed decisions connected to transaction execution, not investment returns.

## Limits and reuse

No profitability, risk controls, unbiased backtest or transaction audit established. Never infer predictive edge from execution speed. The fetched demo page was connecting in dry-run mode with no blocks; its standing order forces buy/sell and offers no abstention. This observation does not independently confirm live execution.

## Sources

- Discord source — private provenance retained locally.
- [https://x.com/jarrodwatts/status/2100356151468585346](https://x.com/jarrodwatts/status/2100356151468585346) — access: `fetched`; review: `post_text_reviewed_media_pending`.
- [https://t.co/vwl2SUu4jm](https://t.co/vwl2SUu4jm) — access: `fetched`; review: `source_text_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
