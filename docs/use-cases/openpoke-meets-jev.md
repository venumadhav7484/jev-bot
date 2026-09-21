---
id: openpoke-meets-jev
title: "OpenPoke: email decisions and suppression lessons"
category: agents
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# OpenPoke: email decisions and suppression lessons

## What

An email-agent fork moves screening, tool checks and search relevance to Jev.

## How Jev fits

Parallel email judgments feed skip, summarize or uncertain-fallback paths. Flagged injection content is quarantined with a deterministic notice rather than silently dropped.

## Why and impact

The author reports mean decision latency of 424 ms versus 2,452 ms for Claude Sonnet 4 on 12 synthetic emails, with 72 calls and no request failures. Input-only costs were estimated at $0.049 versus $4.63 per 1,000 screens; token counts differ. These are per-decision figures, not end-to-end pipeline savings.

## Limits and reuse

The displayed 33/36 agreement at a 0.75 threshold is not accuracy; no labeled email-quality set was supplied. The author reports its initial injection gate suppressed 95.3% of emails during attack testing, motivating quarantine instead of silent dropping. AgentDojo attacks failed even without the guard, so that run does not prove protection. Additional calls and quarantine review costs remain part of the total workflow.

## Sources

- [github.com](https://github.com/0xShin0221/openpoke-meets-jev) — access: `fetched`; review: `sections_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
