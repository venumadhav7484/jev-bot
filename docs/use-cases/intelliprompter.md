---
id: intelliprompter
title: "Intelliprompter: live topic coverage"
category: voice
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Intelliprompter: live topic coverage

## What

Track whether a speaker has covered planned talking points.

## How Jev fits

Each topic receives a parallel Score question over the current transcript, ranging from absent to thoroughly discussed. A community clone reports polling every 0.5 seconds.

## Why and impact

Fast repeated judgments can update a checklist during speech. The clone author estimates less than $0.50 per hour; this was not measured here.

## Limits and reuse

Speech transcription is a separate component. Topic scores do not establish factual correctness. The original demo and community clone are related implementations, not identical artifacts. Source review: Checked points stop being evaluated; false checkoffs need manual correction. Ordinal coverage score is distinct from confidence. Speech recognition and transcript transmission have separate data paths; reported cost is scenario-specific. Source review: Separate transcription supplies text; Jev does not hear audio. Early passing mentions caused false completion at threshold1.0;1.5 is tuned on limited examples. Sticky completion and transcript tail can hide errors; original$40→$0.50/hour comparison is attributed, not independently reproduced.

## Sources

- Discord source — private provenance retained locally.
- [https://github.com/finetuningsingh/intelliprompter](https://github.com/finetuningsingh/intelliprompter) — access: `fetched`; review: `readme_reviewed`.
- [https://finetuningsingh.github.io/intelliprompter/](https://finetuningsingh.github.io/intelliprompter/) — access: `fetched`; review: `source_text_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
