---
id: jev-skill-router
title: "Skill router for Claude Code: a published negative result"
category: limitations
evidence: author-reported
reviewed_on: 2026-09-27
independently_reproduced: false
---

# Skill router for Claude Code: a published negative result

## What

A Claude Code hook asks Jev which installed skill fits each prompt and logs the answer, telling Claude only if the user opts in.

## How Jev fits

On each prompt, the prompt and skill roster go to Jev; code reads the probabilities and names at most one skill, or none. It runs in shadow mode by default so its suggestions can be checked against the skills sessions actually used.

## Why and impact

Scripted single-intent requests were 6 of 6 sensible, but in a real session 3 of 6 suggestions were wrong: mid-conversation follow-ups passed the gate. The author concludes a hook cannot change Claude Code's own skill listing, and a weaker judge advising a stronger model that already sees the same descriptions adds little.

## Limits and reuse

Author's own roster of 50–59 skills, Japanese prompts, very small samples from mixed versions. Published as a measuring instrument, not a recommendation.

## Sources

- [GitHub - shimo4228/jev-skill-router: Claude Code plugin: asks TypeS...](https://github.com/shimo4228/jev-skill-router) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
