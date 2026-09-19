---
id: doom-community
title: "Community Doom implementation"
category: games
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Community Doom implementation

## What

Recreate a Doom decision loop.

## How Jev fits

Host extracts engine depth, labels and game variables into YAML. Jev chooses macro behavior while geometric raycasting, line-of-sight filtering, aim and trigger-lock code control execution. An asynchronous inference loop is separate from the 35Hz simulation.

## Why and impact

Shows that developers can reproduce the broad bounded-action pattern in a prototype.

## Limits and reuse

README claims about 10Hz inference and no dropped frames lack a reproduced performance distribution. Uses structured engine state and deterministic aiming, not Jev processing raw video.

## Sources

- Discord source — private provenance retained locally.
- [https://www.reddit.com/r/developersIndia/s/kuHoZ1jHFc](https://www.reddit.com/r/developersIndia/s/kuHoZ1jHFc) — access: `fetched`; review: `metadata_only`.
- [https://github.com/AmoghCreator/doom-jev](https://github.com/AmoghCreator/doom-jev) — access: `fetched`; review: `readme_reviewed`.
- [r/developersIndia](https://www.reddit.com/r/developersIndia/) — access: `fetched`; review: `metadata_only`.
- [share.redd.it](https://share.redd.it/preview/post/1wj7q3n?share=ziDSeWP5pPmqbkGKOHq6l) — access: `nontext_not_inspected`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
