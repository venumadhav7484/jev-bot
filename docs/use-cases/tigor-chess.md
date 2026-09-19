---
id: tigor-chess
title: "Tigor chess: human and Jev-versus-Jev modes"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Tigor chess: human and Jev-versus-Jev modes

## What

An AI-generated project README describes a single-file chess app with Jev as constrained move selector.

## How Jev fits

chess.js maintains rules and state. Each AI turn sends legal moves as Choice options and only an already-legal returned LAN is applied.

## Why and impact

Separating move legality from move preference prevents a selected answer from introducing an illegal move if the described checks work.

## Limits and reuse

The README requires an origin whitelisted for CORS. Its completion percentage is a project claim, not evidence of playing strength. Source code, gameplay and stale-response handling were not independently tested in this cached README review. Reviewed screenshot shows a loss to Qxf7 after blackNxf2, with .29confidence and290ms. One game, not a rating estimate.

## Sources

- Discord source — private provenance retained locally.
- [https://jev-chess.tgr.rs/](https://jev-chess.tgr.rs/) — access: `fetched`; review: `source_text_reviewed`.
- [https://github.com/enovikov11/tigor-ai/tree/main/games/5-jev-chess](https://github.com/enovikov11/tigor-ai/tree/main/games/5-jev-chess) — access: `fetched`; review: `readme_reviewed`.
- [https://x.com/the_tigor/status/2100532795625832912](https://x.com/the_tigor/status/2100532795625832912) — access: `fetched`; review: `post_text_reviewed_media_pending`.
- [https://t.co/JBEKqzRvRx](https://t.co/JBEKqzRvRx) — access: `fetched`; review: `source_text_reviewed`.
- [https://t.co/Xnyep0eaBN](https://t.co/Xnyep0eaBN) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
