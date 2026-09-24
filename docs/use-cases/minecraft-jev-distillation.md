---
id: minecraft-jev-distillation
title: "Minecraft combat: use Jev labels to train a local classifier"
category: games
evidence: author-reported
reviewed_on: 2026-09-24
independently_reproduced: false
---

# Minecraft combat: use Jev labels to train a local classifier

## What

An author reports training local LightGBM classifiers to imitate Jev combat decisions in Minecraft.

## How Jev fits

Jev supplies decisions for a labelled dataset; the local model controls the real-time combat loop. The report offers per-tick inputs and comparison views.

## Why and impact

The author reports approximately 300 ms remote calls from Australia versus approximately 1 ms local decisions. This moves network latency outside the live loop.

## Limits and reuse

This trains a separate model, not Jev itself. Agreement with the teacher is not proof of good combat decisions, and teacher mistakes can transfer. Saved page text inspected; recording, training data, performance distribution and generalization not independently verified.

## Sources

- [https://aibengineering.github.io/minecraft-jev-distillation/](https://aibengineering.github.io/minecraft-jev-distillation/) — access: `fetched`; review: `post_text_reviewed_media_pending`.
- [https://x.com/aibengineering/status/2102535795953619127?s=20](https://x.com/aibengineering/status/2102535795953619127?s=20) — access: `fetched`; review: `not_reviewed`.
- [Related public project or article](https://aibengineering.github.io/minecraft-jev-distillation) — discovered via Discord source (private provenance retained locally); access: `fetched`; review: `post_text_reviewed_media_pending`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
