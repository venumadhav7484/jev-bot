---
id: azdaja
title: "Azdaja: typed judgments within recursive LLM workflows"
category: agents
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Azdaja: typed judgments within recursive LLM workflows

## What

An open-source RLM layer adds a decision-only branch.

## How Jev fits

Jev handles reranking, verification, classification and semantic joins when generated prose is unnecessary.

## Why and impact

Avoids using a generative model for every recursive subtask.

## Limits and reuse

No end-to-end quality or savings result supplied. Mixed judgment and generation paths need separate evaluation. Source review: Optional Jev is separate from generative calls and historical RLM results. Monty is not OS isolation; offline receipt verification does not reproduce original live-model quality.

## Sources

- Discord source — private provenance retained locally.
- [https://github.com/kubet/azdaja](https://github.com/kubet/azdaja) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
