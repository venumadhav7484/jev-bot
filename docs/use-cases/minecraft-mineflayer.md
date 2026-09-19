---
id: minecraft-mineflayer
title: "Minecraft: structured-world decisions through Mineflayer"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Minecraft: structured-world decisions through Mineflayer

## What

A Minecraft bot navigates, collects resources and avoids threats through a Mineflayer harness.

## How Jev fits

Harness exposes world facts and bounded functions to Jev. Supplied log includes health, hunger, action, goal, threats, cover, time and food; periodic decisions select actions, targets, danger and whether to interrupt current behavior. Author also explores a longer-term decision instance that changes the immediate controller’s goal, for example exploring until food is found.

## Why and impact

Shows event/periodic decision integration without image input. Video author describes exploration and escape from zombies; no success rate supplied.

## Limits and reuse

Author reports reward hacking toward wood and clarifies published shelter log came from a bugged session that would not stop hiding. Log prose is harness output, not evidence of model chain of thought. Validate executor, progress detection and recovery independently. Additional screenshot shows HUNT selected at1.00confidence even at20/20hunger, with danger0/4 and interruptNo.19. One action trace and cow-hit frame establish a demonstrated action, not robust survival.

## Sources

- Discord source — private provenance retained locally.
- [https://youtu.be/3G14OU00crI?si=ucI7ksLDTPisf1pD](https://youtu.be/3G14OU00crI?si=ucI7ksLDTPisf1pD) — access: `fetched`; review: `metadata_only`.
- [YouTube](https://www.youtube.com/) — access: `fetched`; review: `context_only_not_jev_evidence`.
- [Hyperion](https://www.youtube.com/channel/UCD19mqbVLsb11Di1qdvhMZQ) — access: `fetched`; review: `context_only_not_jev_evidence`.
- [Jevbot Flees the Zombie Horde typesafe.ai Jev Model](https://www.youtube.com/watch?v=3G14OU00crI) — access: `fetched`; review: `metadata_only`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
