---
id: langwatch
title: "LangWatch: evaluations over production traces"
category: quality
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# LangWatch: evaluations over production traces

## What

LangWatch Instant Evals applies custom judgments to stored production traces, including a SQL evaluation function.

## How Jev fits

The product page describes per-row Jev questions, probabilities, exports and a bounded SQL interface. The supplied SQL illustration uses eval(conversation_bounded(...), a frustration predicate), grouped by conversation. Long traces may be shortened and marked as digests.

## Why and impact

Makes trace exploration and candidate evaluation sets easier to build. Speed, agreement and cost figures on the product page remain vendor-reported.

## Limits and reuse

The newer product-page evidence supersedes the earlier embed-only source scope. Promotional artwork reports about 20 seconds for 10,000 conversations at about 600 tokens each; it supplies no reproducible trace or accuracy labels. Its separate 300-conversation comparison is small. Shortened traces can omit decisive context; probabilities do not establish factual correctness. No independent benchmark reproduction.

## Sources

- [https://x.com/_rchaves_/status/2101050389898338709?s=46](https://x.com/_rchaves_/status/2101050389898338709?s=46) — access: `fetched`; review: `visible_post_text_reviewed`.
- [langwatch.ai](https://langwatch.ai/instant-evals) — access: `fetched`; review: `sections_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
