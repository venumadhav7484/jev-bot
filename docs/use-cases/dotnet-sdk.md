---
id: dotnet-sdk
title: ".NET SDK: typed builders and Microsoft.Extensions.AI"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# .NET SDK: typed builders and Microsoft.Extensions.AI

## What

Hawxy/TypeSafeAI.Net supplies community .NET client.

## How Jev fits

Strongly typed input/output builders and Microsoft.Extensions.AI patterns for routing, guardrails and evaluations.

## Why and impact

Reusable integration tool for .NET applications.

## Limits and reuse

Source inspection and version compatibility pending; guardrail examples do not establish security correctness. Source review: Middleware thresholds are policies requiring task labels, not security proof. Review result does not itself block action. Router base experimental upstream, tracing can expose bodies at Trace level, and retries/cancellation affect costs. Stand-in chat sample is not live generative integration validation.

## Sources

- Discord source — private provenance retained locally.
- [https://github.com/Hawxy/TypeSafeAI.Net](https://github.com/Hawxy/TypeSafeAI.Net) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
