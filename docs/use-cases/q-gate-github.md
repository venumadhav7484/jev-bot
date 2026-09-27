---
id: q-gate-github
title: "Q-GATE: typed decisions for issues, pull requests and commits"
category: quality
evidence: author-reported
reviewed_on: 2026-09-27
independently_reproduced: false
---

# Q-GATE: typed decisions for issues, pull requests and commits

## What

An open-source quality gate turns repository activity into auto-approved, needs-review or blocked decisions.

## How Jev fits

Jev and a heuristic evaluator both assess the issue, pull request or commit; a deterministic policy layer decides, humans review, and the tool tracks agreement and false-approval calibration, supports shadow mode and simulates policy changes on past runs.

## Why and impact

Shadow mode and policy simulation let a team measure the model before it changes live decisions.

## Limits and reuse

Author project; no accuracy figures published. Falls back to heuristics when Jev is unavailable.

## Sources

- [GitHub - Bnymn1306/jev-github-quality-gate: A Jev-powered quality g...](https://github.com/Bnymn1306/jev-github-quality-gate) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
