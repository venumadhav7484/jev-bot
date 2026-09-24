---
id: askgrep
title: "askgrep: semantic code search with a lexical counterexample"
category: retrieval
evidence: author-reported
reviewed_on: 2026-09-24
independently_reproduced: false
---

# askgrep: semantic code search with a lexical counterexample

## What

A Rust CLI scores source-code chunks against a natural-language predicate and returns file locations.

## How Jev fits

One chunk and one question travel in each request; requests run concurrently and content-based results can be reused. The author rejected packing chunks as Choice options after weaker results. A separate writer can inspect retrieved code.

## Why and impact

The tool makes exhaustive chunk scoring affordable on its measured code tree. Its README also reports a loss: on nine SWE-bench Lite instances, recall@10 was 0.56 versus 1.00 for BM25.

## Limits and reuse

Scanning every chunk does not guarantee finding every relevant fact. Literal wording versus an abstract synonym changed recall substantially on a different 120-chunk test. Small, task-specific author evaluations; one model-labelled comparison is explicitly void. Use lexical search and inspect misses, rather than assuming semantic ranking always wins.

## Sources

- [GitHub - fajarhide/askgrep: grep for the questions you cannot write...](https://github.com/fajarhide/askgrep) — access: `fetched`; review: `sections_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
