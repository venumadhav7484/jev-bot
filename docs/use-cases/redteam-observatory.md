---
id: redteam-observatory
title: "Observatory: inspect guardrail false positives and missed attacks"
category: security
evidence: author-reported
reviewed_on: 2026-09-24
independently_reproduced: false
---

# Observatory: inspect guardrail false positives and missed attacks

## What

An experimental workbench helps authors define, test and share Jev guardrail policies.

## How Jev fits

Users compare policies with matched attack and legitimate-behavior examples. The interface separates authored expectations, native model answers, application decisions and missing results.

## Why and impact

Encourages inspection of both missed attacks and unnecessary blocking instead of trusting one aggregate score.

## Limits and reuse

Synthetic test exploration is not a security certification. Public page text describes behavior, but live runs, implementation and test-label quality were not independently evaluated. A displayed chart or saved artifact is not proof of deployed enforcement.

## Sources

- [Observatory — Put your AI’s rules to the test.](https://redteam-observatory.wizard.chatgpt.site/) — access: `fetched`; review: `landing_page_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
