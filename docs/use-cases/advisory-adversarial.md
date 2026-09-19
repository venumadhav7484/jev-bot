---
id: advisory-adversarial
title: "Synthetic advisory decisions: representation sensitivity"
category: quality
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Synthetic advisory decisions: representation sensitivity

## What

A preregistered synthetic test probes Choice, Noul and Score.

## How Jev fits

Initial 32 cases are followed by contradictory fields, type changes, reordered inputs and identical repeats.

## Why and impact

Author reports 100% schema validity but imperfect correctness: Choice 11/12, Noul 9/10 and Score MAE 0.569 initially.

## Limits and reuse

Semantically equivalent Noul variants reportedly span 36–62% and cross a 0.50 threshold; identical repeats are more stable. Valid output shape does not guarantee correct decisions. Results not independently reproduced.

## Sources


Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
