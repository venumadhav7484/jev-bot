---
id: magic-8-ball-npc
title: "Magic 8-Ball: reactive NPC mood from typed judgments"
category: games
evidence: author-reported
reviewed_on: 2026-09-27
independently_reproduced: false
---

# Magic 8-Ball: reactive NPC mood from typed judgments

## What

A small web toy answers yes/no questions but also reacts to insults and compliments and can hold a grudge against the user.

## How Jev fits

Jev judges the question and the user’s tone; the page logs the full request JSON and response in the browser console so developers can inspect them.

## Why and impact

Shows a cheap way to give a character state-dependent reactions without a generative model writing each reply.

## Limits and reuse

Toy demonstration; the page text reviewed is minimal and the console request was not inspected. No evaluation.

## Sources

- [Magic 8 Ball | OZOROMO zoo](https://fun.ozoromo.com/magic-8-ball/) — access: `fetched`; review: `landing_page_reviewed`.
- [Related public project or article](https://fun.ozoromo.com/magic-8-ball) — discovered via Discord source (private provenance retained locally); access: `fetched`; review: `landing_page_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
