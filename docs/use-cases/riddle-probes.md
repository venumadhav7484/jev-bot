---
id: riddle-probes
title: "Reasoning probes: date arithmetic, literal reading and letter counts"
category: limitations
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Reasoning probes: date arithmetic, literal reading and letter counts

## What

Screenshot-backed closed-choice probes expose arithmetic, literal-reading and wording-sensitive failures.

## How Jev fits

A demo supplies a riddle and candidate answers to Jev, then displays probabilities, confidence and an option-order check.

## Why and impact

Friday11pm plus25hours is Sunday midnight, but screenshot chooses Saturday at1.00 with0.99confidence. A surgeon explicitly identified as father is classified as mother at0.59 versus father0.40. A strawberry-count screenshot chooses two letters R at81% without quotes, but three at65% with quotes.

## Limits and reuse

Illustrative results, not a representative benchmark. Surgeon UI reports a different result after reversing option order; raw repeated calls not inspected. Use deterministic date arithmetic and evaluate wording/ordering on held-out examples. A high confidence field does not guarantee correctness. Earlier screenshot correction: a separate strawberry test ranks the correct count of three first at56%, despite its failure caption. A rope-ladder probe explicitly fixes the boat against vertical motion yet selects four unchanged rungs at69%; preserve that unusual premise. A five-foot-depth score returns4.98/9 with99%confidence, illustrating approximate numeric output.

## Sources

- Discord source — private provenance retained locally.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
