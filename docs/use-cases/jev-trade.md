---
id: jev-trade
title: "Jev Trade: paper-trading loop"
category: finance-experiments
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Jev Trade: paper-trading loop

## What

Expose repeated typed market decisions in a paper desk.

## How Jev fits

Each round supplies book data, recent prints and current position; Jev selects long or short and the desk simulates fills.

## Why and impact

Inspected recording exposes repeated decisions, paper fills, fees, late-call labels and aggregate losses around$29.96–$29.97.

## Limits and reuse

Paper experiment; seven sampled frames are not independently verified PnL or strategy evaluation. Live UI badge does not establish real-money execution. No profitability or risk guarantee.

## Sources

- Discord source — private provenance retained locally.
- [https://x.com/aowang/status/2100770166619652330](https://x.com/aowang/status/2100770166619652330) — access: `fetched`; review: `demo_trace_reviewed`.
- [https://www.jev-trade.com/](https://www.jev-trade.com/) — access: `fetched`; review: `source_text_reviewed`.
- [https://github.com/aowang-ai/jev-trade](https://github.com/aowang-ai/jev-trade) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
