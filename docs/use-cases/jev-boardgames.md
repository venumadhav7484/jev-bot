---
id: jev-boardgames
title: "Jev Plays: board-game choices with coded tactical assistance"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Jev Plays: board-game choices with coded tactical assistance

## What

Rendered demo lists TicTacToe, ConnectFour, Battleship and Wordle modes.

## How Jev fits

Text board and candidate moves go to one Choice plus side judgments. Host code annotates threats, excludes moves allowing wins/forks and forces missed wins or blocks; override counts are displayed.

## Why and impact

Illustrates bounded model choice combined with deterministic tactical safeguards.

## Limits and reuse

Landing-page architecture inspected; no game played or benchmark reproduced. Host supplies tactics beyond legal-move enforcement, so wins cannot be attributed solely to Jev. Distinct from Elixir TicTacToe project.

## Sources

- [https://jevboardgames.everpaper.app/](https://jevboardgames.everpaper.app/) — access: `public_content_recovered`; review: `landing_page_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
