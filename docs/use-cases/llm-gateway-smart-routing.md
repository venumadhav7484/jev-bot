---
id: llm-gateway-smart-routing
title: "LLM Gateway: Jev rates requests before routing"
category: routing
evidence: author-reported
reviewed_on: 2026-09-27
independently_reproduced: false
---

# LLM Gateway: Jev rates requests before routing

## What

An LLM gateway’s “smart” model string reads each request and routes it among up to 30 models an organization chooses.

## How Jev fits

Organizations pick a classifier: none (cheapest capable model) or Jev, which rates the request first so a one-line fix goes to a cheap model and a hard problem to a frontier one.

## Why and impact

Moves the difficulty classification out of application code, where prompts, model lists and fallbacks tend to drift.

## Limits and reuse

Vendor beta announcement; no routing accuracy or cost savings published. A misrated hard request goes to a model that may answer it wrongly.

## Sources

- [Automatic Model Selection by Request Difficulty](https://llmgateway.io/blog/automatic-model-selection) — access: `fetched`; review: `article_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
