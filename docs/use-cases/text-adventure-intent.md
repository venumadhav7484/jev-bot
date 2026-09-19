---
id: text-adventure-intent
title: "Natural-language commands for a text adventure"
category: games
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Natural-language commands for a text adventure

## What

A small adventure accepts varied phrasings of movement and inspection actions.

## How Jev fits

README describes state-machine-filtered callable events, English intent cues, recent transcript/inventory and Choice selection. Host displays authored text in five languages; catchall records missing content and low confidence requests rephrasing.

## Why and impact

Natural-language input over bounded authored story; catchall logs guide new event authoring.

## Limits and reuse

README inspected, no live corpus accuracy reproduced. Offline tests use exact-name fallback, not model behavior. Text/localization authored; engine retains story-specific constants.

## Sources

- [text adventure](https://text-adventure.p11c.xyz/) — access: `fetched`; review: `source_text_reviewed`.
- [here the repo](https://gitlab.com/porky11/text-adventure) — access: `fetched`; review: `scoped_repository_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
