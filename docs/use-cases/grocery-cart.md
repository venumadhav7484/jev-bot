---
id: grocery-cart
title: "Video-to-grocery-cart assistant"
category: consumer
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Video-to-grocery-cart assistant

## What

A personal assistant prepares ingredients for mushroom toast.

## How Jev fits

Videomemory provides visual/transcript understanding; Jev supports ingredient and store-navigation decisions. Video frontend samples about one frame per second, deduplicates, embeds with MobileCLIP, retrieves relevant frames and creates a labeled contact sheet for a separate vision model.

## Why and impact

Author reports a prepared cart in about one minute.

## Limits and reuse

Prepared cart is not a completed purchase. No native Jev vision or autonomous payment capability follows. Media review: Reviewed27 sampled frames: recipe video enters VideoMemory pipeline, ingredient probabilities drive Brave/Playwright searches and add-to-cart actions in Instacart. App reports cart ready; later cart panel shows items split across Walmart, Costco and Safeway. Login screen appears during checkout attempt; no payment/order completed. Brand, quantity, store consolidation and ingredient recall not audited.

## Sources

- Discord source — private provenance retained locally.
- [https://x.com/heykathan/status/2100680287042814326?s=20](https://x.com/heykathan/status/2100680287042814326?s=20) — access: `fetched`; review: `demo_trace_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
