---
id: elcaro
title: "Elcaro: second opinion on prompt injection"
category: security
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Elcaro: second opinion on prompt injection

## What

Assess suspicious content retrieved by an agent.

## How Jev fits

Tavily extracts page text; an existing scanner evaluates it and Jev supplies a second opinion for borderline cases.

## Why and impact

Uses Jev as a bounded escalation component rather than the whole retrieval or execution system.

## Limits and reuse

A second model opinion is not proof that content is safe; execution permissions must stay outside retrieved text.

## Sources

- Discord source — private provenance retained locally.
- [https://x.com/UNgethe/status/2100652324418945273?s=20](https://x.com/UNgethe/status/2100652324418945273?s=20) — access: `fetch_failed`; review: `not_reviewed`.
- [https://t.co/j9hsV64WW6](https://t.co/j9hsV64WW6) — access: `fetch_failed`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
