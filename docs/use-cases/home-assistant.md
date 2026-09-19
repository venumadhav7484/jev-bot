---
id: home-assistant
title: "Home Assistant Jev integration"
category: interfaces
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Home Assistant Jev integration

## What

Expose semantic home-state judgments as entities.

## How Jev fits

The linked integration returns probabilities, choices or scores about household state for use by existing automations.

## Why and impact

Separates judgment from Home Assistant's automation and device-control layer.

## Limits and reuse

No device-action reliability benchmark was supplied. The model should not replace deterministic safety limits.

## Sources

- Discord source — private provenance retained locally.
- [https://github.com/AboveColin/HA-Jev](https://github.com/AboveColin/HA-Jev) — access: `fetched`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
