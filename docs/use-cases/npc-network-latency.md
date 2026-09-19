---
id: npc-network-latency
title: "MMO NPC experiment: network overhead limits responsiveness"
category: quality
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# MMO NPC experiment: network overhead limits responsiveness

## What

A developer reports testing Jev for NPC decisions in an MMO experiment.

## How Jev fits

A linked PDF is offered as the report; the Discord post identifies EU-to-test-infrastructure latency as a blocker. The PDF was inaccessible through the web tool.

## Why and impact

Author reports up to 320 ms network overhead. This is a deployment constraint worth preserving beside low model-latency claims.

## Limits and reuse

No workload details or independent timings were verified. Do not generalize one route or test infrastructure to every deployment, and do not present the inaccessible PDF as reviewed.

## Sources

- Discord source — private provenance retained locally.
- [https://git.sub-net.at/Sub-Net-Public/llm-benchmark/src/branch/main/typesafe-jev/report.pdf](https://git.sub-net.at/Sub-Net-Public/llm-benchmark/src/branch/main/typesafe-jev/report.pdf) — access: `fetched`; review: `not_reviewed`.
- [git.sub-net.at](https://git.sub-net.at/Sub-Net-Public/llm-benchmark/-/summary-card) — access: `nontext_not_inspected`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
