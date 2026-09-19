---
id: jkudish-tools
title: "Jev MCP and Chromium browser packages"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Jev MCP and Chromium browser packages

## What

Two community packages connect ordinary agents and browsers to Jev.

## How Jev fits

jkudish/jev-mcp exposes decisions as MCP tools; jkudish/jev-browser drives Chromium through Playwright.

## Why and impact

Reusable integration patterns for agent-callable judgment and browser action selection.

## Limits and reuse

Proof-of-concept packages, not verified general compatibility or browser success benchmarks. Source review: DONE and goal judgments share model/state and are not independent task verification even when both agree. Dense-page truncation,unsupportediframes/shadowDOM/passwords/keyactions limit use. Typing adds modelcost; output can contain scripts/navigation. No low-confidenceoverride bydesign,thresholds tuned on fewsites; provider availability must be checked separately. Source review: Useful source-grounding and bounded-selection wrappers, but model verification remains fallible. Exact quote matching and named test receipts needed. Truncated candidates cannot establish complete retrieval; agreement does not prove truth. Separate permission controls must enforce actions; configured gateways affect data destination and costs.

## Sources

- Discord source — private provenance retained locally.
- [https://github.com/jkudish/jev-mcp](https://github.com/jkudish/jev-mcp) — access: `fetched`; review: `readme_reviewed`.
- [https://github.com/jkudish/jev-browser](https://github.com/jkudish/jev-browser) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
