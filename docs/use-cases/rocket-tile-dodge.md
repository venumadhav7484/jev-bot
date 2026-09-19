---
id: rocket-tile-dodge
title: "Rocket dodging: bounded safe-tile selection"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Rocket dodging: bounded safe-tile selection

## What

Game controller chooses tiles while rockets fall.

## How Jev fits

Recorded controller uses25tile Choice, must_move Noul and danger Score; application moves avatar on grid.

## Why and impact

Final recorded counters show104decisions,1hit/26rockets and$0.0095; earlier frames show no hits.

## Limits and reuse

Thirteen sampled frames from39.22seconds, UI-reported cost/timing. One run; no representative seeds, baseline, independent execution or perfect-evasion claim.

## Sources

- [https://x.com/atomic_chat_hq/status/2100644221279424925?s=46](https://x.com/atomic_chat_hq/status/2100644221279424925?s=46) — access: `fetched`; review: `demo_trace_reviewed`.
- [https://t.co/RbcCOIgVkj](https://t.co/RbcCOIgVkj) — access: `fetched`; review: `context_only_not_jev_evidence`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
