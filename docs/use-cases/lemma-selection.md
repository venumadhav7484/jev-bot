---
id: lemma-selection
title: "Lemma selection during proof search"
category: retrieval
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Lemma selection during proof search

## What

A proof-search experiment compares Jev selection with BM25.

## How Jev fits

Jev judges which lemmas are promising for the current proof state.

## Why and impact

On ten problems, the screenshot reports Jev8/10 first choice and9/10 within the first five, versus variable-normalized BM252/10 and7/10. Author says Jev is not yet faster; improved pruning on harder proofs is a hypothesis.

## Limits and reuse

Random (one seed), token-overlap and raw BM25 baselines score0/10 in both reported columns. Small evaluation; corpus construction and wall-clock gains are not established. No independent reproduction. A formal checker must establish proof validity.

## Sources

- Discord source — private provenance retained locally.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
