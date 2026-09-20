---
id: pi-jev-sentinel
title: "Pi Jev Sentinel: intent and risk checks"
category: security
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Pi Jev Sentinel: intent and risk checks

## What

A Pi coding-agent extension screens incoming material and proposed tool calls.

## How Jev fits

The author separated overlapping intent and risk labels after feedback, then added extra-context retrieval, task pinning and response checks. Application policy decides when to run, warn or ask.

## Why and impact

Illustrates improving question design through observed ambiguities instead of assuming one Choice can express intent, risk and approval simultaneously.

## Limits and reuse

In the first example GPT already rejected an injected upload instruction; Jev paused a subsequent file read with a near tie. This does not prove independent attack prevention. Later planted-trap tests and secret scrubbing are author reports, not a security audit.

## Sources

- [github.com](https://github.com/harshwasan/pi-jev-sentinel) — access: `fetched`; review: `sections_reviewed`.
- [x.com](https://x.com/harsh_w98/status/2101366309875548252) — access: `fetched`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
