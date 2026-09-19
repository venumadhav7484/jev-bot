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

No adversarial detection coverage established. Do not replace sandboxing, provenance checks or deterministic controls with a probabilistic verdict.

## Sources

- Discord source — private provenance retained locally.
- [https://github.com/luantak/is-malicious](https://github.com/luantak/is-malicious) — access: `fetched`; review: `not_reviewed`.
- [https://github.com/luantak/is-malicious/](https://github.com/luantak/is-malicious/) — access: `fetched`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
