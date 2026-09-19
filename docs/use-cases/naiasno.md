---
id: naiasno
title: "Naiasno: Bulgarian public-data tool routing"
category: agents
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Naiasno: Bulgarian public-data tool routing

## What

Route multilingual questions to more than 230 tools.

## How Jev fits

Jev selects tools; Gemini generates parameters. The author reports a 474-case evaluation including English, Bulgarian and transliterated Bulgarian.

## Why and impact

Reported typo routing improves over keyword matching: 94% English and 86% Bulgarian versus 28% and 34%. Parameter results also improve in the described pipeline.

## Limits and reuse

Transliterated Bulgarian remains a weakness: one reported comparison is 71% versus 94%. These are author measurements, not a general multilingual guarantee.

## Sources

- Discord source — private provenance retained locally.
- [https://naiasno.bg/chat/evals](https://naiasno.bg/chat/evals) — access: `fetched`; review: `source_text_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
