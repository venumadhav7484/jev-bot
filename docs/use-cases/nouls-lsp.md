---
id: nouls-lsp
title: "Nouls: semantic linting in an LSP"
category: developer-tools
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Nouls: semantic linting in an LSP

## What

A community project packages semantic linting as an editor language service.

## How Jev fits

Jev judgments are exposed through a linter and LSP.

## Why and impact

Brings decision feedback into normal development tooling.

## Limits and reuse

Screenshot shows seven warnings and five informational findings across seven files, including partial failure, check-then-act and mixed abstraction. These are proposed diagnostics, not confirmed defects. Function-local context cannot establish whole-program bugs. Label sampling across score bands is useful for detecting misses; default thresholds and disabled false findings require task-specific review. No independent precision/recall evaluation.

## Sources

- [https://github.com/benomahony/nouls](https://github.com/benomahony/nouls) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
