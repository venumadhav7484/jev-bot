---
id: noflow
title: "NoFlow: registered UI action routing"
category: interfaces
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# NoFlow: registered UI action routing

## What

Make an interface respond to natural-language intent.

## How Jev fits

Registered UI actions and current state form Jev's choice set. Thresholds, fallback behavior and confirmation remain in the runtime.

## Why and impact

Recorded same-label interaction changes from trial to checkout when trial-used state changes; demonstrates state-aware selection among registered surfaces.

## Limits and reuse

Recorded examples display295ms and438ms, not a latency distribution. UI surface selection is not payment execution or authorization. Model confidence and warning controls are not sufficient security boundaries; deterministic permissions and confirmation remain necessary.

## Sources

- Discord source — private provenance retained locally.
- [https://noflow.casungo.workers.dev/](https://noflow.casungo.workers.dev/) — access: `browser_readable`; review: `landing_page_reviewed`.
- [https://github.com/casungo/noflow-runtime](https://github.com/casungo/noflow-runtime) — access: `fetched`; review: `readme_reviewed`.
- [https://www.npmjs.com/package/noflow-runtime](https://www.npmjs.com/package/noflow-runtime) — access: `browser_readable`; review: `readme_reviewed`.
- [NoFlow | Buttons with opinions](https://noflow.casungo.workers.dev/?) — access: `browser_readable`; review: `landing_page_reviewed`.
- [https://x.com/casungo/status/2101037798614499387](https://x.com/casungo/status/2101037798614499387) — access: `public_media_extracted`; review: `demo_trace_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
