---
id: ego-decision-layer
title: "ego-decision-layer: one Jev decision per browser step"
category: browser
evidence: author-reported
reviewed_on: 2026-09-27
independently_reproduced: false
---

# ego-decision-layer: one Jev decision per browser step

## What

A pluggable decision layer for the ego lite browser replaces the per-step LLM round trip in browser automation.

## How Jev fits

Jev reads an indexed table of page elements and answers, in one request, both the operation (click, type, select, scroll, wait, done, blocked) and the target element. Code owns observation, execution, verification and exits; the executor fails closed on stale, hidden or dangerous targets. A local OpenAI-compatible backend can be swapped in; without calibrated probabilities, confidence-based escalation is skipped.

## Why and impact

The author measured decisions at a median 434 ms against 1.6–4.5 s for large-model turns, and a two-step navigation falling from 4,569 ms to 1,916 ms. Against another Jev browser harness over 100 paired rounds, results were mixed.

## Limits and reuse

Author measurements with raw data in the repository; not independently reproduced. Execution, not the decision, is now the largest part of each step.

## Sources

- [GitHub - jiangkoumo/ego-jev: Drive the ego lite browser with Jev (T...](https://github.com/jiangkoumo/ego-jev) — access: `fetched`; review: `not_reviewed`.
- [Show and tell: driving ego-browser with Jev (TypeSafe System One) -...](https://github.com/citrolabs/ego-lite/discussions/410) — access: `fetched`; review: `not_reviewed`.
- [GitHub - jiangkoumo/ego-decision-layer: Pluggable decision layer fo...](https://github.com/jiangkoumo/ego-decision-layer) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
