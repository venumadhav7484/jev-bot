---
id: ugc-classifier
title: "User-generated-content classification"
category: content
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# User-generated-content classification

## What

A team tests Jev in an existing content-classification agent.

## How Jev fits

Initial Jev judgments expose ambiguous grading criteria. Follow-up applies the rubric as deterministic code over Jev attribute booleans; it is not only a prompt rewrite.

## Why and impact

On the same 88-bio Astra-derived gold set over three runs, reported ordinal exact agreement rises from 44.3–46.6% to 88.6–89.8%; Luna is 35.2–38.6%. Initial Jev misses adjacency and mowing floors; revised pipeline clears the reported floors. Revised p50 is 320 ms versus 24 s, with reported run cost $0.018 versus $0.070.

## Limits and reuse

Gold labels come from another model, not established truth. Same development cohort before and after tuning; no independent held-out test or reproduction. Improvement combines model judgments and code-owned rules. First report explicitly says Jev is not a drop-in replacement; retain initial failures alongside revised results.

## Sources

- Discord source — private provenance retained locally.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
