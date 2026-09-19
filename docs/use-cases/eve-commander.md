---
id: eve-commander
title: "Synthetic EVE-inspired tactical commander"
category: games
evidence: author-reported
reviewed_on: 2026-09-19
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

Not an integration running NPCs inside EVE Frontier. Reinforcement overuse, reluctance to select no target and inconsistent danger/posture judgments were reported. Source review: Do not describe Jev as controlling EVE/Carbon gameplay. Numeric battlefield benchmark and deterministic subordinate logic are separate from live game integration; metrics need detailed reports. Source inspection here covers README, not reproduced renderer or commander run. Source review: Synthetic commander study, not native game NPC deployment or live combat win rate. Code overrides ambiguous/unsafe outputs; no-pressure reinforcement still wrong. Stable choices are not correctness; continuous5/10Hz unsustainable in measured sequential setup and event-driven savings only estimates.

## Sources

- Discord source — private provenance retained locally.
- [https://github.com/Diabolacal/eo-map-carbon/blob/main/experiments/typesafe/JEV_TACTICAL_COMMANDER.md](https://github.com/Diabolacal/eo-map-carbon/blob/main/experiments/typesafe/JEV_TACTICAL_COMMANDER.md) — access: `fetched`; review: `article_reviewed`.
- [https://github.com/Diabolacal/eo-map-carbon](https://github.com/Diabolacal/eo-map-carbon) — access: `fetched`; review: `readme_reviewed`.
- [Detailed benchmark protocol](https://github.com/Diabolacal/eo-map-carbon/blob/main/experiments/typesafe/COMMANDER_BENCHMARK.md) — discovered via [external source](https://github.com/Diabolacal/eo-map-carbon/blob/main/experiments/typesafe/JEV_TACTICAL_COMMANDER.md); access: `fetched`; review: `sections_reviewed`.
- [Processed benchmark results](https://github.com/Diabolacal/eo-map-carbon/blob/main/experiments/typesafe/commander/summaries/latest.json) — discovered via [external source](https://github.com/Diabolacal/eo-map-carbon/blob/main/experiments/typesafe/JEV_TACTICAL_COMMANDER.md); access: `fetched`; review: `structured_report_reviewed`.
- [Benchmark harness](https://github.com/Diabolacal/eo-map-carbon/tree/main/experiments/typesafe/commander) — discovered via [external source](https://github.com/Diabolacal/eo-map-carbon/blob/main/experiments/typesafe/JEV_TACTICAL_COMMANDER.md); access: `fetched`; review: `metadata_only`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
