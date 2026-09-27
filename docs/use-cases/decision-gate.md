---
id: decision-gate
title: "decision-gate: rate, spend and privacy limits for Jev loops"
category: developer-tools
evidence: author-reported
reviewed_on: 2026-09-27
independently_reproduced: false
---

# decision-gate: rate, spend and privacy limits for Jev loops

## What

An npm library is the single path through which code sends Jev requests when it asks many questions in a loop.

## How Jev fits

It waits for room under the account’s rate limit, pauses all callers together on 429s, enforces per-run and daily spend ceilings, caches answers scoped to the exact questions, and redacts emails, known secret formats and credentials before anything is sent or cached.

## Why and impact

Removes the three volume failures the author names: retry storms, paying twice for the same question, and runaway loops.

## Limits and reuse

Pre-1.0 and unofficial; interfaces may change. Redaction covers known formats only. Rewording a question invalidates its cache by design.

## Sources

- [https://www.npmjs.com/package/decision-gate](https://www.npmjs.com/package/decision-gate) — access: `access_failed`; review: `inaccessible_content_pending`.
- [GitHub - zachlandes/decision-gate: Rate and spend limits for code t...](https://github.com/zachlandes/decision-gate) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
