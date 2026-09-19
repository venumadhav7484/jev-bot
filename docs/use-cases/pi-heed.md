---
id: pi-heed
title: "Pi-heed: conversational constraints at tool execution"
category: security
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Pi-heed: conversational constraints at tool execution

## What

A Pi extension tracks user constraints as runtime state.

## How Jev fits

Latest README describes a ledger where the main model records constraints with exact user quotes; host validates receipts and enforces paths/scopes. Jev checks free-text violations, exceptions and permission lifts. Earlier interpreter results refer to a different pipeline.

## Why and impact

Author reports 8/13 changing-rule violations without the guard versus 0/13 with it; unchanged-rule baseline already had zero violations in 30 runs. Separate scripted benchmark and historical replay are not equivalent evidence.

## Limits and reuse

Fails open on timeout/error and uncertainty. Reported Slack-webhook restriction scored 0.76–0.88 and executed. Pattern-based shell detection, intervention budget and limited live scenarios constrain coverage. Calibration, field-order and wording experiments are small and project-specific; no independent reproduction.

## Sources

- [https://github.com/Nyarlathoteppppp/pi-heed](https://github.com/Nyarlathoteppppp/pi-heed) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
