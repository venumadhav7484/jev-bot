---
id: local-air-traffic
title: "Local-view air-traffic simulation"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Local-view air-traffic simulation

## What

Toy multi-airplane system makes decisions from local state and nearby ATC.

## How Jev fits

Astra/GLM used to build visuals and logic; Jev chooses per-plane actions with reported 150ms roundtrip.

## Why and impact

Explores decentralized decisions under limited information.

## Limits and reuse

Not the JFK voice simulation or later single-plane controller. No collision, throughput or real aviation validation. Source review: Safety comes partly from deterministic runway invariants, not model judgment alone. Confidence example is not calibration validation; toy simulation is not aviation certification. Default mock demo and live API mode must be distinguished; cost/latency reports are workload-specific.

## Sources

- Discord source — private provenance retained locally.
- [https://bsky.app/profile/leo.sylin.org/post/3mvp2qbuumk2s](https://bsky.app/profile/leo.sylin.org/post/3mvp2qbuumk2s) — access: `fetched`; review: `source_text_reviewed`.
- [#TypeSafe](https://bsky.app/hashtag/TypeSafe) — access: `fetched`; review: `metadata_only`.
- [https://github.com/lbotinelly/jev-little-airways/](https://github.com/lbotinelly/jev-little-airways/) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
