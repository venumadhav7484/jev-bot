---
id: jevex
title: "Jevex: split ReAct decisions and writing"
category: agents
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Jevex: split ReAct decisions and writing

## What

Reduce generative calls in an agent loop.

## How Jev fits

Jev decides tool selection and loop state. A generative model writes user-facing output and tool arguments when needed.

## Why and impact

The strongest successful reported comparison used two LLM calls instead of five and 77% fewer total LLM input tokens.

## Limits and reuse

Uncached input fell only 17%; caching materially changes the economics. The strongest run is not an average across all workloads. Source review: No LLM control-flow authority does not mean no semantic reasoning in writer. Defaultthreshold notcalibrated,filenameparsermissesspaces,truncationandoutputcapsfail. Scriptedtestsvalidateboundaries not liveaccuracy;READMEestablishes no net token saving and excludesproductioninjectiondefense/writeoperations.

## Sources

- [https://github.com/jvsteiner/jevex](https://github.com/jvsteiner/jevex) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
