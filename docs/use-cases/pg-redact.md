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

The post's database-to-browser protection claim does not imply raw content never reaches the model provider. A reply identifies local token classifiers as an alternative. The claim that unapproved data never leaves the database describes the browser-facing boundary. Jev tagging may require transmitting source text upstream; audit that data flow separately. Source review: PII candidate generation and confidence filtering can miss sensitive spans; database masking only protects identified spans. Role-switching demo is not evidence of production authorization enforcement. Source review: Useful complementary local preprocessing, not Jev capability or guaranteed anonymization. Masking can miss sensitive spans and remove needed evidence. Threshold/decoder tuning is distinct from dynamic semantic policy; evaluate in-domain before transmitting data downstream.

## Sources

- Discord source — private provenance retained locally.
- [https://pg-redact.vercel.app/](https://pg-redact.vercel.app/) — access: `access_failed`; review: `inaccessible_content_pending`.
- [https://github.com/rishi-raj-jain/pg-redact](https://github.com/rishi-raj-jain/pg-redact) — access: `fetched`; review: `readme_reviewed`.
- [https://x.com/rishi_raj_jain_/status/2100606501501169726](https://x.com/rishi_raj_jain_/status/2100606501501169726) — access: `fetched`; review: `post_text_reviewed_media_pending`.
- [https://huggingface.co/openai/privacy-filter](https://huggingface.co/openai/privacy-filter) — access: `fetched`; review: `related_tool_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
