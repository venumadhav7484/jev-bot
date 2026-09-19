---
id: jev-nethack
title: "NetHack: live runner, action probabilities and recordings"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# NetHack: live runner, action probabilities and recordings

## What

Public NetHack runner and live viewer expose Jev gameplay decisions.

## How Jev fits

Jev selects multi-turn intentions from choices filtered by host code. Movement, targeting and some safety responses are deterministic; the runner exposes state, requests and action probabilities.

## Why and impact

Inspectable trajectories could support later policy training.

## Limits and reuse

Early recording shows dungeon levels 1 to 3, not ascension; author reports frequent stalls. A later nearly 10,000-move level-one run had a harness bug: moves did not advance game state. No corrected completion established. Do not merge these distinct runs into one outcome. Action confidence is not winning probability; future trajectory-based policy training does not mean Jev updates weights online.

## Sources

- Discord source — private provenance retained locally.
- [https://github.com/integrate-your-mind/jev-codex-plugin](https://github.com/integrate-your-mind/jev-codex-plugin) — access: `fetched`; review: `readme_reviewed`.
- [https://github.com/integrate-your-mind/jev-codex-plugin/tree/main/source/jev-workflows](https://github.com/integrate-your-mind/jev-codex-plugin/tree/main/source/jev-workflows) — access: `fetched`; review: `readme_reviewed`.
- [https://github.com/retsu-AI/qq](https://github.com/retsu-AI/qq) — access: `fetched`; review: `readme_reviewed`.
- [https://github.com/retsu-AI/qq/pull/72](https://github.com/retsu-AI/qq/pull/72) — access: `fetched`; review: `pull_request_reviewed`.
- Private artifact (provenance retained locally) — access: `access_failed`; review: `inaccessible_content_pending`.
- Private artifact (provenance retained locally) — access: `access_failed`; review: `inaccessible_content_pending`.
- [https://github.com/integrate-your-mind/jev-nethack](https://github.com/integrate-your-mind/jev-nethack) — access: `fetched`; review: `readme_reviewed`.
- [https://github.com/integrate-your-mind/jev-nethack/tree/main/until-win](https://github.com/integrate-your-mind/jev-nethack/tree/main/until-win) — access: `fetched`; review: `readme_reviewed`.
- Private artifact (provenance retained locally) — access: `access_failed`; review: `inaccessible_content_pending`.
- Private artifact (provenance retained locally) — access: `access_failed`; review: `inaccessible_content_pending`.
- [https://jev-nethack-live.poppybyte.chatgpt.site/](https://jev-nethack-live.poppybyte.chatgpt.site/) — access: `fetched`; review: `source_text_reviewed`.
- [https://x.com/pj4533/status/2100624540938260919?s=20](https://x.com/pj4533/status/2100624540938260919?s=20) — access: `public_media_extracted`; review: `demo_trace_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
