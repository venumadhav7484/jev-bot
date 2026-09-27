---
id: jev-ercot
title: "Texas electricity plans: Jev picks prices from fact labels"
category: domain-review
evidence: author-reported
reviewed_on: 2026-09-27
independently_reproduced: false
---

# Texas electricity plans: Jev picks prices from fact labels

## What

A static site prices every English-language Texas electricity offer for a household from one bill and classifies the fine print.

## How Jev fits

Regexes find candidate spans in each Electricity Facts Label; one request per plan asks about 30 questions, such as which candidate is the energy charge, with a “none” escape so Jev only selects verbatim spans. Sentences are classified into 12 clause families in batches of 25. Code computes bills and checks them against the label’s own price table before trusting them.

## Why and impact

The whole 944-plan corpus costs about $1.40 of Jev and runs in about a minute.

## Limits and reuse

The corpus is frozen at an export date; the author makes no claim about data validity or real savings. The table check catches pricing errors, not every misclassified clause.

## Sources

- [Texas REP Shopper](https://temporary-turbo-nickel-bxyt4z0.vercel.app/) — access: `fetched`; review: `not_reviewed`.
- [GitHub - cdubiel08/jev-ercot: Texas retail electric plan shopper: P...](https://github.com/cdubiel08/jev-ercot) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
