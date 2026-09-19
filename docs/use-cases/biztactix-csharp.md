---
id: biztactix-csharp
title: "C# SDK port before live access"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# C# SDK port before live access

## What

Biztactix-Ryan/TypeSafe.Sdk.C- ports Python and JavaScript clients.

## How Jev fits

Developer authored C# wrapper while awaiting access.

## Why and impact

Potential .NET integration option.

## Limits and reuse

Live API compatibility explicitly untested at announcement; distinct from Hawxy SDK. Source review: Treat first live use as compatibility validation; repository/package availability differs. Debug logs redactheaders butnotstatebodies,totalretrybudgetoffdefault. Unknown-answer behavior needs code check; SDK contract tests are not Jevsemanticaccuracy evidence.

## Sources

- [https://github.com/Biztactix-Ryan/TypeSafe.Sdk.C-](https://github.com/Biztactix-Ryan/TypeSafe.Sdk.C-) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
