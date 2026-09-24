---
id: filelathe
title: "Filelathe: select a viewer, generate only when needed"
category: interfaces
evidence: author-reported
reviewed_on: 2026-09-24
independently_reproduced: false
---

# Filelathe: select a viewer, generate only when needed

## What

A file-viewing application separates deterministic type detection, bounded layout selection and optional generated viewers.

## How Jev fits

Known player matches resolve in code first. Jev chooses catalog layout candidates or invent-versus-inspect for unknown input. Haiku generates only within the invention catalog; validation, one repair and Text/Hex fallback remain in the host.

## Why and impact

Shows how bounded model decisions can reduce how often a generative step is needed while keeping an inspectable fallback.

## Limits and reuse

Jev selects candidates; it does not invent an emulator or generate the Spec. Catalog/schema checks do not prove arbitrary generated viewer behavior is safe. README architecture inspected; live app, full code and security not audited. Measure actual traffic before claiming savings.

## Sources

- [Filelathe — open XM, PDF, CSV, images & more in your browser](https://filelathe.com/) — access: `fetched`; review: `not_reviewed`.
- [https://github.com/rhelmer/filelathe#jev-vs-haiku](https://github.com/rhelmer/filelathe#jev-vs-haiku) — access: `fetched`; review: `sections_reviewed`.
- [GitHub - rhelmer/filelathe](https://github.com/rhelmer/filelathe) — access: `fetched`; review: `sections_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
