---
id: stll-house-style
title: "STLL: paragraph selection for document house styles"
category: domain-review
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# STLL: paragraph selection for document house styles

## What

Reformat an existing contract with a selected house style.

## How Jev fits

A separate generative model describes available styles once. Jev chooses a known style per paragraph using existing document structure; deterministic DOCX tooling applies changes.

## Why and impact

Separates semantic style selection from document serialization; recorded contract formatting changes visibly.

## Limits and reuse

Early demo; broad content-preservation and OOXML compatibility untested here. Author says Folio support is forthcoming, so README availability alone does not establish shipped Jev integration. External follow-up posted after the frozen capture cutoff.

## Sources

- Discord source — private provenance retained locally.
- [https://x.com/jan__kubica/status/2100636173249007696?s=20](https://x.com/jan__kubica/status/2100636173249007696?s=20) — access: `signed_in_browser_and_public_media`; review: `demo_trace_reviewed`.
- [Author-linked workflow evidence](https://x.com/jan__kubica/status/2101224078707208245) — discovered via [external source](https://x.com/jan__kubica/status/2100636173249007696); access: `public_media_extracted`; review: `demo_trace_reviewed`.
- [Author-linked workflow evidence](https://github.com/stella/folio) — discovered via [external source](https://x.com/jan__kubica/status/2101224010021282302); access: `public_web_reader`; review: `readme_reviewed`.
- [Author-linked workflow evidence](https://x.com/jan__kubica/status/2101224010021282302) — discovered via [external source](https://x.com/jan__kubica/status/2100636173249007696); access: `public_media_extracted`; review: `demo_trace_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
