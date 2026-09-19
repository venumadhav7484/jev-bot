---
id: jev-axi
title: "Jev-axi: CLI offloading wrapper"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Jev-axi: CLI offloading wrapper

## What

Developer starts a CLI wrapper for agents to offload tasks to Jev.

## How Jev fits

CLI exposes typed questions,ranking,filtering,diff/log review,guards and agent supervision. Host code owns thresholds,redaction,caching,local allow rules and hooks.

## Why and impact

Reusable command-line adapter may reduce per-project wiring.

## Limits and reuse

Author benchmark on a390k-line repository finds no demonstrated general coding-agent cost saving: sixruns per condition,session-dependent saving/penalty,and mean/median disagreement. Report says skill was not loaded unprompted. Guard-exec fails open on missingkey/network unless explicitly configured otherwise. Safetyhook44/44authoredcases does not establish general security. Confidence bands remain uncalibrated application policy; derived Noul confidence is wrapper math. No independent reproduction.

## Sources

- Discord source — private provenance retained locally.
- [https://www.npmjs.com/package/jev-axi](https://www.npmjs.com/package/jev-axi) — access: `browser_readable`; review: `readme_reviewed`.
- [https://github.com/shiftynick/jev-axi](https://github.com/shiftynick/jev-axi) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
