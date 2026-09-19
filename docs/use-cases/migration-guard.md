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

Deterministic SQL parsing, backups and explicit approval remain necessary; missed model detections must not silently authorize destructive migrations. Source review: Typed enum is not deterministic semantic safety; a false SAFE can pass destructive SQL. Two toy statements do not validate nested DDL or production readiness. Bind scan to exact migration hash/revision; code rollback does not reverse database migration. README certainty claims rejected pending implementation and adversarial tests.

## Sources

- [https://github.com/opaielsheikh/typesafe-migration-guard](https://github.com/opaielsheikh/typesafe-migration-guard) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
