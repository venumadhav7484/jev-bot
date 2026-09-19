---
id: arcade-arena
title: "Nine arcade games: batched parallel decisions"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Nine arcade games: batched parallel decisions

## What

Arcade arena runs nine games with Jev controllers.

## How Jev fits

One API request batches decisions across game states; author reports under $2 per hour. Later update increases claimed parallel batch from nine to 36 games; this means recurring batched decisions, not one call completing entire sessions.

## Why and impact

Illustrates parallel independent questions across multiple simulations.

## Limits and reuse

No quality, throughput or billing protocol inspected; cost depends on cadence and state sizes.

## Sources

- Discord source — private provenance retained locally.
- [https://jev-arena.vercel.app/](https://jev-arena.vercel.app/) — access: `fetched`; review: `source_text_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
