---
id: jeeves
title: "Jeeves: natural-language Discord moderation"
category: security
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Jeeves: natural-language Discord moderation

## What

Apply channel-specific moderation rules.

## How Jev fits

The author describes Jev deciding whether messages match actions, with Gemini and Neon in the surrounding system and explicit strike/action rules.

## Why and impact

Enables semantic moderation beyond literal regex matching.

## Limits and reuse

Moderator actions remain consequential. No measured false-positive rate or adversarial robustness was established. Source review: Jev consumes image descriptions, not images; Gemini and hosting add costs. Generated syntax-valid rule code still needs semantic tests. Moderation false-positive/negative rates unmeasured; incomplete history/media and non-atomic external effects require operational review.

## Sources

- Discord source — private provenance retained locally.
- [https://fixupx.com/just_some_dev/status/2100757839056634080](https://fixupx.com/just_some_dev/status/2100757839056634080) — access: `fetched`; review: `visible_post_text_reviewed`.
- [Astrid (@just_some_dev)](https://x.com/just_some_dev/status/2100757839056634080) — access: `fetched`; review: `visible_post_text_reviewed`.
- [github.com/Infrawrench/Jeeves](https://github.com/Infrawrench/Jeeves) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
