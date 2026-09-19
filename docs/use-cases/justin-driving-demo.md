---
id: justin-driving-demo
title: "Driving prototype: Justin’s FSD-inspired demo"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Driving prototype: Justin’s FSD-inspired demo

## What

Developer shares a driving-control experiment framed as recreating Tesla FSD in under an hour.

## How Jev fits

Structured simulator world state and finite driving options feed Jev; local routing, candidate generation and braking execute actions. Recording includes one small-town destination completion.

## Why and impact

Shows rapid prototyping interest; build-time claim is not autonomous-driving performance.

## Limits and reuse

No safety, real-world operation, reliability or equivalence to Tesla is established. Do not recommend deployment based on promotional analogy. Source review: Local geometry, candidate generation and braking surround Jev. Simulator behavior and aggressive rubric do not establish safe real-world autonomous driving. Media review: Reviewed40 sampled frames plus narration: structured world state feeds finite driving choices; city segment stops/turns, author switches to small-town environment and reaches destination confirmation, then switches to interstate. One simulator completion, not Tesla equivalence. Local route/candidate/braking code and reset/environment choice affect result; no physical test.

## Sources

- Discord source — private provenance retained locally.
- [https://x.com/jpschroeder/status/2100347770867458384?s=20](https://x.com/jpschroeder/status/2100347770867458384?s=20) — access: `fetched`; review: `demo_trace_reviewed`.
- [Author-linked implementation artifact](https://github.com/standardagents/jevpilot) — discovered via [external source](https://x.com/jpschroeder/status/2100347770867458384); access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
