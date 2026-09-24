---
id: enterprise-decision-fabric
title: "Decision Fabric: separate model errors from policy errors"
category: engineering
evidence: author-reported
reviewed_on: 2026-09-24
independently_reproduced: false
---

# Decision Fabric: separate model errors from policy errors

## What

An experimental .NET workflow keeps semantic contracts, typed evidence, deterministic policy and execution separate.

## How Jev fits

Jev answers shared-state questions; application gates decide approval, review, denial or escalation. A read-only inspector exposes raw answers and policy reasons for labelled agent-action cases.

## Why and impact

Author reports Jev matched 100 of 111 unique case labels and Claude 102. Weighting repeated calls reverses the ranking, showing why the unit of evaluation matters. Both systems exposed a contract gap: an action can be reversible yet highly consequential.

## Limits and reuse

Synthetic cases, one annotator and labels revised after a Jev pilot. Five repeats in one session do not prove long-term stability. Sample has no real side effects, tenancy or production authentication. Upstream identity, authorization and data-access controls are assumed; model judgments do not replace them.

## Sources

- [GitHub - ghubnab99/jev-enterprise-decision-fabric: Architecture for...](https://github.com/ghubnab99/jev-enterprise-decision-fabric) — access: `fetched`; review: `sections_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
