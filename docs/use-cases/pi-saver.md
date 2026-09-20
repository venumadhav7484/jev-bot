---
id: pi-saver
title: "Pi-Saver: reversible context filtering"
category: retrieval
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Pi-Saver: reversible context filtering

## What

Filter older conversation turns before inference while retaining local history.

## How Jev fits

Jev scores complete turn groups for relevance. Code protects current turns and instruction/summary content, removes eligible low-scoring groups, and keeps failed batches.

## Why and impact

Shows reversible evidence filtering with observe/active modes instead of destructive history rewriting.

## Limits and reuse

The advertised reduction measures normalized text length, not tokens or billing. Retained disk history does not prove needed context remains in a particular model call. Image placeholders lack visual content, and privacy and cache effects require evaluation.

## Sources

- [github.com](https://github.com/amazingjoe/pi-saver) — access: `fetched`; review: `sections_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
