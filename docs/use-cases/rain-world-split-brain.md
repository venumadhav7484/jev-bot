---
id: rain-world-split-brain
title: "Rain World: Claude plans, Jev picks the next move"
category: games
evidence: author-reported
reviewed_on: 2026-09-27
independently_reproduced: false
---

# Rain World: Claude plans, Jev picks the next move

## What

A split-brain agent plays Rain World: a mod turns the game into JSON ten times a second, Claude plans the route, Jev chooses what to do several times a second, and code presses buttons.

## How Jev fits

Each Jev request asks three questions: a Choice of action built fresh each tick from what is possible now, a Noul on whether a predator can attack within seconds, and a Score of how safe the plan is. After night one, options changed from motor primitives to semantic steps whose criteria text describe the concrete path from a pathfinder.

## Why and impact

The author reports 613 calls at a median 297 ms for $0.04 in one session. With semantic options the agent fed, crossed the gap that ended night one and reached a shelter.

## Limits and reuse

Author journal of a few nights; progress also came from rebuilt movement code. The lesson generalizes: a small, dynamic set of truthful options beat a large static menu.

## Sources

- [Related public project or article](https://frankyheadpants.net/) — discovered via Discord source (private provenance retained locally); access: `fetched`; review: `not_reviewed`.
- [Related public project or article](https://frankyheadpants.net/night-two) — discovered via Discord source (private provenance retained locally); access: `fetched`; review: `article_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
