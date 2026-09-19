---
id: tenet
title: "Tenet: natural-language code review rules"
category: quality
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Tenet: natural-language code review rules

## What

Check agent-written commits against repository conventions.

## How Jev fits

Developers define rules in tenet.yml; Jev judges changes and feeds findings into an agent correction loop.

## Why and impact

Targets semantic conventions that ordinary syntax linting misses.

## Limits and reuse

The project was early-stage in its post. A passing judgment does not establish functional correctness or replace tests.

## Sources

- Discord source — private provenance retained locally.
- [https://github.com/zoidsh/tenet](https://github.com/zoidsh/tenet) — access: `fetched`; review: `not_reviewed`.
- [https://github.com/zoidsh/tenetlint](https://github.com/zoidsh/tenetlint) — access: `fetch_failed`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
