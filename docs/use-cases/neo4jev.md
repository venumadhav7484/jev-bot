---
id: neo4jev
title: "Neo4jev: semantic graph traversal"
category: retrieval
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Neo4jev: semantic graph traversal

## What

Navigate a graph toward a natural-language goal.

## How Jev fits

Jev chooses among neighboring nodes and evaluates goal completion with Noul; the graph engine owns traversal and available edges.

## Why and impact

Demonstrates composition of semantic judgments with exact graph structure.

## Limits and reuse

No general path-optimality or completeness result is established by the post. Source review: Excluded edges cannot be found; semantic goal Noul is not exact target verification. Sum of log probabilities prevents underflow but does not itself remove path-length bias. Multi-branch traversal may require multiple calls per depth, despite one call per visited-node hop. Live graph access does not prove Jev navigation when stand-ins are active.

## Sources

- [https://github.com/jexp/neo4jev](https://github.com/jexp/neo4jev) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
