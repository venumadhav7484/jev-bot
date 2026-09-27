---
id: configurator-jev-gemini
title: "Industrial configurator: batching “what if” questions, Jev versus Gemini"
category: business
evidence: author-reported
reviewed_on: 2026-09-27
independently_reproduced: false
---

# Industrial configurator: batching “what if” questions, Jev versus Gemini

## What

An agent chooses product options across eight linked configurator dropdowns and was compared with Gemini on 300 synthetic customer requests.

## How Jev fits

Asking the dependent “what if” questions together cut about seven model calls to three. A verification step rejects answers it does not trust.

## Why and impact

The author reports both models became more accurate with batching, and Jev rejected wrong answers while wrongly rejecting 70% fewer correct ones. Gemini still won on overall accuracy, and its structured-output schema limit was hit before its context window.

## Limits and reuse

Synthetic requests; only the first post of the thread was reviewed, so full numbers and diagrams are not verified. Gemini’s overall accuracy advantage is part of the result.

## Sources

- [https://x.com/nikhilmudholkar/status/2103441246370791548?s=20](https://x.com/nikhilmudholkar/status/2103441246370791548?s=20) — access: `fetched`; review: `post_text_reviewed_media_pending`.
- [Related public project or article](https://x.com/nikhilmudholkar/status/2103441246370791548) — discovered via Discord source (private provenance retained locally); access: `fetched`; review: `post_text_reviewed_media_pending`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
