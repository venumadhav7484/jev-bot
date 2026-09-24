---
id: jev-clean
title: "jev-clean: judge proposed data repairs, execute them locally"
category: data
evidence: author-reported
reviewed_on: 2026-09-24
independently_reproduced: false
---

# jev-clean: judge proposed data repairs, execute them locally

## What

An experimental CSV-cleaning tool separates candidate generation, semantic judgment and deterministic mutation.

## How Jev fits

Profilers and local code propose bounded repairs. Jev answers applicability and ordered-risk questions; policy checks full distributions and deterministic eligibility before an executor commits or rejects a batch. Every outcome gets an evidence-linked audit record.

## Why and impact

Offers an inspectable pattern for accepted, rejected and abstained repairs, with replay and rollback. The model does not write arbitrary cleaning code or silently mutate the original table.

## Limits and reuse

Experimental single-CSV scope with schema and policy inputs. Mocked tests validate application behavior, not live judgment accuracy. Audit hashes establish correspondence to saved evidence, not truth or safety; median/mode imputation can still distort meaning. No independent data-quality evaluation.

## Sources

- [GitHub - Kunyanli230/jev-clean](https://github.com/Kunyanli230/jev-clean) — access: `fetched`; review: `sections_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
