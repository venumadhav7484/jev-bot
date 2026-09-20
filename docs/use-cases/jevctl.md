---
id: jevctl
title: "jevctl: composable judgment CLI and agent plugin"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# jevctl: composable judgment CLI and agent plugin

## What

CLI exposes typed judgment workflows with probabilities and exit codes.

## How Jev fits

Commands cover evidence verification, screening, classification, regex extraction, matching, routing, retrieval, transcript compaction and concurrent batches; supports multiple provider routes and Claude Code plugin.

## Why and impact

Reusable toolkit may avoid building repeated API plumbing.

## Limits and reuse

Command semantics, extraction guarantees and provider compatibility require source review. Screening is fallible; compaction must be evaluated for lost context. Compaction docs say Jev sees tool-output size notes rather than full outputs and may abridge old state to fit its budget. Keeping retained text verbatim does not prove important content was never dropped. Source review: Closed spans prevent fabricated extraction strings but can select wrong candidate or omit missing spans. Source support judgments are not correctness proof. Exit status blocks downstream commands only with correct shell control flow; a pipe alone does not stop later consumers. Compaction can lose needed evidence even without rewriting. Later session-hook discussion warns frequent compaction can disrupt prompt-cache reuse. Reported 40–60% context reduction does not establish token billing savings or lossless task performance.

## Sources

- [https://jevcli.vectorz.app/](https://jevcli.vectorz.app/) — access: `fetched`; review: `page_reviewed`.
- [https://github.com/Nasrallah-AL/jev-cli/blob/main/docs/compact.md](https://github.com/Nasrallah-AL/jev-cli/blob/main/docs/compact.md) — access: `fetched`; review: `source_text_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
