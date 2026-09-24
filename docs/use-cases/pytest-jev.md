---
id: pytest-jev
title: "pytest-jev: semantic assertions with explicit uncertainty failures"
category: developer-tools
evidence: author-reported
reviewed_on: 2026-09-24
independently_reproduced: false
---

# pytest-jev: semantic assertions with explicit uncertainty failures

## What

A pytest plugin turns meaning-based assertions into typed Jev questions.

## How Jev fits

All claims about a text share a request. Code interprets probability mass and thresholds, fails uncertain answers and caches results for repeated tests.

## Why and impact

Useful for testing properties that exact substring checks miss. Author reports matching one Claude configuration on 12 example tests; this small demonstration does not establish general judge reliability.

## Limits and reuse

Cached reruns test the saved judgment rather than making a fresh independent observation. A confident semantic pass can still be wrong; keep deterministic schema checks and human-labelled false-pass tests. Published speed/cost projections depend on cache and workload.

## Sources

- [GitHub - allebee/pytest-jev: Semantic assertions for pytest: test w...](https://github.com/allebee/pytest-jev) — access: `fetched`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
