---
id: near-here
title: "Near Here: local event validation"
category: business
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Near Here: local event validation

## What

Validate whether scraped material represents a relevant local event.

## How Jev fits

The author compares Jev with Mistral and Gemini using separately tuned prompts for this bounded validation task.

## Why and impact

Article reports mean0.59s and estimated$0.043 per1000decisions for the selected Jev configuration. Main50case development result48/50; additional21case result19/21. Faster/cheaper reported configuration does not establish a general accuracy advantage.

## Limits and reuse

Article reports prompt selection across132development cases with assistant-written expected labels. Headline48/50 for Jev is not held-out accuracy. On21additional,skewed records Jev19/21 equals Mistral and trails Gemini20/21; no general accuracy advantage established. High-reasoning chat baselines generate explanations,unlike Jev. Production deployment not claimed; no independent reproduction.

## Sources

- [https://nearhere.events/blog/typesafe-jev-mistral-gemini-event-validation](https://nearhere.events/blog/typesafe-jev-mistral-gemini-event-validation) — access: `browser_readable`; review: `article_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
