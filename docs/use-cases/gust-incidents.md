---
id: gust-incidents
title: "Gust: security-incident evaluation via OpenRouter"
category: operations
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Gust: security-incident evaluation via OpenRouter

## What

An Elixir Gust example models security-alert analysis, triage, incident-state assessment and response selection through Jev decisions.

## How Jev fits

Choice questions evaluate authorization, explanatory records and evidence strength; later stages consume previous choices. Response assessment is skipped for AUTO CLOSE or NOTIFY USER.

## Why and impact

The example encodes a prioritized response playbook, selecting a matching condition group and applicable action. No measured security effectiveness or deployment outcome is established by this cached code.

## Limits and reuse

Missing input categories fall back to a sample incident, and absent incident evidence is instructed to choose the mildest value. Selected response actions are logged; this excerpt does not demonstrate execution of containment or validated enforcement.

## Sources

- [https://x.com/MarcioK/status/2101043696422494246](https://x.com/MarcioK/status/2101043696422494246) — access: `fetched`; review: `visible_post_text_reviewed`.
- [https://t.co/sxIAN4VBUo](https://t.co/sxIAN4VBUo) — access: `fetched`; review: `source_text_reviewed`.
- [Author-linked implementation artifact](https://gist.github.com/marciok/673a02cfe1dd03055bec3b55b4a5d0f2) — discovered via [external source](https://x.com/MarcioK/status/2101043696422494246); access: `fetched`; review: `source_text_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
