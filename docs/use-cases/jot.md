---
id: jot
title: "Jot: tool-selection agent loop"
category: agents
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Jot: tool-selection agent loop

## What

A general-purpose agent experiment driven by Jev decisions.

## How Jev fits

The inspected README describes Jev choosing tools and arguments, a host executing them, and real tool results returning as context until a reply is possible. Its calculator example delegates arithmetic to code; local drafts require separate tooling.

## Why and impact

Shows how typed decisions can drive a multi-step application loop. A follow-up post describes constraining Chrome actions to visible candidates.

## Limits and reuse

The marketing claim of being first was not verified. Do not infer native free-text generation or arithmetic reliability from the agent UI. No task suite was reproduced.

## Sources

- Discord source — private provenance retained locally.
- [https://github.com/runta-dev/jot](https://github.com/runta-dev/jot) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
