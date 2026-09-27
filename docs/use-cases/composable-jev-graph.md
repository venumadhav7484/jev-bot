---
id: composable-jev-graph
title: "composable-jev and JevGraph: chaining Jev answers into graphs"
category: developer-tools
evidence: author-reported
reviewed_on: 2026-09-27
independently_reproduced: false
---

# composable-jev and JevGraph: chaining Jev answers into graphs

## What

A library chains Jev questions into a graph whose later nodes read earlier answers; a browser tool builds and runs such graphs.

## How Jev fits

Nodes ask, choose or score over a shared context; combinators such as all, sum and weighted sums combine probabilities; later questions can take earlier nodes as inputs. The author also built logic gates and an 8-bit adder entirely from Jev questions.

## Why and impact

The JevGraph examples classify 5×5 images; the version that asks Jev only about three-pixel runs and leaves the rest to code got 40 of 40 test images right in one request.

## Limits and reuse

The adder and gates are a novelty demonstration, not an efficient use of Jev. The hosted tool sends your key to the author’s server; the README says you cannot confirm the deployed code matches the repository.

## Sources

- [GitHub - Fox-Islam/composable-jev: A library to chain Jev calls, fo...](https://github.com/Fox-Islam/composable-jev) — access: `fetched`; review: `readme_reviewed`.
- [https://jevgraph.lexic.cloud/](https://jevgraph.lexic.cloud/) — access: `fetched`; review: `not_reviewed`.
- [GitHub - Fox-Islam/jev-graph: Semantic computation engine??](https://github.com/Fox-Islam/jev-graph) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
