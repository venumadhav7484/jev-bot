---
id: pi-heed
title: "Pi-heed: conversational constraints at tool execution"
category: security
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Pi-heed: conversational constraints at tool execution

## What

A Pi extension tracks user constraints as runtime state.

## How Jev fits

Deterministic rules cover obvious cases; Jev handles ambiguous free-text constraints before side-effecting tool calls. Default is shadow mode, failing open on uncertainty or errors.

## Why and impact

Author reports 46 passing tests.

## Limits and reuse

Passing tests are not containment evidence. Fail-open advisory behavior cannot enforce hard bans or replace permissions.

## Sources

- Discord source — private provenance retained locally.
- [https://github.com/Nyarlathoteppppp/pi-heed](https://github.com/Nyarlathoteppppp/pi-heed) — access: `fetched`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
