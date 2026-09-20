---
id: feedwall
title: "Feedwall: personal feed rules"
category: filtering
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Feedwall: personal feed rules

## What

Apply personal topic rules to posts across social feeds.

## How Jev fits

The extension sends post text and parallel yes/no topic questions to Jev. Code applies per-topic thresholds and a fixed Keep, Hide, Dim, Highlight precedence; users can restore mistakes.

## Why and impact

The README describes local caching, request budgets and topic tests against recently seen posts, making criteria and false positives inspectable.

## Limits and reuse

README reviewed, not installed. Errors keep posts visible. The trailer uses invented sample feeds and a fake browser API; it is not an independent live demonstration. Site adapters have different test coverage, and text is sent to TypeSafe under the user’s key.

## Sources

- [github.com](https://github.com/abhixhek/feedwall) — access: `fetched`; review: `sections_reviewed`.
- [x.com](https://x.com/thenightshipper/status/2101241514492092666v0.2) — access: `not_attempted`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
