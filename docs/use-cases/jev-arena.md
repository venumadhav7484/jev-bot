---
id: jev-arena
title: "Jev Arena: fighters written in English, piloted live by Jev"
category: games
evidence: author-reported
reviewed_on: 2026-09-27
independently_reproduced: false
---

# Jev Arena: fighters written in English, piloted live by Jev

## What

An open-source arena where each fighter is a paragraph of strategy plus optional reflex rules, and a decision model pilots it several times a second.

## How Jev fits

Jev chooses movement and weapon actions and answers yes/no reflex checks about four times a second from the game state; code runs physics and damage. Replays show every probability Jev returned. The brain can be swapped for Laya, Kev or an LLM.

## Why and impact

The author reports one 32-second fight took 239 decisions at about 0.23 s each for about 1.4 cents. On the ladder, a one-sentence fighter with no reflexes finished second of six.

## Limits and reuse

Game ladder results are small and author-run; a strategy paragraph winning does not show general control ability. Latency figures are for this game loop.

## Sources

- [Jev Arena](https://eliot5566.github.io/jev-arena/?replay=ladder/replays/glass-cannon__trickster__g1.json) — access: `fetched`; review: `not_reviewed`.
- [https://github.com/Eliot5566/jev-arena](https://github.com/Eliot5566/jev-arena) — access: `fetched`; review: `readme_reviewed`.
- [https://github.com/Eliot5566/jev-arena/issues/1](https://github.com/Eliot5566/jev-arena/issues/1) — access: `fetched`; review: `not_reviewed`.
- [https://eliot5566.github.io/jev-arena/?overlay=1&playlist=highlights](https://eliot5566.github.io/jev-arena/?overlay=1&playlist=highlights) — access: `fetched`; review: `not_reviewed`.
- [https://eliot5566.github.io/jev-arena/?replay=highlights/glass-cannon-vs-trickster.json](https://eliot5566.github.io/jev-arena/?replay=highlights/glass-cannon-vs-trickster.json) — access: `fetched`; review: `not_reviewed`.
- [https://github.com/Eliot5566/jev-arena/pull/2](https://github.com/Eliot5566/jev-arena/pull/2) — access: `fetched`; review: `not_reviewed`.
- [Related public project or article](https://eliot5566.github.io/jev-arena) — discovered via Discord source (private provenance retained locally); access: `not_attempted`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
