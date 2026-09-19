---
id: pcb-routing
title: "PCB route-candidate selection"
category: engineering
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# PCB route-candidate selection

## What

An experiment asks models to choose PCB routing candidates.

## How Jev fits

Jev performs batched regional judgments; external routing and validation determine connectivity, design-rule violations and length.

## Why and impact

Author reports fast, low-token selection with comparable routing outcomes across small trials.

## Limits and reuse

Comparisons include different agent overhead and concurrency, and costs are API-equivalent estimates rather than invoices. Routing legality comes from deterministic validation, not model confidence.

## Sources

- Discord source — private provenance retained locally.
- [OpenAI pricing](https://developers.openai.com/api/docs/pricing) — access: `fetched`; review: `official_reference_reviewed`.
- [Codex billing](https://learn.chatgpt.com/docs/pricing) — access: `fetched`; review: `official_reference_reviewed`.
- [TypeSafe pricing example](https://docs.typesafe.ai/cookbooks/parallel_questions) — access: `fetched`; review: `official_documentation_reviewed`.
- [ts-docs.mintlify.app](https://ts-docs.mintlify.app/mintlify-assets/_next/image?url=%2F_mintlify%2Fapi%2Fog%3Fdivision%3DBatching%26title%3DParallel%2Bquestions%26description%3DRuns%2Ba%2B13-question%2Bregulatory%2Bbriefing%2Bover%2Bthe%2BGDPR%2BWikipedia%2Barticle%252C%2Bshowing%2Bthat%2Bbatching%2Bevery%2Bquestion%2Binto%2Bone%2BTypeSafe%2Bcall%2Bis%2B12.2x%2Bcheaper%2Band%2B10.0x%2Bf%26theme%3Df0580ae664a0195833f0555d&w=1200&q=100) — access: `public_image_extracted`; review: `image_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
