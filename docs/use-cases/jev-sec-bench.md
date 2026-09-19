---
id: jev-sec-bench
title: "Security corpus classification benchmark"
category: security
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Security corpus classification benchmark

## What

Evaluate prompt-injection detection on public data.

## How Jev fits

The author uses a Go client and publishes benchmark code for two safety corpora.

## Why and impact

The post reports 96.5% accuracy on 662 deepset/prompt-injections messages without tuning and 325 ms p50.

## Limits and reuse

Public benchmark accuracy does not establish resistance to new adaptive attacks or safe autonomous execution.

## Sources

- [https://x.com/_GauravGosain/status/2100111398277959715?s=20](https://x.com/_GauravGosain/status/2100111398277959715?s=20) — access: `fetched`; review: `context_only_reviewed`.
- [https://github.com/Gaurav-Gosain/jev-sec-bench](https://github.com/Gaurav-Gosain/jev-sec-bench) — access: `fetched`; review: `source_text_reviewed`.
- [Author-linked implementation artifact](https://github.com/Gaurav-Gosain/jev-go) — discovered via [external source](https://x.com/_GauravGosain/status/2100111398277959715); access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
