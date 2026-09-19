---
id: feed-materiality
title: "Public-feed materiality classification"
category: finance-experiments
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Public-feed materiality classification

## What

Classify SEC, supply-chain and news events in an event-driven pipeline.

## How Jev fits

Choice and Noul map text to typed operational signals; downstream rules consume explicit probability thresholds.

## Why and impact

The author reports hundreds of cycles without parsing failures and 600–900 ms roundtrips.

## Limits and reuse

Schema validity does not establish semantic accuracy. In Python, a nonempty answer dictionary is truthy; extract its Noul value before thresholding.

## Sources

- Discord source — private provenance retained locally.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
