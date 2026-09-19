---
id: ruby-feelings
title: "Feelings: probabilistic conditions in Ruby"
category: developer-tools
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Feelings: probabilistic conditions in Ruby

## What

A Ruby library makes semantic judgments look like conditional expressions.

## How Jev fits

The feels construct wraps typed questions about values, inspired by Probably.

## Why and impact

Reduces repetitive decision-model plumbing for application developers.

## Limits and reuse

Probabilistic conditions should not silently replace deterministic invariants. API behavior and probability calibration were not independently tested. Source review: Ruby conditional ergonomics do not establish calibration on a new application; evaluate thresholds and uncertain branches. Source review: Explicit uncertain branch, bounded loop and recorded responses make probabilistic conditionals auditable. These defaults are library policy, not validated universal thresholds.

## Sources

- [https://github.com/obie/feelings](https://github.com/obie/feelings) — access: `fetched`; review: `readme_reviewed`.
- [https://obiefernandez.com/gems/feelings/](https://obiefernandez.com/gems/feelings/) — access: `fetched`; review: `source_text_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
