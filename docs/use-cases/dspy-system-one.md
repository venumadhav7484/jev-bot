---
id: dspy-system-one
title: "DSPy 3.4: run decision signatures on Jev"
category: developer-tools
evidence: author-reported
reviewed_on: 2026-09-27
independently_reproduced: false
---

# DSPy 3.4: run decision signatures on Jev

## What

DSPy added native support for System One models, so existing signatures whose outputs are decisions can run on Jev.

## How Jev fits

Output fields must be decisions (bool, a Literal of fixed options, or the new Noul, Choice and Score types), each with a description phrased as the question. Predict maps them to Jev questions; incompatible fields raise an error naming the field. A new optimizer, ReAnchor, targets System One models.

## Why and impact

Teams already using DSPy can switch a decision program to Jev with a two-line configuration change and keep their task definitions.

## Limits and reuse

Integration announcement; no benchmark of optimized versus unoptimized Jev programs reviewed. Signatures needing free-text output still need a generative model.

## Sources

- [Building & Optimizing Jev Programs with DSPy — Cmpnd](https://www.cmpnd.ai/blog/building-jev-programs-with-dspy.html) — access: `fetched`; review: `article_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
