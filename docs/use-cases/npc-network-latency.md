---
id: npc-network-latency
title: "MMO NPC benchmark: useful context, framing failures and deployment mismatch"
category: quality
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# MMO NPC benchmark: useful context, framing failures and deployment mismatch

## What

Author evaluates Jev against three NPC heuristic families on 46 hand-built scenarios, repeated five times, plus 110 defender prompt-variant calls. Project ultimately not adopted because hosted API conflicts with its self-hosted deployment requirement.

## How Jev fits

Batched Choice, Noul and Score assess temperament, routines and pursuit. Proposed event-driven overlay keeps deterministic heuristics active while awaiting results, then applies confidence and cross-question agreement gates. Deployment proposal was not adopted.

## Why and impact

Routine matches 11/13 author-labeled sensible outcomes; contextual temperament judgments address information missing from HP-only rule. Defender Noul holds in all 11 scenarios under two framings; Choice changes policy but misses range and threat edge cases. Original 553 ms median included fresh TCP/TLS setup; corrected small sample reports 220-225 ms warm floor and 265 ms median including a 636 ms first call.

## Limits and reuse

Report read, not reproduced. Hand-labeled scenarios are not representative production evaluation. Five repeats show no Noul boundary flips but 3/35 Choice flips, so not deterministic-output proof. Selected low-confidence examples do not establish calibration or validate 0.7 threshold. Corrected latency sample is small and report retains inconsistent later floor/whole-battery wording. Cost table assumes hypothetical prices, not actual Jev billing. Hosted measurements miss this project's 50 ms tick budget; cannot generalize to every route or deployment. Typed outputs can still be wrong.

## Sources

- Discord source — private provenance retained locally.
- [https://git.sub-net.at/Sub-Net-Public/llm-benchmark/src/branch/main/typesafe-jev/report.pdf](https://git.sub-net.at/Sub-Net-Public/llm-benchmark/src/branch/main/typesafe-jev/report.pdf) — access: `public_content_recovered`; review: `report_reviewed`.
- [git.sub-net.at](https://git.sub-net.at/Sub-Net-Public/llm-benchmark/-/summary-card) — access: `public_image_extracted`; review: `image_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
