---
id: technical-price-signal
title: "Price features: no next-day predictive signal"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Price features: no next-day predictive signal

## What

Author tests whether ticker and historical price indicators predict a positive next-day return.

## How Jev fits

Inputs: dated ticker, 1/5-day return, 20-day volatility/momentum, relative volume and RSI(14). Initial question embeds a more-likely-than-not threshold; participant proposes direct event wording.

## Why and impact

Author reports processing 2,900 days for under $0.01 but no predictive signal, including after wording change.

## Limits and reuse

Screenshot reports SPY next-day AUC about0.508, Brier0.2538, log loss0.7012 and ECE0.0909; calibration bins total550observations, distinct from the author's2900days processed claim. No inspected dataset, baseline, split protocol or cost ledger. Historical leakage and domain calibration remain unresolved. These results do not establish investable prediction.

## Sources

- Discord source — private provenance retained locally.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
