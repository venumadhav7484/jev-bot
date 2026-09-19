---
id: computer-use-aaron
title: "Computer use: early cross-platform speed claim"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Computer use: early cross-platform speed claim

## What

Developer reports a Jev computer-use prototype.

## How Jev fits

OCR text and bounding rectangles become a selectable list; Jev chooses an item and host clicks it. Small generative models supply text or missing actions; the example uses Haiku.

## Why and impact

One TechCrunch ticket-search example reports $0.003 and about 1.5 seconds versus Opus 5 at roughly $0.50 and 5.5 seconds. These figures imply about 3.7x timing improvement, not the post headline’s 20x.

## Limits and reuse

Handwavy single-task comparison; no controlled suite or measured cross-platform compatibility. Author notes poor icon handling; repository is macOS-focused. OCR portability is a design argument, not evidence of successful runs on every OS. Source review: Jev acts on extracted text and structured controls, not screenshots. Writing and final screenshot interpretation use separate generative models/costs. One-decision comparison does not establish equal task success or general speedup; perception engineering and stopping rules matter.

## Sources

- Discord source — private provenance retained locally.
- [https://x.com/awlevin/status/2100262612428894676](https://x.com/awlevin/status/2100262612428894676) — access: `fetched`; review: `post_text_reviewed_media_pending`.
- [https://github.com/browser-use/macOS-use](https://github.com/browser-use/macOS-use) — access: `fetched`; review: `ecosystem_context_reviewed`.
- [https://github.com/awlevin/typesafe-computer-use](https://github.com/awlevin/typesafe-computer-use) — access: `fetched`; review: `readme_reviewed`.
- [https://x.com/awlevin/status/2100262612428894676?s=46](https://x.com/awlevin/status/2100262612428894676?s=46) — access: `fetched`; review: `post_text_reviewed_media_pending`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
