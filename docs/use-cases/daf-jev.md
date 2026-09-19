---
id: daf-jev
title: "daf-jev: composable Python decision toolkit"
category: developer-tools
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# daf-jev: composable Python decision toolkit

## What

A Python toolkit wraps Jev with builders, gates, routing, evaluation, calibration, CLI, skill and MCP interfaces.

## How Jev fits

Typed API calls feed reusable decision-composition helpers and concurrent corpus evaluation.

## Why and impact

Authors report up to about 18× batching speedup and fourfold token reduction versus sequential calls in their tests.

## Limits and reuse

Toolkit and paper claims were not independently reproduced. Repeated confidence consistency is not equivalent to calibration against outcomes. Source review: Zenodo abstract reports batching results, but PDF/artifacts require inspection; repeated-confidence consistency is not empirical calibration. Source review: Calibration utilities can accept ground truth, but supplied benchmark does not establish correctness calibration. Default fallback must be chosen per application; never infer API success from exit0 skip. API question/context limits still apply to batches.

## Sources

- [https://github.com/docxology/daf-jev](https://github.com/docxology/daf-jev) — access: `fetched`; review: `readme_reviewed`.
- [https://zenodo.org/records/22817425](https://zenodo.org/records/22817425) — access: `fetched`; review: `provider_listing_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
