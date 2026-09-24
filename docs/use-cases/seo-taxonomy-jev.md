---
id: seo-taxonomy-jev
title: "SEO taxonomy: context, lookup tables and rubric wording"
category: data
evidence: author-reported
reviewed_on: 2026-09-24
independently_reproduced: false
---

# SEO taxonomy: context, lookup tables and rubric wording

## What

An author reports adapting a search-query taxonomy benchmark to Jev on 325 wine-and-food tourism queries.

## How Jev fits

Choice questions select category and subcategory; a Score rubric measures similarity. Application code supplies a winery-name gazetteer for deterministic region lookup. The author moved away from array-indexed multi-query state.

## Why and impact

Reported exact agreement with human labels rose from 67.4% under a strict rubric to 83.4% when world knowledge was allowed and 89.2% with the gazetteer.

## Limits and reuse

The linked AI-Seobench README documents the general dashboard, not this Jev run or its per-query files; those were offered on request and not obtained. Model-judge similarity scores differ from human-label exact accuracy. A reported absence of off-topic errors on this set does not prove Jev never goes off topic.

## Sources

- [GitHub - Search-Foundry/AI-Seobench: An interactive dashboard to vi...](https://github.com/Search-Foundry/AI-Seobench) — access: `fetched`; review: `context_repository_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
