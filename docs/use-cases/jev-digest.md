---
id: jev-digest
title: "jev-digest: verbatim passages for an agent instead of whole pages"
category: retrieval
evidence: author-reported
reviewed_on: 2026-09-27
independently_reproduced: false
---

# jev-digest: verbatim passages for an agent instead of whole pages

## What

An MCP tool and Python API search the web or local documents and return only the passages relevant to a question, with sources.

## How Jev fits

Jev selects passages; the tool returns original wording with URLs, sections and passage IDs and flags topics without evidence. It does not generate a summary.

## Why and impact

In one reported Codex research run, input tokens fell 67% and tool rounds halved against built-in search.

## Limits and reuse

The README calls it a working proof of concept with small benchmarks; one question is not a general result. Passage selection is not fact verification, and missed passages are silent.

## Sources

- [GitHub - pr0ta9/jev-digest: Give AI agents relevant passages from w...](https://github.com/pr0ta9/jev-digest) — access: `fetched`; review: `readme_reviewed`.
- [https://x.com/prIo_Ol/status/2103479500394967062](https://x.com/prIo_Ol/status/2103479500394967062) — access: `fetched`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
