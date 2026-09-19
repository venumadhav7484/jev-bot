---
id: judgment-village
title: "Village NPCs: observable actions, attitudes and beliefs"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Village NPCs: observable actions, attitudes and beliefs

## What

Village simulation visualizes NPC judgments instead of generated dialogue.

## How Jev fits

Each tick asks typed questions about action, attitude toward player and belief. Host simulation renders results. One request batches all four villagers, each with five to nine questions; unchanged perceptions reuse decisions. Host owns pathing, memory, witnesses and arrest thresholds, with rate limits, budgets and a deterministic fallback.

## Why and impact

Multiple independent judgments can drive richer visible behavior. Author reports approximately 400ms for either one or four villagers, with near-zero idle inference cost; not independently reproduced.

## Limits and reuse

Linked demo/code need inspection; no measured consistency or latency.

## Sources

- Discord source — private provenance retained locally.
- [https://x.com/haiderTheDev/status/2100419750459519156?s=20](https://x.com/haiderTheDev/status/2100419750459519156?s=20) — access: `fetched`; review: `post_text_reviewed_media_pending`.
- [https://t.co/1JAlFmT4GM](https://t.co/1JAlFmT4GM) — access: `fetched`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
