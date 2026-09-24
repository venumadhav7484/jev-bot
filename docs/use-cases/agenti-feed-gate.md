---
id: agenti-feed-gate
title: "Agenti: wake the writing model only for useful feed updates"
category: filtering
evidence: author-reported
reviewed_on: 2026-09-24
independently_reproduced: false
---

# Agenti: wake the writing model only for useful feed updates

## What

Scheduled feed watchers put a typed relevance judgment before their main writing model.

## How Jev fits

Runtime fetches and deduplicates entries; Jev screens new entries against the watch question. Matches and uncertain cases reach the writer; provider errors send new entries through the writer fallback.

## Why and impact

Author reports most quiet runs avoided the main model. Adding the first 300 words to title-only state changed an example from an uncertain score to stronger relevance.

## Limits and reuse

Post and later article use different run totals; do not combine them. Zero main-model calls or credits does not mean zero Jev requests or total cost. The article records unrelated run failures and an outage fallback. Small before/after window; missed relevant items and threshold quality were not independently measured.

## Sources

- [Why a Heartbeat's quiet checks are nearly free: decision models —...](https://agenti.chat/en/docs/decision-model) — access: `fetched`; review: `article_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
