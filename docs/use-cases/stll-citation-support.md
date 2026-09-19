---
id: stll-citation-support
title: "STLL: citation support while drafting"
category: domain-review
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# STLL: citation support while drafting

## What

Check whether a drafted statement matches a retrieved court decision.

## How Jev fits

Application retrieves the decision from its database, supplies passages to Jev and displays a support judgment with a source-passage viewer.

## Why and impact

Makes grounding evidence inspectable alongside the judgment; one trace displays 1,128 ms model latency and 2,186 ms end-to-end.

## Limits and reuse

Experimental example, no independently assessed legal interpretation or error rate. A displayed 99% support judgment does not guarantee the legal statement is correct. Retrieval correctness and authority remain separate checks.

## Sources

- [https://x.com/jan__kubica/status/2100636173249007696?s=20](https://x.com/jan__kubica/status/2100636173249007696?s=20) — access: `signed_in_browser_and_public_media`; review: `demo_trace_reviewed`.
- [Author-linked workflow evidence](https://x.com/jan__kubica/status/2100697651373072413) — discovered via [external source](https://x.com/jan__kubica/status/2100636173249007696); access: `public_media_extracted`; review: `demo_trace_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
