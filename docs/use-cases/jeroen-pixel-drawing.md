---
id: jeroen-pixel-drawing
title: "Pixel drawing: Jev and Haiku comparison"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Pixel drawing: Jev and Haiku comparison

## What

Experiment renders pictures through pixel-by-pixel decisions.

## How Jev fits

Host turns model-selected pixel values into images and compares Jev with Claude Haiku.

## Why and impact

Caption reports Jev only slightly faster.

## Limits and reuse

Video explicitly compares a completed 4,047-pixel Jev coloring with Haiku's 300-pixel sample, extrapolating remaining runtime. Reported ~107x is not two completed equal-workload runs. Jev nearest-color agreement 98.2% versus Haiku sample 100% uses different denominators. No native image generation or independent cost/latency reproduction.

## Sources

- Discord source — private provenance retained locally.
- [https://x.com/j_lamberts/status/2100577481698734255?s=20](https://x.com/j_lamberts/status/2100577481698734255?s=20) — access: `fetched`; review: `demo_trace_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
