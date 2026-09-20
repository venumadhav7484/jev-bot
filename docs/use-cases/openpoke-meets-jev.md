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

The README reports cheaper individual decisions and documents a suppression attack created by its own initial drop policy.

## Limits and reuse

Agreement is not accuracy; there is no labeled email-quality result. End-to-end savings remain unmeasured because some paths add model calls. AgentDojo attacks failed even without the guard, so that run does not prove protection. Quarantine still imposes review cost.

## Sources

- [github.com](https://github.com/0xShin0221/openpoke-meets-jev) — access: `fetched`; review: `sections_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
