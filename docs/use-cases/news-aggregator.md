---
id: news-aggregator
title: "AI news relevance filtering"
category: content
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# AI news relevance filtering

## What

Filter a daily news feed for AI relevance.

## How Jev fits

Rendered pipeline replay identifies Jev relevance/importance judgments over article title, source and bounded snippet. Relevant items continue to separate generative analysts; insufficient evidence and service failures retain the article. Other models write summaries and enrich links.

## Why and impact

Reports 69 articles evaluated in 0.7 seconds.

## Limits and reuse

Replay supports Jev integration more directly than the previously inspected README. Sept18 replay reports 119 calls across providers, 1718 items, 54m17s and $0.480; those totals are not Jev-only cost or latency. Home page Sept19 report is a different run. Application telemetry and article truth, novelty, false-negative rate and editorial savings have not been independently validated.

## Sources

- Discord source — private provenance retained locally.
- [https://news.aatf.ai/](https://news.aatf.ai/) — access: `fetched`; review: `landing_page_reviewed`.
- [https://github.com/flyryan/ai-news-aggregator](https://github.com/flyryan/ai-news-aggregator) — access: `fetched`; review: `repository_documentation_reviewed`.
- [https://news.aatf.ai/replay?date=2026-09-18](https://news.aatf.ai/replay?date=2026-09-18) — access: `fetched`; review: `demo_trace_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
