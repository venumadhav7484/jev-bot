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

Structured gameplay/recovery loop retains recordings and action distributions for research.

## Why and impact

Inspectable trajectories could support later policy training.

## Limits and reuse

Author hopes to ascend; no completed ascension established. Policy training is future work, not evidence Jev updates weights online. A reported nearly 10,000-move run still at level one was later found to have a harness bug: moves were not advancing the game. Author planned a fix; no corrected completion confirmed. Source review: Captured page contains no server frame or completed outcome. Action confidence is not winning probability, and movement alone does not establish game progress. Source review: Hook coverage depends on host events; hidden reasoning and bypassed tools are unobservable. No plugin daily/byte/session quota by default. Completion judgments do not prove deployment. Source review: Gameplay activity and fewer loops are not win/progress proof. Negative experiments, false-positive evaluator and native final-score corrections must remain in recommendations. One validated crash path does not establish hardware resilience; availability/credit-exhaustion and archive limits remain operational constraints. Source review: Restartability does not establish game competence or bounded total spend. Accounting chunk limits reset indefinitely and cannot cap whole until-win run. Legacy replay arrays are reconstructions,not historical observations; retention depends on finite storage and services. No ascension demonstrated. Source review: Post-tool assessment cannot undo executed action or authenticate fabricated evidence. Merge state does not prove every historical acceptance item or live-provider demo complete. Defaults evolved in later PRs; current enforced/optional behavior needs those updates, not original body alone. Do not call R2/R3 automatic routing shipped from R1 transport. Source review: Broad advisory coverage is not mandatory enforcement, model switching or hidden-reasoning access. Completion assessment only checks supplied evidence. No default cumulative cost cap; attempts differ from successful/billedcalls. Synthetic evaluations/installation evidence do not prove universal host support or Directory approval. Source review: Root README and PR evidence have different scope/version. Do not infer automatic model routing or Jev-enforced approvals from general agent features; post-tool review and pre-action authorization remain distinct.

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

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
