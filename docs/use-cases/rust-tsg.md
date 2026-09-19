---
id: rust-tsg
title: "Rust TypeSafe client and tsg semantic search"
category: developer-tools
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Rust TypeSafe client and tsg semantic search

## What

A Rust client library and command-line tool search source passages by meaning or a yes/no condition.

## How Jev fits

Inspected documentation describes typed Choice, Score and Noul outputs, async and blocking transports, and observable retries. tsg supports ranked find and predicate grep modes, preserving original file paths and line numbers.

## Why and impact

A relevant implementation pattern for this knowledge base: use model judgments to locate evidence and return the original source for review.

## Limits and reuse

README and tsg documentation were read; code was not installed or benchmarked. tsg sends source passages and nearby context to TypeSafe. Its own documentation warns of semantic misses and incomplete scans. Source review: Semantic search can miss evidence; failed files/evaluations explicitly mark incomplete coverage. Demo rules are fictional, and returned source passages are review starting points. Reviewed terminal images show threshold.700, file/line passages and14/14units succeeding on demo food-truck ordinances. This supports interface behavior, not legal relevance precision/recall.

## Sources

- Discord source — private provenance retained locally.
- [https://github.com/Twister915/typesafe-ai/tree/main/examples/tsg](https://github.com/Twister915/typesafe-ai/tree/main/examples/tsg) — access: `fetched`; review: `readme_reviewed`.
- [Rust TypeSafe client README](https://github.com/Twister915/typesafe-ai) — discovered via [external source](https://github.com/Twister915/typesafe-ai/tree/main/examples/tsg); access: `fetched`; review: `readme_reviewed`.
- [tsg semantic search documentation](https://github.com/Twister915/typesafe-ai/blob/main/examples/tsg/README.md) — discovered via [external source](https://github.com/Twister915/typesafe-ai/tree/main/examples/tsg); access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
