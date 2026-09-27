---
id: jev-search
title: "Jev Search: plain-language web search ranked by Jev"
category: retrieval
evidence: author-reported
reviewed_on: 2026-09-27
independently_reproduced: false
---

# Jev Search: plain-language web search ranked by Jev

## What

A web search app takes a plain-language request and returns ranked links and snippets with visible relevance scores, without generating an answer.

## How Jev fits

Jev answers typed questions about the request, which the app turns into a query, sources and a time range the user can override; engines run in parallel through a search API; Jev scores each result for relevance and results are merged by URL, relevance, engine agreement and original rank. Jev can be called through TypeSafe, Vercel AI Gateway or Cloudflare Workers AI, with the others as fallbacks.

## Why and impact

Keeps the model to routing and ranking decisions, so users see real results and scores rather than a synthesized answer.

## Limits and reuse

Independent project; no relevance evaluation published. Coverage depends on the search provider, and model choices vary by provider.

## Sources

- [GitHub - superagents-lab/jev-search: Search the web with TypeSafe's...](https://github.com/superagents-lab/jev-search) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
