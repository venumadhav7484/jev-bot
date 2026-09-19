---
id: dinostomp
title: "Dinostomp: checking evaluation instruments"
category: quality
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Dinostomp: checking evaluation instruments

## What

An open-source evaluation harness adds Jev as a refusal judge and tool router.

## How Jev fits

The author describes one Choice question per item through /v1/systemone, storing probabilities with every record and running a blind control.

## Why and impact

The important pattern is validating the scorer and control setup, rather than treating a score alone as evidence.

## Limits and reuse

Integration is author-reported; no independent evaluation was run. Judge reliability and routing accuracy still need workload-specific tests. Source review: Evaluation tooling can expose label, scorer, threshold and drift problems. Small authored examples and self-planted failures are development evidence; evaluate held-out application cases and retain a separate construct-validity judgment.

## Sources

- [https://github.com/collapseindex/dinostomp](https://github.com/collapseindex/dinostomp) — access: `fetched`; review: `scoped_repository_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
