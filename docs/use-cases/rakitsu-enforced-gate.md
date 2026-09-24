---
id: rakitsu-enforced-gate
title: "Rakitsu: validate actual tool results before the next step"
category: agents
evidence: author-reported
reviewed_on: 2026-09-24
independently_reproduced: false
---

# Rakitsu: validate actual tool results before the next step

## What

An alpha agent IDE adds typed Jev tools and an application-enforced pipeline gate.

## How Jev fits

The gate reads the tool JSON result, checks bounds and blocks the next stage when data is missing or invalid. A per-finding grounding example asks whether the supplied diff contains the referenced construct.

## Why and impact

Author reports catching a run where Jev failed but the writing agent still declared the change safe. The enforced gate rejected that narration. This is a concrete distinction between an agent mentioning a check and code requiring a successful check.

## Limits and reuse

The fact-checking example still failed to retrieve adequate source pages. Grounding to a diff is not truth verification. The release also reports fixes for non-finite bounds; alpha tooling and examples were not executed or security-audited here.

## Sources

- [https://rakitsu.com/#wallpapers](https://rakitsu.com/#wallpapers) — access: `fetched`; review: `not_reviewed`.
- [Rakitsu v0.3.0-alpha.8 — Jev tool type + 8 worked examples, secur...](https://github.com/SK-ENT/rakitsu/discussions/98) — access: `fetched`; review: `release_notes_reviewed`.
- [Rakitsu — The Agent IDE](https://rakitsu.com/) — access: `fetched`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
