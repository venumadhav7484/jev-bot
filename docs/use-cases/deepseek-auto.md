---
id: deepseek-auto
title: "DeepSeek harness automatic-choice plugin"
category: agents
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# DeepSeek harness automatic-choice plugin

## What

A plugin lets Jev answer next-action and multiple-choice prompts in an agent harness.

## How Jev fits

Generative model extracts end-prompt questions; Jev answers bounded questions and autonomy predicate; code applies thresholds and three-decision turn budget. Separate tool-question path can return one selection.

## Why and impact

Intended to reduce unattended-run interruptions.

## Limits and reuse

README explicitly says no sandbox/no approval and gate governs questions, not tool calls. Fail-closed question review is not permission enforcement. Small author prompt tests and model-assisted threshold selection do not validate security; merge-to-main is borderline. No installation or execution performed.

## Sources

- [https://git.allen-software.com/allenh1/dsh-auto-mode](https://git.allen-software.com/allenh1/dsh-auto-mode) — access: `fetched`; review: `scoped_repository_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
