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

Phase 1 shadow report: Jev agreed with 14/20 declared lanes; GLM agreed with 12/17 completed calls and had three timeouts. The author reports approximately 33x lower latency and 11x lower cost. No acting consumer shipped in this phase.

## Limits and reuse

Small internal sample, not a general benchmark. Keep explicit effects and fallback paths distinct from probability judgments. Source review: Fallback is uncalibrated and visibly degraded.20document comparison is not broad accuracy evidence; calls outside existing cost accounting require separate budgets and complete distribution logging. Source review: Shipped integration is shadow-only; 20-document comparison is small and label-conflicted, not production automation evidence. Phase 1 network calls bypass AI budget accounting. Preserve response/model provenance and enforce separate spend/deadline controls; do not promote agreement between models into ground truth.

## Sources

- Discord source — private provenance retained locally.
- [https://github.com/sunholo-data/ailang-packages/tree/main/packages/decisions](https://github.com/sunholo-data/ailang-packages/tree/main/packages/decisions) — access: `fetched`; review: `readme_reviewed`.
- [https://github.com/sunholo-data/ailang/blob/dev/design_docs/implemented/v0_40_1/m-ai-decide-system-one.md](https://github.com/sunholo-data/ailang/blob/dev/design_docs/implemented/v0_40_1/m-ai-decide-system-one.md) — access: `fetched`; review: `implementation_report_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
