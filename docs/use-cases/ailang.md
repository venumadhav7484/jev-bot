---
id: ailang
title: "AILANG: typed decision effects"
category: developer-tools
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# AILANG: typed decision effects

## What

A typed functional language adds Jev through OpenRouter.

## How Jev fits

Noul, Choice and Score become algebraic data types. A gate returns Act, Escalate or Ungateable, has no default threshold, and distinguishes uncertainty from wrong type.

## Why and impact

Author reports matching Flash accuracy on 20 hand-labeled routing decisions at roughly 1/30 latency and 1/10 cost; live shadowing was underway.

## Limits and reuse

Small internal sample, not a general benchmark. Keep explicit effects and fallback paths distinct from probability judgments.

## Sources

- Discord source — private provenance retained locally.
- [https://github.com/sunholo-data/ailang-packages/tree/main/packages/decisions](https://github.com/sunholo-data/ailang-packages/tree/main/packages/decisions) — access: `fetch_failed`; review: `not_reviewed`.
- [https://github.com/sunholo-data/ailang/blob/dev/design_docs/implemented/v0_40_1/m-ai-decide-system-one.md](https://github.com/sunholo-data/ailang/blob/dev/design_docs/implemented/v0_40_1/m-ai-decide-system-one.md) — access: `fetch_failed`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
