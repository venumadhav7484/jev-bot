---
id: decor-agent-flinch
title: "Agent flinch: destructive operations still need explicit authority"
category: security
evidence: author-reported
reviewed_on: 2026-09-24
independently_reproduced: false
---

# Agent flinch: destructive operations still need explicit authority

## What

A coding-agent gate evaluates a proposed destructive tool call before execution.

## How Jev fits

Author supplies JSON state to three Nouls and one Choice. Application policy separately classifies the action; shared destructive work requires confirmation of the resolved environment name even when the judge appears confident.

## Why and impact

A reusable boundary: use Jev to interpret intent and context, but keep destructive-action policy and human confirmation in deterministic code.

## Limits and reuse

This is an attributed integration report, not proof against destructive-agent incidents. A local-looking endpoint can hide shared resources, so environment resolution must come from trusted application data. The captured repository response did not establish code behavior; end-to-end enforcement remains untested.

## Sources

- [GitHub - arober39/decor-agent](https://github.com/arober39/decor-agent) — access: `fetched`; review: `not_reviewed`.
- [Building the Agent Flinch with Jev and LaunchDarkly](https://dev.to/alexiskroberson/building-the-agent-flinch-with-jev-and-launchdarkly-pg0) — access: `fetched`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
