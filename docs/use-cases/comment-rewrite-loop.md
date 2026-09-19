---
id: comment-rewrite-loop
title: "Comment-rule judge and rewrite loop"
category: quality
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Comment-rule judge and rewrite loop

## What

A coding workflow reviews comments in a diff.

## How Jev fits

Jev flags rule violations; a generative model rewrites flagged comments; Jev checks again.

## Why and impact

Separates cheap checking from selective rewriting.

## Limits and reuse

An unflagged result is not proof of correctness. Add iteration bounds and preserve meaning while editing.

## Sources


Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
