---
id: second-thought
title: "Second Thought: terminal command screening"
category: security
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Second Thought: terminal command screening

## What

Warn about risky shell commands before execution.

## How Jev fits

Jev returns allow/warn/block judgments; a local wrapper applies a confidence-based gate.

## Why and impact

The author reports very small per-check model cost and an 85% blocking threshold.

## Limits and reuse

The threshold is application policy, not proof of safety. Never substitute probabilistic screening for sandboxing and explicit execution authority. Source review: Shell mode fails open on unreachable judge; keyless mock is rehearsal, not protection. Agent integration has a different fail-closed contract. Confidence thresholds are not a security proof.

## Sources

- Discord source — private provenance retained locally.
- [https://github.com/rodriveiga01/second-thought](https://github.com/rodriveiga01/second-thought) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
