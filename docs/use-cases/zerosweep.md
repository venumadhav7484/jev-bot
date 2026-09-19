---
id: zerosweep
title: "ZeroSweep: email triage benchmark demo"
category: content
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# ZeroSweep: email triage benchmark demo

## What

A developer demo compares Jev-driven email triage against an LLM workflow.

## How Jev fits

The author describes a confidence-gated triage engine; the repository post uses an 85% gate.

## Why and impact

Demonstrates typed triage and uncertain-case handling as an alternative to parsing generated responses.

## Limits and reuse

Demo claims are not production accuracy evidence. A numeric probability threshold needs calibration against labeled examples and missed-important-mail costs. Source review: Captured mailbox is empty and backend still checking; advertised latency and schema figures are not verified measured results. Source review: Synthetic inbox and workload-dependent timings cannot establish enterprise accuracy or universal speedup. Confidence>=.85 is not85%correctness or verified safe deletion. Envoy upstream time includes upstream processing beyond pure inference. Model size, pricing tiers and impossible-malformed-JSON claims remain unsupported promotional assertions; no mailbox actions performed.

## Sources

- Discord source — private provenance retained locally.
- [https://sysadarsh-zerosweep.vercel.app/](https://sysadarsh-zerosweep.vercel.app/) — access: `fetched`; review: `source_text_reviewed`.
- [https://sysadarsh-zerosweep.vercel.app//](https://sysadarsh-zerosweep.vercel.app//) — access: `fetched`; review: `source_text_reviewed`.
- [https://github.com/sysadarsh/zerosweep](https://github.com/sysadarsh/zerosweep) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
