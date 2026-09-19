---
id: langgraph-intent
title: "LangGraph: mocked intent-recognition workflow"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# LangGraph: mocked intent-recognition workflow

## What

Small LangGraph workflow uses Jev for intent matching.

## How Jev fits

Jev decisions feed graph branches; author uses mocked recognition tasks and plans MLflow-backed evaluation on synthetic data.

## Why and impact

Shows composition with existing orchestration framework without requiring a generative model for each branch.

## Limits and reuse

Ten mocked emails are smoke checks; handlers only assign destinations, not send email or make payments. Confidence is exposed but successful calls always route to one of two handlers. Mocked SDK tests do not validate semantic accuracy.

## Sources

- Discord source — private provenance retained locally.
- [https://github.com/GiesN/typesafe-jev-workflow](https://github.com/GiesN/typesafe-jev-workflow) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
