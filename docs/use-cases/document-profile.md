---
id: document-profile
title: "Compressed document profiles for classification"
category: content
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Compressed document profiles for classification

## What

A classifier reduces input before evaluating documents.

## How Jev fits

A local structured profile reduces 24k characters to at most 4.5k; category, language and subject share a request. Sixteen documents run in parallel with SHA-256 caching.

## Why and impact

Author claims unchanged decisions with less input and latency.

## Limits and reuse

No labeled equivalence benchmark. Compression may remove decisive details; cache keys should include model and schema versions.

## Sources

- Discord source — private provenance retained locally.
- [https://x.com/Charlyhno/status/2100670579321754080](https://x.com/Charlyhno/status/2100670579321754080) — access: `fetch_failed`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
