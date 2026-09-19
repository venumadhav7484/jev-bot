---
id: pcb-routing
title: "PCB route-candidate selection"
category: engineering
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# PCB route-candidate selection

## What

An experiment asks models to choose PCB routing candidates.

## How Jev fits

Jev performs batched regional judgments; external routing and validation determine connectivity, design-rule violations and length.

## Why and impact

Author reports fast, low-token selection with comparable routing outcomes across small trials.

## Limits and reuse

Comparisons include different agent overhead and concurrency, and costs are API-equivalent estimates rather than invoices. Routing legality comes from deterministic validation, not model confidence.

## Sources

- Discord source — private provenance retained locally.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
