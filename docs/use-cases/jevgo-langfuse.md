---
id: jevgo-langfuse
title: "jevgo: Go client with optional Langfuse instrumentation"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# jevgo: Go client with optional Langfuse instrumentation

## What

fgn/jevgo wraps TypeSafe System One API.

## How Jev fits

Claims feature parity with official Python/TypeScript SDKs and optional Langfuse instrumentation.

## Why and impact

Supports typed calls plus observability in Go services.

## Limits and reuse

Source/version review pending; parity is author claim, not tested guarantee. Source review: Community compatibility claims need live version checks. Retries can add cost; total deadline must be configured. Tracing sends state/output to Langfuse and debug bodies may contain sensitive input. Strict distribution validation protects contracts, not semantic correctness. Source review: Pinned v0.3.0 documentation establishes client contract, not inference accuracy. Unknown answer kinds retained in this version; older summaries saying dropped/no release are stale. Configure whole-call deadline and treat trace bodies as sensitive.

## Sources

- Discord source — private provenance retained locally.
- [https://pkg.go.dev/github.com/fgn/jevgo](https://pkg.go.dev/github.com/fgn/jevgo) — access: `fetched`; review: `api_documentation_reviewed`.
- [https://github.com/fgn/jevgo](https://github.com/fgn/jevgo) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
