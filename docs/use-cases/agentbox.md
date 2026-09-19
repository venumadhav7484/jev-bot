---
id: agentbox
title: "Agentbox: live skill routing"
category: agents
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Agentbox: live skill routing

## What

Select skills for an agent task.

## How Jev fits

The author identifies Jev as a daily-used skill router and links an architecture decision record.

## Why and impact

A bounded skill catalog is a concrete routing surface.

## Limits and reuse

Daily-use status is self-reported. Repository documentation still needs implementation-level review before adopting its configuration. Source review: Small local routing set and soft labels limit generalization. Advisory pick must still fit task; prompt egress accepted for that project only and per-project bypass missing. Context residency can exceed judge cost. Staged activation and mid-run proposal must not be described as broadly deployed features.

## Sources

- Discord source — private provenance retained locally.
- [https://github.com/DreamLab-AI/agentbox/blob/main/docs/adr/ADR-2091-live-skill-router.md](https://github.com/DreamLab-AI/agentbox/blob/main/docs/adr/ADR-2091-live-skill-router.md) — access: `fetched`; review: `document_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
