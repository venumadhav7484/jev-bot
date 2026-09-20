---
id: extraction-marker-recovery
title: "Recover flattened document markers"
category: retrieval
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Recover flattened document markers

## What

Classify ambiguous superscript-like markers left behind by document extraction.

## How Jev fits

A recall-oriented tokenizer proposes spans; Jev chooses citation, footnote, section label, unit/exponent or non-marker. Code assembles labels using existing source characters.

## Why and impact

Separates cheap candidate discovery from semantic interpretation, useful when regex alone cannot distinguish a unit from a citation.

## Limits and reuse

Jev cannot recover a marker the tokenizer never proposes. The README and author report describe the method; no measured corpus accuracy or executed reproduction is established.

## Sources

- [github.com](https://github.com/chrismoseley/jev-extraction-marker-recovery) — access: `fetched`; review: `sections_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
