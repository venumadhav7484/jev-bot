---
id: symbolic-integration-routing
title: "Symbolic integration: choosing candidate techniques"
category: experiments
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Symbolic integration: choosing candidate techniques

## What

A playground experiment proposes using Jev to guide SymPy integration strategy.

## How Jev fits

Text state supplies an expression and variable; separate typed questions judge existence of an elementary antiderivative, choose an integration technique and score algebraic complexity. SymPy integration and exact verification remain external responsibilities.

## Why and impact

Possible use of semantic routing before an exact solver. Screenshot gives72% elementary-antiderivative signal and favors u-substitution65% over integration-by-parts21%; these are model outputs, not mathematical proof.

## Limits and reuse

Proposed SymPy integration, not demonstrated speedup. No completed solver integration, correctness proof or timing comparison visible. Complexity score2.56/4 andconfidence41% are heuristic signals. Never replace deterministic symbolic checks with these judgments.

## Sources

- Discord source — private provenance retained locally.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
