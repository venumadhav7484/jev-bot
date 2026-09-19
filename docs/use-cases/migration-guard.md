---
id: migration-guard
title: "Database Migration Guardian"
category: quality
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Database Migration Guardian

## What

Screen planned database migrations before execution.

## How Jev fits

The author describes intercepting Prisma SQL plans and halting when Jev detects destructive operations.

## Why and impact

Adds a semantic review step before a consequential action.

## Limits and reuse

Deterministic SQL parsing, backups and explicit approval remain necessary; missed model detections must not silently authorize destructive migrations.

## Sources

- Discord source — private provenance retained locally.
- [https://github.com/opaielsheikh/typesafe-migration-guard](https://github.com/opaielsheikh/typesafe-migration-guard) — access: `fetched`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
