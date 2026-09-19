---
id: text-elo-ranker
title: "Text tournament: pairwise judgments and Elo ranking"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Text tournament: pairwise judgments and Elo ranking

## What

Recursive tournament ranks poems, pitches, lyrics, emails and hooks.

## How Jev fits

Jev answers two Choice questions: winner A/B and a reason from five authored criteria. Code maps the chosen reason to a fixed description, then uses tournament/Elo logic; there is no free-form Jev critique.

## Why and impact

Turns pairwise semantic preferences into an ordered list.

## Limits and reuse

Source-code inspection confirms predefined rationale text, not generated explanations. Random A/B swapping mitigates but cannot eliminate ordering bias. Missing winner responses default to A and 0.5 confidence; retries can compound SDK retries. Simultaneous winner/reason questions cannot condition on each other’s returned answer. No independent agreement or convergence benchmark. https://github.com/opaielsheikh/ai-elo-ranker/blob/main/elo_ranker/judge.py

## Sources

- [https://github.com/opaielsheikh/ai-elo-ranker](https://github.com/opaielsheikh/ai-elo-ranker) — access: `fetched`; review: `source_code_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
