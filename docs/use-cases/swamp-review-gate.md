---
id: swamp-review-gate
title: "Swamp: conditional software-review gate"
category: Developer tooling
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Swamp: conditional software-review gate

## What

A TypeSafe extension for Swamp and a software-factory review trigger.

## How Jev fits

Author describes combining touched-filepath rules with a Noul response below 0.8 before running a review. The exact Noul proposition is absent, so threshold direction cannot be reused safely without the question.

## Why and impact

A semantic decision can gate expensive reviews after deterministic path filtering. No measured cost saving or missed-defect rate is supplied.

## Limits and reuse

Published extension plus author report; no reproduced trial. Question wording, polarity, threshold calibration and false-negative cost must be established before automation. Source review: Resource logging includes evaluated state; handle retention deliberately. Registry quality score does not establish inference correctness; retries can add calls.

## Sources

- [https://swamp-club.com/extensions/@swamp/typesafe-ai](https://swamp-club.com/extensions/@swamp/typesafe-ai) — access: `fetched`; review: `source_text_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
