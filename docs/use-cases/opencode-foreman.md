---
id: opencode-foreman
title: "Foreman: workflow supervision can increase total token use"
category: agents
evidence: author-reported
reviewed_on: 2026-09-24
independently_reproduced: false
---

# Foreman: workflow supervision can increase total token use

## What

An OpenCode plugin uses Jev to select the next allowed workflow capability while coding models perform the work.

## How Jev fits

Workflow configuration defines stages, model choices, required outputs and allowed transitions. Foreman validates stage outputs and persists progress around the Jev routing decision.

## Why and impact

Author reports better subjective structure on basic coding prompts, but also 4–6 times baseline token use initially and roughly twice baseline after fixes. The README explicitly warns that extra review and repair stages add model calls.

## Limits and reuse

No controlled quality benchmark establishes the claimed improvement. A cheap routing call does not imply a cheaper complete workflow. Include writing-model calls, repeated context, reviews and repairs when measuring cost; persistent progress is not proof of task completion.

## Sources

- [GitHub - Harrison97/opencode-foreman: A generic workflow runtime fo...](https://github.com/Harrison97/opencode-foreman) — access: `fetched`; review: `sections_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
