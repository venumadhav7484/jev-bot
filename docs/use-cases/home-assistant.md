---
id: home-assistant
title: "Home Assistant Jev integration"
category: interfaces
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Home Assistant Jev integration

## What

Expose semantic home-state judgments as entities.

## How Jev fits

Community integration maps Jev Noul/Choice/Score answers to sensors and automation variables, batching questions that share state and schedule. Assist selects exposed entities and supported intents; host code parses brightness, enforces budgets and sends unsupported or uncertain commands to a fallback agent.

## Why and impact

Separates judgment from Home Assistant's automation and device-control layer.

## Limits and reuse

README laundry and modem examples use sample data on a throwaway instance. A 0.31-second trace is one run; European latency is reported higher than published figures. No calibration or safety-control guarantee; host permissions, fallback and exact arithmetic remain necessary.

## Sources

- [https://github.com/AboveColin/HA-Jev](https://github.com/AboveColin/HA-Jev) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
