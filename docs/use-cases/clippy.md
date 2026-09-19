---
id: clippy
title: "Clippy: context-sensitive help triggers"
category: interfaces
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Clippy: context-sensitive help triggers

## What

Show assistance when users appear stuck.

## How Jev fits

Recent interaction signals and explicit DOM validation errors feed typed judgments about struggle and whether to intervene. Host chooses help action, highlights relevant field and enforces a cooldown; user can accept help or dismiss it.

## Why and impact

Allows semantic help triggers beyond fixed timers.

## Limits and reuse

Author questions trigger quality and production readiness. Hesitation is not proof of confusion. Recorded malformed-number and missing-amount nudges do not establish fewer errors or higher conversion. Keep deterministic form validators, cooldowns, dismissal and false-positive feedback; never infer payment authorization from model confidence.

## Sources

- Discord source — private provenance retained locally.
- [https://x.com/sotak/status/2100701152824185319](https://x.com/sotak/status/2100701152824185319) — access: `fetched`; review: `demo_trace_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
