---
id: waitless
title: "Waitless: UI timeout investigation advisor"
category: operations
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Waitless: UI timeout investigation advisor

## What

Suggest the first area to investigate after Selenium stabilization times out.

## How Jev fits

Choice evaluates an allowlisted diagnostic snapshot covering network activity, DOM churn, animations and WebSockets.

## Why and impact

Ten author cases: corrected deterministic baseline 90%, Jev 100%, including one ambiguous mixed-signal case.

## Limits and reuse

An optional diagnostic hint, not proof of root cause or a replacement for stabilization logic. Very small development sample.

## Sources

- Discord source — private provenance retained locally.
- [https://github.com/godhiraj-code/waitless/tree/poc/typesafe-smart-doctor](https://github.com/godhiraj-code/waitless/tree/poc/typesafe-smart-doctor) — access: `fetch_failed`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
