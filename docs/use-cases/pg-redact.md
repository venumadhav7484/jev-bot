---
id: pg-redact
title: "pg-redact: contextual PII masking"
category: security
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# pg-redact: contextual PII masking

## What

Mask selected personal information according to viewer role.

## How Jev fits

The author describes Jev tagging meaningful personal fields and a Neon Postgres redact function returning role-specific masked text.

## Why and impact

Preserves readable non-personal content rather than hiding whole columns.

## Limits and reuse

The post's database-to-browser protection claim does not imply raw content never reaches the model provider. A reply identifies local token classifiers as an alternative.

## Sources

- Discord source — private provenance retained locally.
- [https://pg-redact.vercel.app/](https://pg-redact.vercel.app/) — access: `fetch_failed`; review: `not_reviewed`.
- [https://github.com/rishi-raj-jain/pg-redact](https://github.com/rishi-raj-jain/pg-redact) — access: `fetch_failed`; review: `not_reviewed`.
- [https://x.com/rishi_raj_jain_/status/2100606501501169726](https://x.com/rishi_raj_jain_/status/2100606501501169726) — access: `fetch_failed`; review: `not_reviewed`.
- [https://huggingface.co/openai/privacy-filter](https://huggingface.co/openai/privacy-filter) — access: `fetched`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
