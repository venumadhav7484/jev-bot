---
id: jev-research-pipeline
title: "Research monitor: code runs the loop, Jev screens sources, an LLM writes"
category: retrieval
evidence: author-reported
reviewed_on: 2026-09-27
independently_reproduced: false
---

# Research monitor: code runs the loop, Jev screens sources, an LLM writes

## What

A single-user pipeline checks new papers and repositories each morning against a few open questions per topic and writes one note per topic into an Obsidian vault.

## How Jev fits

Code gathers candidates from fixed sources. Jev screens each source-question pair: an on-topic check first, then hard gates as yes/no questions and weighted scores; code applies thresholds and routes each pair to keep, review, drop, incomplete or unjudged. A separate LLM writes prose only from kept, verbatim sentences, and ticks in the note steer the next run.

## Why and impact

The author moved from an agent that ran the whole loop ($8–15 a day, 37% of past topics on one theme) to per-pair judgments; an evaluation run cost $0.297, and daily four-topic runs with the new prose step cost about $1–2.

## Limits and reuse

Pilot in daily use by its author. The last evaluation run met 5 of 7 goal conditions, and an independent model judge rated 1 of 3 notes publishable before the prose step was rebuilt. Notes are in Japanese.

## Sources

- [GitHub - shimo4228/jev-research-pipeline: Daily research monitor fo...](https://github.com/shimo4228/jev-research-pipeline) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
