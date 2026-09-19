---
id: eve-commander
title: "Synthetic EVE-inspired tactical commander"
category: games
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Synthetic EVE-inspired tactical commander

## What

Make group-level tactical judgments above deterministic NPCs.

## How Jev fits

A compact battlefield snapshot feeds sixteen parallel questions; deterministic logic controls around sixty simulated subordinates.

## Why and impact

The author reports 220 live calls, roughly 240 ms median latency from Scotland, and clean one-to-two decisions per second.

## Limits and reuse

Author benchmark not independently reproduced. Cross-field judgments can conflict. Scoped controller inspection: error/empty-answer branch retains last command without current-state target/capacity revalidation; stale-safe fallback is not established. Deterministic comparator is explicitly not ground truth. Existing report timing and consistency failures remain.

## Sources

- [https://github.com/Diabolacal/eo-map-carbon/blob/main/experiments/typesafe/JEV_TACTICAL_COMMANDER.md](https://github.com/Diabolacal/eo-map-carbon/blob/main/experiments/typesafe/JEV_TACTICAL_COMMANDER.md) — access: `fetched`; review: `article_reviewed`.
- [https://github.com/Diabolacal/eo-map-carbon](https://github.com/Diabolacal/eo-map-carbon) — access: `fetched`; review: `readme_reviewed`.
- [Detailed benchmark protocol](https://github.com/Diabolacal/eo-map-carbon/blob/main/experiments/typesafe/COMMANDER_BENCHMARK.md) — discovered via [external source](https://github.com/Diabolacal/eo-map-carbon/blob/main/experiments/typesafe/JEV_TACTICAL_COMMANDER.md); access: `fetched`; review: `sections_reviewed`.
- [Processed benchmark results](https://github.com/Diabolacal/eo-map-carbon/blob/main/experiments/typesafe/commander/summaries/latest.json) — discovered via [external source](https://github.com/Diabolacal/eo-map-carbon/blob/main/experiments/typesafe/JEV_TACTICAL_COMMANDER.md); access: `fetched`; review: `structured_report_reviewed`.
- [Benchmark harness](https://github.com/Diabolacal/eo-map-carbon/tree/main/experiments/typesafe/commander) — discovered via [external source](https://github.com/Diabolacal/eo-map-carbon/blob/main/experiments/typesafe/JEV_TACTICAL_COMMANDER.md); access: `fetched`; review: `scoped_repository_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
