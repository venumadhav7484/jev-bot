---
id: jev-code
title: "Jev Code: constrained AST construction"
category: experiments
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Jev Code: constrained AST construction

## What

Build small programs through typed choices.

## How Jev fits

Thread discussion describes choosing valid AST nodes, operators and identifiers, updating state and repeating until STOP, then rendering source code.

## Why and impact

Shows how constrained structures can be assembled without ordinary token generation.

## Limits and reuse

Outputs remain simple. The author says the first Hello-world literal might have been hardcoded and earlier character-grid generation worked poorly. Proposed parallel search branches are not demonstrated. Syntactic validity is not program correctness. Source review: Code creation comes from grammar assembly or separate generative candidates, not free-text Jev output. Syntax validity does not imply task correctness. Shell execution needs application permissions; optional generator adds cost. README demo with scripted Jev is not end-to-end live Jev validation.

## Sources

- Discord source — private provenance retained locally.
- [https://github.com/rhighs/jev-code](https://github.com/rhighs/jev-code) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
