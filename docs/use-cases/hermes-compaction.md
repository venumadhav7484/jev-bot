---
id: hermes-compaction
title: "Hermes context-compaction plugin"
category: agents
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Hermes context-compaction plugin

## What

A plugin delegates part of Hermes context compaction to Jev.

## How Jev fits

Jev judges what context to retain; the exact policy is not described in the source post.

## Why and impact

Potentially reduces irrelevant context before further agent work.

## Limits and reuse

No retention-quality evaluation supplied. Important constraints can be lost during compaction and need explicit preservation checks.

## Sources

- Discord source — private provenance retained locally.
- [https://github.com/TheEpTic/hermes-plugins/tree/main/hermes-jev-compact](https://github.com/TheEpTic/hermes-plugins/tree/main/hermes-jev-compact) — access: `fetched`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
