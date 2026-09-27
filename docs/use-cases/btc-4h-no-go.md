---
id: btc-4h-no-go
title: "BTC four-hour direction: a pre-registered NO-GO"
category: finance-experiments
evidence: author-reported
reviewed_on: 2026-09-27
independently_reproduced: false
---

# BTC four-hour direction: a pre-registered NO-GO

## What

A pre-registered test asked Jev whether the next four-hour BTC candle goes up or down, with ten indicator values as state.

## How Jev fits

One Choice per bar; a long-only rule entered at p_up ≥ 0.65 and exited at ≤ 0.50. Data were split in time, windows chosen on development data only, five gates fixed in advance, and a shuffled-input control used the same ids and labels.

## Why and impact

NO-GO: high-confidence accuracy was 48.9% (n=1,539) against 51.7% for the shuffled control; mean stated confidence 78.7% against 49.1% accuracy. An outside review recomputed the numbers and found a reporter bug that did not change the verdict.

## Limits and reuse

One asset, one horizon and numeric state. The author proposes a shared bench for other framings (Jev as a filter on an existing signal, text state, longer horizons). Counterevidence, not a trading method.

## Sources

- [development-debugging-logbook/case-005-jev-btc-classifier-no-go.md ...](https://github.com/martinzzpmaatschap/development-debugging-logbook/blob/main/case-005-jev-btc-classifier-no-go.md) — access: `fetched`; review: `report_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
