---
id: forum-to-issues
title: "Discord forum posts to tracked issues"
category: operations
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Discord forum posts to tracked issues

## What

A radio-simulator developer triages community reports.

## How Jev fits

Jev judges whether a post warrants tracking, assigns severity and labels, then an LLM writes a clearer issue title and description.

## Why and impact

Avoids generating issue prose for irrelevant posts.

## Limits and reuse

Proof of concept with no measured recall or spam-resistance. Issue creation remains an application action with its own permissions.

## Sources

- Discord source — private provenance retained locally.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
