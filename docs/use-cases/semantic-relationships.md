---
id: semantic-relationships
title: "Corca: sentence relationship graph"
category: content
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Corca: sentence relationship graph

## What

Map how sentences relate inside a text.

## How Jev fits

Intl.Segmenter handles segmentation. Three Jev calls classify the document domain, sentence types and inter-sentence relationships.

## Why and impact

The author reports approximately 0.5 seconds, largely network roundtrip.

## Limits and reuse

The graph contains model judgments, not proven logical entailment. No annotated-corpus evaluation was supplied.

## Sources

- [https://jev-demo.corca.ai/](https://jev-demo.corca.ai/) — access: `fetched`; review: `source_text_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
