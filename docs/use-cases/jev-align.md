---
id: jev-align
title: "jev-align: optimize decision criteria with labels"
category: quality
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# jev-align: optimize decision criteria with labels

## What

An experimental CLI refines Jev decision functions from user-labeled examples.

## How Jev fits

Rounds select ambiguous examples plus an audit sample, run GEPA with a separate reflection model, and present proposed question changes for user acceptance. Saved functions can capture later examples.

## Why and impact

Turns repeated decision errors into inspectable criterion changes instead of manually guessing every threshold or prompt.

## Limits and reuse

This changes question configuration, not Jev weights. Labels, held-out evaluation and reflection-model cost remain necessary; higher training score does not automatically accept a change. No reproduced quality gain is established.

## Sources

- [github.com](https://github.com/sutro-sh/jev-align) — access: `fetched`; review: `sections_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
