---
id: peaks-notes
title: "Peaks: novelty routing with shadow-mode audits"
category: agents
evidence: author-reported
reviewed_on: 2026-09-24
independently_reproduced: false
---

# Peaks: novelty routing with shadow-mode audits

## What

A conversation-summary tool compares each new chunk with an evolving topic state.

## How Jev fits

Jev labels information as new, known or changed; a separate writer updates summaries and names topics. Original sources and an audit journal remain. The README’s default hook runs in shadow mode, letting the writer inspect every turn while recording routing decisions.

## Why and impact

Illustrates how to measure a possible bypass policy before allowing it to skip work. Active mode describes sampled audits of bypassed chunks.

## Limits and reuse

The announcement describes the intended active flow; the README says the current hook does not yet obtain those skipped-writer savings. Optional evaluator absence means no semantic verdict. Source preservation and atomic summary commits do not prove important content was retained.

## Sources

- [GitHub - RankOneLabs/peaks-notes: Conversation summary](https://github.com/RankOneLabs/peaks-notes) — access: `fetched`; review: `sections_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
