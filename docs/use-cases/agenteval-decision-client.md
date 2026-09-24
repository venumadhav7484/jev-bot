---
id: agenteval-decision-client
title: "AgentEval: preserve typed answers and provider provenance"
category: developer-tools
evidence: author-reported
reviewed_on: 2026-09-24
independently_reproduced: false
---

# AgentEval: preserve typed answers and provider provenance

## What

A proposed AgentEval integration treats Jev as a decision evaluator rather than a prose-generating client.

## How Jev fits

The report describes a direct/OpenRouter client feeding a decision-evaluation interface, persisting probabilities and returned model IDs. Dry-run samples show request bodies before sending.

## Why and impact

Author reports 13 successful live calls. The intended 440-case comparison was future work at posting time, not a completed evaluation.

## Limits and reuse

A pull request is not proof of a released or merged feature. Wire-format notes distinguish zero-indexed Score levels and the absence of a Noul confidence field. No outcome accuracy or false-pass benchmark from this post.

## Sources

- [Decision evals (ADR-033): TypeSafe Jev as a third evaluator kind; s...](https://github.com/AgentEvalHQ/AgentEval/pull/257) — access: `fetched`; review: `not_reviewed`.
- [.NET: Add IDecisionClient (experimental), DecisionLoopEvaluator, an...](https://github.com/microsoft/agent-framework/pull/8563) — access: `fetched`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
