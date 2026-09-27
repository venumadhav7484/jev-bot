---
id: system-one-adapter
title: "System One Adapter: compare Jev with an LLM on the same calls"
category: developer-tools
evidence: author-reported
reviewed_on: 2026-09-27
independently_reproduced: false
---

# System One Adapter: compare Jev with an LLM on the same calls

## What

A drop-in replacement for the SDK's system_one call that answers with an LLM, so the same Noul, Choice and Score requests can be compared across models.

## How Jev fits

The adapter asks an OpenAI-compatible or Anthropic model to return probabilities or discrete answers in the same shape; an included finding-routing example compares unfiltered, filtered and guarded routing by important misroutes and review workload.

## Why and impact

Makes cost, speed and quality comparisons apples to apples, and measures review workload rather than latency alone.

## Limits and reuse

Example cases and responses are synthetic and are not evidence of Jev accuracy. LLM "probabilities" are not calibrated the same way.

## Sources

- [GitHub - zuwasi/jev-limitations: MIT-licensed experiment: context f...](https://github.com/zuwasi/jev-limitations) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
