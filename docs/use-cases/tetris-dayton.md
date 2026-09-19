---
id: tetris-dayton
title: "Tetris: confidence-sensitive hard-drop failure"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Tetris: confidence-sensitive hard-drop failure

## What

A Tetris controller demo exposes model confidence during play.

## How Jev fits

Author reports that near 40/60 confidence the controller hard-drops pieces down the middle; exact primitive and action encoding remain unspecified.

## Why and impact

Low-latency execution exposes mistakes quickly and offers a concrete failure to test.

## Limits and reuse

Video unreviewed; no score, line-clear rate or comparative strategy benchmark. Confidence alone does not supply correct placement or robust fallback.

## Sources


Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
