---
id: sat-unsat-advisory
title: "SAT/UNSAT: advisory judgments compared with Z3"
category: quality
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# SAT/UNSAT: advisory judgments compared with Z3

## What

Screenshot reports a small comparison of TypeSafe judgments with Z3 satisfiability results.

## How Jev fits

Six examples span easy formulas, pigeonhole cases and quantified arithmetic. Full questions and code are not visible.

## Why and impact

Report claims agreement across six rows, with Z3 faster on easy cases and TypeSafe faster on harder cases including one timeout. Potential triage signal before exact checking.

## Limits and reuse

Assistant-generated report screenshot, not reproduced logs. It explicitly calls answers advisory rather than kernel proof. No proof certificates, representative test set or timing fairness audit. Never treat probabilistic SAT/UNSAT judgments as formal verification.

## Sources

- Discord source — private provenance retained locally.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
