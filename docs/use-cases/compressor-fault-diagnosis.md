---
id: compressor-fault-diagnosis
title: "Fault Diagnosis PoC: manual-grounded triage for a compressor"
category: operations
evidence: author-reported
reviewed_on: 2026-09-27
independently_reproduced: false
---

# Fault Diagnosis PoC: manual-grounded triage for a compressor

## What

A read-only proof of concept monitors a replayed industrial compressed-air unit and suggests a fault diagnosis only when confident.

## How Jev fits

Code computes windows, trends and machine state and raises suspect events; retrieval pulls candidate faults from the machine manual; the decision backend (Jev, an LLM or rules) answers which fault or none, how severe and how sure. A gate turns answers into tickets, review items or log lines.

## Why and impact

The evaluation harness reports precision and recall per fault, lead time against the unit’s own alarms and how often “none of these” is correct, on scenarios with known ground truth.

## Limits and reuse

The README says Jev’s figures are not published pending vendor terms; only the rules baseline results are public, and that baseline misses all four recorded failures. Figures are in-sample. Read-only by design; no control actions.

## Sources

- [GitHub - meddle-connect/jev-fault-diagnosis-poc: Fault Diagnosis Po...](https://github.com/meddle-connect/jev-fault-diagnosis-poc) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
