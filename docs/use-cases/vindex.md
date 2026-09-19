---
id: vindex
title: "Vindex: policy screening before content generation"
category: security
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Vindex: policy screening before content generation

## What

Vindex markets text-prompt policy screening with allow, review, block and webhook outcomes.

## How Jev fits

This cached landing page does not name Jev or establish which model implements its decisions.

## Why and impact

The vendor reports roughly 100 ms decisions and a ten-week moderation-queue sample with 84% auto-allowed, 9% blocked and 7% sent to human review.

## Limits and reuse

The interactive landing-page example explicitly uses canned simulation results. The reported percentages describe one platform’s moderation queue, not general accuracy.

## Sources

- [https://getvindex.com/](https://getvindex.com/) — access: `fetched`; review: `source_text_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
