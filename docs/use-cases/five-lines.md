---
id: five-lines
title: "five-lines: parser rules plus semantic code review"
category: developer-tools
evidence: author-reported
reviewed_on: 2026-09-24
independently_reproduced: false
---

# five-lines: parser rules plus semantic code review

## What

A Rust pull-request reviewer separates countable refactoring rules from questions requiring interpretation.

## How Jev fits

Tree-sitter finds changed methods and structural preconditions. Jev answers Nouls for semantic rules; application thresholds raise, flag for inspection or suppress findings. The updated README batches named methods in shared state.

## Why and impact

Author reports 34 labelled judgments remained correct while changing batch size, with 7.6 seconds for separate requests versus 1.0 second for one batch. The README chooses eight methods as a speed/margin compromise.

## Limits and reuse

One small author-labelled seed set, not an independent benchmark. Compliant examples moved toward the reporting threshold as batches grew; the largest reported question shift was 0.24. This checks structural style, not program correctness. Parser limits and unsupported-language fallback remain.

## Sources

- [https://github.com/jamescazzetta/five-lines](https://github.com/jamescazzetta/five-lines) — access: `fetched`; review: `sections_reviewed`.
- [Christian Clausen's ten refactoring rules](https://www.oreilly.com/library/view/five-lines-of/9781617298318/) — access: `not_attempted`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
