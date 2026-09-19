---
id: infer-code-review
title: "Static analysis plus semantic edit review"
category: quality
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Static analysis plus semantic edit review

## What

A coding demo checks whether changes unnecessarily increase computational work or architectural complexity.

## How Jev fits

Intercepted edits go through Infer; work-estimate differences, comments and user intent become Jev scoring context. Weak results send feedback to the coding agent.

## Why and impact

Author reports better results with static-analysis context than with Jev alone on synthetic and one historical task.

## Limits and reuse

Bundled archive was not executed. No full benchmark or concurrency proof supplied; scores supplement compiler and static analysis.

## Sources


Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
