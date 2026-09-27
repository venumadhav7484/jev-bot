---
id: jevfend-word-count
title: "Jevfend: a “Jev confidence” that tracked word count"
category: limitations
evidence: author-reported
reviewed_on: 2026-09-27
independently_reproduced: false
---

# Jevfend: a “Jev confidence” that tracked word count

## What

A third-party tester probed an architecture-defence simulator that reports a verdict with “Jev confidence”.

## How Jev fits

The tester removed each of five sections, doubled the length, and replaced all content with filler of the same length. Every variant returned byte-identical scores; only truncating to about 70 words flipped the verdict. The panel showed “Demo Simulation Mode (Local Heuristics)” under the model name.

## Why and impact

A useful audit pattern: vary the substance while holding length fixed, and check whether the number moves. Here it did not, and the tool itself indicated local heuristics were in use.

## Limits and reuse

One tester’s report of one product in demo mode; it is not evidence about Jev itself and may reflect that Jev was not called. The product page reviewed does not describe the scoring method.

## Sources

- [Simul | The Soft Skills Simulator for Career & Family](https://getsimul.com/) — access: `fetched`; review: `landing_page_reviewed`.
- [Jevfend — Defend Your Architecture Using Jev | Free FDE Tool by S...](https://getsimul.com/tools/jevfend) — access: `fetched`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
