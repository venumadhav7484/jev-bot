---
id: priorbench-jev
title: "PriorBench: a pre-registered evaluation of Jev"
category: experiments
evidence: author-reported
reviewed_on: 2026-09-27
independently_reproduced: false
---

# PriorBench: a pre-registered evaluation of Jev

## What

An independent, pre-registered evaluation ran 5,721 calls across 21 experiments for $0.176 through a gateway.

## How Jev fits

Fifty predictions were registered before running; experiments cover latency, zero-shot accuracy, thresholds, out-of-scope inputs, criteria wording and concurrency.

## Why and impact

Zero-shot accuracy was 95.9% on a 400-item benchmark (77.2% for keywords, 66.0% for supervised TF-IDF); 800 judgments in one call took 985 ms. Without an explicit "none of these" option, 0 of 30 out-of-scope messages were flagged, all at 0.99 confidence. Wrong criteria descriptions dropped accuracy to 16.7%.

## Limits and reuse

Gateway-measured latency (~430 ms floor) is higher than direct-API reports. Its threshold finding (flat to 0.95, 100% at 0.99) did not transfer to another team's adjudication task, whose curve peaked at 0.90: thresholds are task-specific.

## Sources

- [GitHub - priorbench/jev: Independent, pre-registered evaluation of ...](https://github.com/priorbench/jev) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
