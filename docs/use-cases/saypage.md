---
id: saypage
title: "Saypage: constrained page assembly"
category: interfaces
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Saypage: constrained page assembly

## What

Build a page through selections from a component menu.

## How Jev fits

The author explains that Jev selects and composes from 50 prebuilt components and fills arguments. Layouts and sections constrain the choices; full-page requests reportedly average 7k tokens.

## Why and impact

Author reports sub-half-second page assembly and approximately $0.001 per page in this proof of concept.

## Limits and reuse

This establishes constrained assembly, not native free-form HTML generation. Scaling to a much larger component library was discussed but not measured. An earlier draft wrongly attached another developer’s Anthropic copy-generation comment; that belongs to the separate UI-generator case.

## Sources

- Discord source — private provenance retained locally.
- [https://saypage.vercel.app/](https://saypage.vercel.app/) — access: `fetched`; review: `source_text_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
