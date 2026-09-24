---
id: homing-pigeon
title: "Homing Pigeon: optional email labels before any mailbox action"
category: productivity
evidence: author-reported
reviewed_on: 2026-09-24
independently_reproduced: false
---

# Homing Pigeon: optional email labels before any mailbox action

## What

A local Gmail inventory adds optional Jev categories and a spam indicator to sender/subject metadata.

## How Jev fits

A Choice selects one of seven categories; a separate Noul adds a spam marker at the application threshold. Guidance is editable. Current README explicitly describes a read-only inventory, not automatic deletion.

## Why and impact

Useful separation between storage accounting, semantic labels and later user action.

## Limits and reuse

Highest-probability classification has no abstention threshold and ties favor the first category; sender/subject alone omits message context. Future mailbox actions were not implemented in the post. Local hosting and token storage need care; no spam accuracy or safe-deletion evidence.

## Sources

- [GitHub - carlosinho/homing-pigeon: Tool for easier search and clean...](https://github.com/carlosinho/homing-pigeon) — access: `fetched`; review: `sections_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
