---
id: jev-guard
title: "Jev-guard: proposed automatic command approvals"
category: security
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Jev-guard: proposed automatic command approvals

## What

A repository describes an auto-approval layer for coding-agent harnesses.

## How Jev fits

Jev judges requested operations for Claude Code, Codex and Antigravity integrations.

## Why and impact

Intended to reduce repetitive approval interruptions.

## Limits and reuse

README claims host hook interception and escalation behavior; compatibility and security enforcement are unverified. Audit mode explicitly converts all blocks to ALLOW; trusted fastpaths bypass Jev. Model judgment cannot establish shell containment or guarantee prevention of destructive commands.

## Sources

- [https://github.com/ClemensSchartmueller/jev-guard](https://github.com/ClemensSchartmueller/jev-guard) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
