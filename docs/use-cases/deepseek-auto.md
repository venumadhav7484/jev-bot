---
id: deepseek-auto
title: "DeepSeek harness automatic-choice plugin"
category: agents
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# DeepSeek harness automatic-choice plugin

## What

A plugin lets Jev answer next-action and multiple-choice prompts in an agent harness.

## How Jev fits

Jev adds an automatic-review permission mode around end-of-step decisions.

## Why and impact

Intended to reduce unattended-run interruptions.

## Limits and reuse

Full-access wording does not establish safety. No permission-boundary or recovery tests verified; preserve user authorization separately.

## Sources

- Discord source — private provenance retained locally.
- [https://git.allen-software.com/allenh1/dsh-auto-mode](https://git.allen-software.com/allenh1/dsh-auto-mode) — access: `fetched`; review: `metadata_only`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
