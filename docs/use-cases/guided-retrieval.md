---
id: guided-retrieval
title: "Evidence-guided web retrieval"
category: retrieval
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Evidence-guided web retrieval

## What

A private-alpha retrieval API extends a wiki-racing experiment.

## How Jev fits

Jev ranks links, external code fetches promising pages, and a judgment decides when sufficient evidence has been found.

## Why and impact

Targets useful evidence without reading every page.

## Limits and reuse

No recall benchmark supplied. Stopping too early can miss conflicting evidence; typed outputs do not guarantee factual coverage. Source review: Retrieval design preserves block-level citations and conflicts; captured page alone does not establish Jev implementation or measured retrieval accuracy.

## Sources

- Discord source — private provenance retained locally.
- [https://x.com/aipintodev/status/2101036073719570869](https://x.com/aipintodev/status/2101036073719570869) — access: `fetched`; review: `visible_post_text_reviewed`.
- [https://t.co/8d0Bc6oGQv](https://t.co/8d0Bc6oGQv) — access: `fetched`; review: `source_text_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
