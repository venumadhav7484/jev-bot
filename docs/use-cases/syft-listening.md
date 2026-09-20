---
id: syft-listening
title: "Syft Listening: judgments over live transcripts"
category: voice
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Syft Listening: judgments over live transcripts

## What

Analyze transcript text for selected speaking and language signals.

## How Jev fits

Browser speech recognition produces text; finalized sentence context and enabled metrics go through a server proxy to Jev. The UI renders typed readings and uncertainty.

## Why and impact

Separates transcription from cheap repeated judgments, with optional metrics reducing unnecessary questions.

## Limits and reuse

Browser transcription support differs and a text fallback is needed. A claim-related judgment is not external fact checking. The hosted proxy sees keys in transit according to the README; accuracy and latency were not independently tested.

## Sources

- [listen.syftlearning.app](https://listen.syftlearning.app/) — access: `fetched`; review: `sections_reviewed`.
- [github.com](https://github.com/tpaulshippy/syft-listening) — access: `fetched`; review: `sections_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
