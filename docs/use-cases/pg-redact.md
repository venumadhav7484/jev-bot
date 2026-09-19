---
id: pg-redact
title: "pg-redact: contextual PII masking"
category: security
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# pg-redact: contextual PII masking

## What

Mask selected personal information according to viewer role.

## How Jev fits

The author describes Jev tagging meaningful personal fields and a Neon Postgres redact function returning role-specific masked text.

## Why and impact

Inspected role-switching demo preserves non-sensitive text while masking selected spans; includes decoy location words and spelled-out phone example.

## Limits and reuse

Ten sampled frames, synthetic selected examples. Candidate generation can miss sensitive spans; displayed found3 versus row5 counters are not reconciled. Role selector is not proof of secure authorization. Browser-facing database masking does not imply source text stays out of Jev requests; assess provider egress separately.

## Sources

- Discord source — private provenance retained locally.
- [https://pg-redact.vercel.app/](https://pg-redact.vercel.app/) — access: `access_failed`; review: `inaccessible_content_pending`.
- [https://github.com/rishi-raj-jain/pg-redact](https://github.com/rishi-raj-jain/pg-redact) — access: `fetched`; review: `readme_reviewed`.
- [https://x.com/rishi_raj_jain_/status/2100606501501169726](https://x.com/rishi_raj_jain_/status/2100606501501169726) — access: `fetched`; review: `demo_trace_reviewed`.
- [https://huggingface.co/openai/privacy-filter](https://huggingface.co/openai/privacy-filter) — access: `fetched`; review: `related_tool_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
