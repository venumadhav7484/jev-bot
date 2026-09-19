---
id: corealm-rpg
title: "Corealm: state-driven RPG agents"
category: games
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Corealm: state-driven RPG agents

## What

RPG agents choose combat, travel, food, rest and gathering actions alongside players.

## How Jev fits

Host supplies current game state, allowed API actions and nearby argument choices. Jev ranks them; code executes the selected action and rechecks at a configured cadence. Personality is additional state.

## Why and impact

Author reports roughly 260ms decisions. In one low-health example, travel probability was 79% with 86% danger and the agent retreated.

## Limits and reuse

Illustrative author report; no controlled survival, economic or multiplayer benchmark. Planned raids/trade/economy are goals, not proven results. Recheck interval is not inference latency; media remains unreviewed. Source review: Agent-accessible game surface is useful integration infrastructure but not proof of Jev gameplay. Test polyfill is not native browser validation; game grants same knowledge/actions as player and persistent data remain browser-local.

## Sources

- Discord source — private provenance retained locally.
- [https://x.com/abcdmku/status/2100743097143493062](https://x.com/abcdmku/status/2100743097143493062) — access: `fetched`; review: `visible_post_text_reviewed`.
- [Corealm repository](https://github.com/abcdmku/Corealm2) — discovered via [external source](https://x.com/abcdmku/status/2100743097143493062); access: `fetched`; review: `context_only_not_jev_evidence`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
