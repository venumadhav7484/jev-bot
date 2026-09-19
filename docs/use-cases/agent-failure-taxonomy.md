---
id: agent-failure-taxonomy
title: "Agent-session failure classification"
category: operations
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Agent-session failure classification

## What

Label failure reasons across agent execution logs.

## How Jev fits

Jev classifies full sessions into a predefined failure taxonomy after logs are retrieved.

## Why and impact

Recording resolves count discrepancy:323sessions downloaded,321classified and2failed. UI reports3m41s acquisition,14seconds classification,2.0Mtokens and$0.08;267yes/54no judgments.

## Limits and reuse

Eleven sampled frames; no human-label agreement benchmark.83% successful is the model judgment distribution, not accuracy. Concurrent throughput is not individual request latency. Conditional failure explanation remains separate from independent success verdict; two processing failures must remain in denominator.

## Sources

- [https://x.com/danmana/status/2100545412780220877](https://x.com/danmana/status/2100545412780220877) — access: `fetched`; review: `demo_trace_reviewed`.
- [https://t.co/VRQKvuxvJV](https://t.co/VRQKvuxvJV) — access: `fetched`; review: `demo_trace_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
