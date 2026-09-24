---
id: jev-subtitle-qc
title: "Subtitle QC: flag translation errors without rewriting cues"
category: quality
evidence: author-reported
reviewed_on: 2026-09-24
independently_reproduced: false
---

# Subtitle QC: flag translation errors without rewriting cues

## What

A subtitle translator adds a Jev review queue after a separate model produces translations.

## How Jev fits

Local code preserves cue IDs, order and timestamps and retries missing translations. Jev sees source–translation pairs and answers whether a line needs human review for omission, negation, names, numbers or unsupported additions.

## Why and impact

Author reports catching all 65 injected errors with no false positives among 65 clean controls, matching one DeepSeek configuration under the same binary rubric.

## Limits and reuse

An early synthetic English-to-German test, not a production benchmark or proof of translation quality. Structural cue checks stay in code; Jev flags suspicious lines and does not rewrite them. Real ambiguity, language pairs and natural errors need separate labelled evaluation.

## Sources

- [GitHub - GeekLinkDev/jev-subtitle-translator: Translate SRT subtitl...](https://github.com/GeekLinkDev/jev-subtitle-translator) — access: `fetched`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
