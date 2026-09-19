---
id: is-malicious
title: "Codebase screening before execution"
category: security
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Codebase screening before execution

## What

A scanner asks whether code may be malicious before running it.

## How Jev fits

Jev supplies semantic risk judgments over repository content.

## Why and impact

Potential screening step for unfamiliar code.

## Limits and reuse

No adversarial detection coverage established. Do not replace sandboxing, provenance checks or deterministic controls with a probabilistic verdict. Source review: Clean scan means no detected high-severity finding among selected files, not safe software. Chunk/window context and skipped artifacts can hide behavior. Derived Noul confidence is application math, not API field. Default moving alias and thresholds require validation.

## Sources

- [https://github.com/luantak/is-malicious](https://github.com/luantak/is-malicious) — access: `fetched`; review: `readme_reviewed`.
- [https://github.com/luantak/is-malicious/](https://github.com/luantak/is-malicious/) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
