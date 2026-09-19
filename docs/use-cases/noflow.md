---
id: noflow
title: "NoFlow: registered UI action routing"
category: interfaces
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# NoFlow: registered UI action routing

## What

Make an interface respond to natural-language intent.

## How Jev fits

Registered UI actions and current state form Jev's choice set. Thresholds, fallback behavior and confirmation remain in the runtime.

## Why and impact

Reuses existing application capabilities instead of generating arbitrary execution code.

## Limits and reuse

The demo does not make model confidence an authorization boundary; actions still need deterministic constraints.

## Sources

- Discord source — private provenance retained locally.
- [https://noflow.casungo.workers.dev/](https://noflow.casungo.workers.dev/) — access: `fetched`; review: `metadata_only`.
- [https://github.com/casungo/noflow-runtime](https://github.com/casungo/noflow-runtime) — access: `fetched`; review: `not_reviewed`.
- [https://www.npmjs.com/package/noflow-runtime](https://www.npmjs.com/package/noflow-runtime) — access: `fetch_failed`; review: `not_reviewed`.
- [NoFlow | Buttons with opinions](https://noflow.casungo.workers.dev/?) — access: `fetched`; review: `metadata_only`.
- [https://x.com/casungo/status/2101037798614499387](https://x.com/casungo/status/2101037798614499387) — access: `fetched`; review: `post_text_reviewed_media_pending`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
