---
id: codeeagle-jev
title: "CodeEagle: propose candidates before asking for a judgment"
category: retrieval
evidence: author-reported
reviewed_on: 2026-09-24
independently_reproduced: false
---

# CodeEagle: propose candidates before asking for a judgment

## What

A project uses optional Jev steps for speaker adjudication, topic relationships and search reranking, with a reusable Go client.

## How Jev fits

Deterministic or inexpensive logic proposes candidates; focused questions judge supplied evidence; application thresholds decide whether to accept or leave an item unidentified.

## Why and impact

The author reports narrower yes/no questions worked better for the intended relation task than broad multi-way classification, and reranking improved three of five example queries. Leaving an uncertain speaker unnamed avoids silently assigning a wrong identity.

## Limits and reuse

The reported six-way accuracy and binary AUC are different metrics and tasks, not directly comparable percentages. Small local corpora, repeat-call variation and inaccurate state fields remain. A sharply separated distribution is not by itself a calibration result; no independent reproduction.

## Sources

- [CodeEagle/docs/jev.md at main · imyousuf/CodeEagle](https://github.com/imyousuf/CodeEagle/blob/main/docs/jev.md) — access: `fetched`; review: `sections_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
