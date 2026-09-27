---
id: jev-secrets
title: "jev-secrets: pseudonymise requests, restore the answers"
category: security
evidence: author-reported
reviewed_on: 2026-09-27
independently_reproduced: false
---

# jev-secrets: pseudonymise requests, restore the answers

## What

A middleware for PHP, JavaScript and Python replaces names, keys and other secrets in a Jev request before sending and restores them in the answers.

## How Jev fits

Each replaced word keeps its shape (letters for letters, digits for digits), the same word gets the same stand-in everywhere including in questions, and answers return with original question ids and choice labels.

## Why and impact

On 67 labelled questions over 50 PII-heavy requests, the default configuration got 64 right against 67 for the plain request; date and time comparisons kept their answers.

## Limits and reuse

Pseudonymisation, not anonymisation: the mapping stays in memory. What is replaced is lost to the model (for example whether an email domain is a company’s), and comparing two plain numbers passed as values fails.

## Sources

- [GitHub - Fox-Islam/jev-secrets: Pseudonymisation wrapper for Jev qu...](https://github.com/Fox-Islam/jev-secrets) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
