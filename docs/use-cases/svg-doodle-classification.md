---
id: svg-doodle-classification
title: "SVG doodles: representation matters"
category: quality
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# SVG doodles: representation matters

## What

A published experiment classifies 400 sketches encoded as text SVG across ten categories.

## How Jev fits

Coordinates are normalized and simplified before Jev chooses among supplied object labels. The article compares the same drawings as SVG and image encodings.

## Why and impact

Author reports about 35% for Jev on SVG versus 10% chance, while base64 image strings were near chance. This illustrates structured text representation, not native vision.

## Limits and reuse

Sonnet on SVG performed better. Drawings and classes were selected, category behavior was uneven, and there was one attempt per drawing. Results were not independently reproduced and do not establish general visual reasoning.

## Sources

- [mikulskibartosz.name](https://mikulskibartosz.name/typesafe-jev-guess-what-i-drew) — access: `fetched`; review: `sections_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
