---
id: yingkai-browser
title: "Browser automation: LLM planner with paced Jev actions"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Browser automation: LLM planner with paced Jev actions

## What

Browser automation separates LLM planning from Jev decisions and Playwright execution.

## How Jev fits

Jev returns probability distributions used by browser-control tools rather than free-form text.

## Why and impact

The author reports 40/42 correct tasks in the latest run and roughly 14 seconds for a five-step checkout.

## Limits and reuse

Counting remains a reported failure; tiny pages show no token saving. These are author benchmarks, not independently reproduced results.

## Sources

- [https://github.com/Ying-Kai-Liao/jev-browser/tree/main](https://github.com/Ying-Kai-Liao/jev-browser/tree/main) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
