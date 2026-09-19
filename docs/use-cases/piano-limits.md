---
id: piano-limits
title: "Piano note selection failure"
category: experiments
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Piano note selection failure

## What

Test whether repeated note choices make coherent music.

## How Jev fits

Prior notes are fed back into state; a reply proposes choosing compatible MIDI sections instead.

## Why and impact

The original author reports repetitive C4-heavy output that did not sound good.

## Limits and reuse

Section selection was a proposed alternative, not a demonstrated fix. Do not claim native audio generation. Media review: Reviewed40 sampled frames: piano selects notes from prior-note state, initially climbs E4/A4/E5/A5/E6/A6/E7 then becomes dominated by repeated E4; late counter286notes with44%confidence. This gives visible repetition evidence consistent with author's negative musical assessment. Audio aesthetics not independently judged; proposed MIDI-section selection remains untested.

## Sources

- Discord source — private provenance retained locally.
- [https://x.com/BaselAshraf81/status/2100400028711805242?s=20](https://x.com/BaselAshraf81/status/2100400028711805242?s=20) — access: `fetched`; review: `demo_trace_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
