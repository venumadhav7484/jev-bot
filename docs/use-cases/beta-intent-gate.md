---
id: beta-intent-gate
title: "Beta intent gate: bounded routing under latency budget"
category: routing
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Beta intent gate: bounded routing under latency budget

## What

Author replaces intent checks that route requests to models and tool sets.

## How Jev fits

Jev selects bounded intent judgments; host uses those decisions to route subsequent processing. Article also reports a separate slide-deck claim check without exposing its complete input representation.

## Why and impact

Author reports roughly70 cases, repeated three times, all correct; median250ms, reported means453–688ms, and no call exceeding1.5s. These are local author results.

## Limits and reuse

Dataset, exact prompts and repeat logs unavailable in article. No universal accuracy or latency guarantee. Article incorrectly says every answer has confidence: official Noul returns a probability without a separate confidence field. Slide-deck example does not establish native image input.

## Sources

- [https://madppiper.substack.com/p/my-thoughts-on-jev-after-the-private](https://madppiper.substack.com/p/my-thoughts-on-jev-after-the-private) — access: `fetched`; review: `article_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
