---
id: pixel-art
title: "Jev Pixel Art: numeric image construction"
category: experiments
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Jev Pixel Art: numeric image construction

## What

Draw an image through per-pixel decisions.

## How Jev fits

The author requests pixel RGBA values from a description, coordinates and optional previous-composition context; rendering happens in code.

## Why and impact

A deliberately unusual test of typed outputs and batching.

## Limits and reuse

Jev does not receive or directly generate an image modality here. Coherence remains experimental; later batches need context. Author reports numeric sketch feedback mis-mapped rows and scrambled image. Initial state used only description, coordinates, channel definitions and a composition sentence; independent questions do not implicitly share previously selected pixels. Source review: Independent pixel judgments lack joint consistency; sharpening changes distribution interpretation. Key is stored in browser localStorage and forwarded through proxy despite headline wording that it stays in browser. This is bounded numeric reconstruction, not native image generation.

## Sources

- Discord source — private provenance retained locally.
- [https://github.com/rivianpratama/JevPixelArt](https://github.com/rivianpratama/JevPixelArt) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
