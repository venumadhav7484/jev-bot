---
id: snake-limits
title: "Snake: speed versus planning quality"
category: games
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Snake: speed versus planning quality

## What

Compare real-time movement decisions with a reasoning model.

## How Jev fits

Both models receive the same input, one API call per move, with several prompt variations.

## Why and impact

The author reports Jev being faster while Luna collected roughly twice as many apples over the same move count.

## Limits and reuse

Reported weakness is anticipating multi-move traps. Use as counterevidence against assuming bounded actions make long-horizon reasoning easy. First image shows13versus24apples over200steps each,zero invalid moves/errors. Second shows Jev dead at81steps14apples versus baseline28apples at200steps; second comparison is unequal survival duration.

## Sources


Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
