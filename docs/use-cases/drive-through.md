---
id: drive-through
title: "Voice drive-through assistant"
category: voice
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Voice drive-through assistant

## What

Interpret spoken drive-through orders.

## How Jev fits

Author reports local nvidia/parakeet-tdt-0.6b-v2 speech recognition; Jev supplies semantic decisions over menu and current order. Reviewed recording shows item additions, quantity corrections, ingredient removals and size changes.

## Why and impact

Illustrates combining specialized speech recognition with rapid semantic decisions.

## Limits and reuse

A34-second recording was reviewed using a local speech transcript and34sampled frames. It shows an ambiguous size-change exchange and subsequent order update; not a full accuracy or latency benchmark. Displayed cumulativeJevcost$.00598 lacks invoice/protocol verification. No payment handling or production reliability test. Speech recognition is a separate component; sampled frames can miss brief events.

## Sources

- [https://x.com/oow2626/status/2101110230000230872?s=46](https://x.com/oow2626/status/2101110230000230872?s=46) — access: `browser_readable`; review: `post_and_transcript_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
