---
id: slide-selection
title: "Slides selected from live speech"
category: voice
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Slides selected from live speech

## What

Pull up a relevant slide while the presenter speaks.

## How Jev fits

Browser speech recognition supplies recent transcript. Jev Choice ranks stored slide titles/descriptions; host switching thresholds and none-of-these control deck changes.

## Why and impact

Reduces explicit navigation during a presentation; no formal evaluation was reported.

## Limits and reuse

A proposed reusable design is transcript plus slide IDs into Choice, with a keep-current option. This design is analysis, not inspected implementation. Media review: Reviewed61 sampled frames and narration. Browser speech recognition transcribes recent speech; deck descriptions and transcript feed slide-choice probabilities. Display explains switching above70%, or two agreeing matches above45%; off-topic/none keeps slide. Visible deck transitions follow broad topics, with transient alternatives. No independent relevance or latency evaluation. This establishes separate speech-to-text, not native Jev audio.

## Sources

- Discord source — private provenance retained locally.
- [https://x.com/zain_hoda/status/2100720719470494126?s=20](https://x.com/zain_hoda/status/2100720719470494126?s=20) — access: `fetched`; review: `demo_trace_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
