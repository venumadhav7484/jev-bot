---
id: news-aggregator
title: "AI news relevance filtering"
category: content
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# AI news relevance filtering

## What

Filter a daily news feed for AI relevance.

## How Jev fits

Discord source reports Jev relevance filtering and links a replay and repository. The reviewed repository README describes a Claude/Gemini news pipeline but does not corroborate the Jev integration itself.

## Why and impact

Reports 69 articles evaluated in 0.7 seconds.

## Limits and reuse

Relevance filtering does not verify article truth or novelty; network collection time and evaluation quality were not established. Source review: Public README establishes an adjacent generative news pipeline, not demonstrated Jev integration. Separate model and collection costs apply; adopt bounded retries and inspect replay payloads before publishing.

## Sources

- Discord source — private provenance retained locally.
- [https://news.aatf.ai/](https://news.aatf.ai/) — access: `fetched`; review: `metadata_only`.
- [https://github.com/flyryan/ai-news-aggregator](https://github.com/flyryan/ai-news-aggregator) — access: `fetched`; review: `repository_documentation_reviewed`.
- [https://news.aatf.ai/replay?date=2026-09-18](https://news.aatf.ai/replay?date=2026-09-18) — access: `fetched`; review: `metadata_only`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
