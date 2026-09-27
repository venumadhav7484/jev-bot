---
id: usagetap-model-lifecycle
title: "UsageTap: resolve model keys to lifecycle advice"
category: developer-tools
evidence: author-reported
reviewed_on: 2026-09-27
independently_reproduced: false
---

# UsageTap: resolve model keys to lifecycle advice

## What

A free GET API and GitHub Action detect LLM model identifiers in code and report deprecation, retirement and suggested replacements.

## How Jev fits

The author uses Jev alongside heuristics to classify parts of a model key (vendor, family, version, date pin) and to match the right base model, using confidence to know when the match is uncertain.

## Why and impact

The author reports model-key matching was unreliable before Jev and expects the Jev cost to be about $0.50 a month.

## Limits and reuse

The public product page reviewed describes the lifecycle audit but does not mention Jev; the Jev role and cost come from the author’s post. No matching accuracy published. Lifecycle data still depends on provider announcements.

## Sources

- [https://usagetap.com/model-lifecycle?model=openai%2Fgpt-4-turbo](https://usagetap.com/model-lifecycle?model=openai%2Fgpt-4-turbo) — access: `fetched`; review: `not_reviewed`.
- [Model Lifecycle Audit for GitHub | UsageTap](https://usagetap.com/model-lifecycle) — access: `fetched`; review: `landing_page_reviewed`.
- [usagetap.com](https://usagetap.com/twitter-image?fe774505fb41b1bc) — access: `not_attempted`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
