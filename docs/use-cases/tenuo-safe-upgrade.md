---
id: tenuo-safe-upgrade
title: "safe-upgrade: judgment, workflow and authority are separate"
category: agents
evidence: author-reported
reviewed_on: 2026-09-24
independently_reproduced: false
---

# safe-upgrade: judgment, workflow and authority are separate

## What

A dependency-upgrade example combines Jev decisions, LangGraph execution flow and Tenuo-scoped worker permissions.

## How Jev fits

Code computes eligible actions first. Jev chooses among that set; the runtime validates the label and handles uncertain or failed responses. A separate authorization layer limits each selected worker’s actual tools and resources.

## Why and impact

Shows how a useful semantic router can sit inside a workflow without becoming its permission authority. Installation and passing tests alone may miss migration risks, so supplied repository evidence drives bounded review questions.

## Limits and reuse

Article examples include illustrative response values. Architecture claims and code excerpts do not independently prove complete authorization enforcement, upgrade correctness or performance. Permissions must remain narrower than whatever action the model prefers.

## Sources

- [Jev in practice: typed decisions, scoped authority | Tenuo](https://tenuo.ai/blog/jev-scoped-authority) — access: `fetched`; review: `sections_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
