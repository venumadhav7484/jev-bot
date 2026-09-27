---
id: jev-decision-bench
title: "jev-decision-bench: compare Jev and LLMs on your own decisions"
category: experiments
evidence: author-reported
reviewed_on: 2026-09-27
independently_reproduced: false
---

# jev-decision-bench: compare Jev and LLMs on your own decisions

## What

A self-hosted toolkit compares Jev with conventional LLMs on bounded decisions: the same state, rubric and permitted answers.

## How Jev fits

Versioned experiment packages cover intent routing (BANKING77), policy decisions (HateCheck) and search relevance (TREC Deep Learning), with runs, scores and comparisons stored as artifacts; other task families are planned.

## Why and impact

Published snapshots: Choice 81.0% for Jev against 77.9–86.1% for five LLMs; Noul 98.2% against 95.1–100%; Score 47.4% against 42.9–47.4%. Jev fell within the range of the five LLMs on all three types and tied the best Score result.

## Limits and reuse

Snapshots are not a single leaderboard; per-task results, reliability and latency are in the repository reports. Token counts are provider-reported. Several task families have no dataset yet.

## Sources

- [GitHub - Tenkei/jev-decision-bench: A reproducible, self-hosted ben...](https://github.com/Tenkei/jev-decision-bench) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
