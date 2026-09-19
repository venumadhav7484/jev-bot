---
id: private-process-comparison
title: "Internal routing and comment judgments: mixed screenshot results"
category: quality
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Internal routing and comment judgments: mixed screenshot results

## What

A developer compares Jev with existing LLM-driven routing and comment-processing workflows.

## How Jev fits

Screenshots show routing decisions with fallbacks, pairwise comment judgments at a fixed threshold, and real/synthetic comment subsets. Exact task definitions and judge protocol are not provided.

## Why and impact

In 106 hand-labeled development routing cases, reported final accuracy rises from 95.3% to 98.1% and median latency falls from 644ms to 181ms. Other tables also report lower latency.

## Limits and reuse

Three images were inspected. Mixed-request handling worsens from 8/8 with no false alarms to 7/8 with two false alarms; real-comment score is 73.3% versus stored Gemini 75.6%. A 34s versus 2.3s comparison covers two baseline stages but only one Jev stage. Cost columns are incomplete or use different units. These tables do not support the author’s blanket faster/cheaper/more-accurate claim. No independent reproduction.

## Sources

- Discord source — private provenance retained locally.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
