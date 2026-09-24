---
id: kassad
title: "Kassad: stage-wide guardrail questions with measured failure paths"
category: security
evidence: author-reported
reviewed_on: 2026-09-24
independently_reproduced: false
---

# Kassad: stage-wide guardrail questions with measured failure paths

## What

A .NET guardrails library groups stage policies into one Jev request and maps typed answers to application verdicts.

## How Jev fits

ASP.NET middleware and an HTTP handler consume allow, flag, review or block decisions. The author links a harness over named injection, toxicity and claim datasets, with threshold-specific measures.

## Why and impact

The source report preserves practical integration problems: invalid requests, unordered Choice keys, run-to-run variation and a WAF rejection on one prompt.

## Limits and reuse

Reported datasets do not by themselves establish guardrail effectiveness or correct labels. Parse keys by name, retain failed calls as failures and measure the enforced policy, not only model answers. One reported 403 does not establish a general provider limit or root cause. No security certification or independent reproduction.

## Sources

- [GitHub - jacob-berendsohn/kassad](https://github.com/jacob-berendsohn/kassad) — access: `fetched`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
