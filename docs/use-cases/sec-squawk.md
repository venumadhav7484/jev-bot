---
id: sec-squawk
title: "SEC filings: semantic event screening"
category: finance-experiments
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# SEC filings: semantic event screening

## What

Detect filing events and changes for a market-information feed.

## How Jev fits

Jev classifies signals such as buybacks, insider trades and meaningful quarter-over-quarter differences from supplied filings.

## Why and impact

Author reports approximately $2.75 for quarter-over-quarter comparisons across 100 companies and $0.15/day for filings across a roughly 1,000-company watchlist. These are workload-specific costs; separate LLM analysis remains necessary.

## Limits and reuse

Event detection is separate from price prediction. No labeled evaluation or complete filing coverage was supplied.

## Sources

- [https://x.com/Anot/status/2100425243269468583](https://x.com/Anot/status/2100425243269468583) — access: `fetched`; review: `visible_post_text_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
