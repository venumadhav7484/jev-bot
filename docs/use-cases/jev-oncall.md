---
id: jev-oncall
title: "jev-oncall: alert triage with four questions per alert"
category: operations
evidence: author-reported
reviewed_on: 2026-09-27
independently_reproduced: false
---

# jev-oncall: alert triage with four questions per alert

## What

An open-source layer receives production alerts from Alertmanager and routes each to page, ticket, review or log.

## How Jev fits

One Jev call per alert asks four typed questions: is it actionable, how severe, who owns it, and is it a duplicate of an open incident. Code turns the probabilities into routing; Jev never pages anyone. Without a key, alerts fall back to their configured severity.

## Why and impact

In the replayed demo, an alert with P(page)=1.00 was sent to human review instead of paging, because Jev linked it (0.87) to an incident another team owned. Decisions took a median 228 ms.

## Limits and reuse

Eight staged alerts from one replayed run; no evaluation on a real alert stream. Sending to PagerDuty, Slack or Jira is not built yet.

## Sources

- [Related public project or article](https://github.com/mingleiw/jev-oncall) — discovered via Discord source (private provenance retained locally); access: `fetched`; review: `readme_reviewed`.
- [Related public project or article](https://mingleiw.github.io/jev-oncall/demo) — discovered via Discord source (private provenance retained locally); access: `fetched`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
