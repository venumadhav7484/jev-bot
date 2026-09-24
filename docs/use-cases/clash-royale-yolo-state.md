---
id: clash-royale-yolo-state
title: "Clash Royale: YOLO/CV supplies state, Jev chooses moves"
category: games
evidence: author-reported
reviewed_on: 2026-09-24
independently_reproduced: false
---

# Clash Royale: YOLO/CV supplies state, Jev chooses moves

## What

A separate community game controller reports an early winning streak and later 98% wins near 500 trophies.

## How Jev fits

The author clarifies that images go through YOLOv9 troop detection and a computer-vision pipeline. Jev receives the resulting JSON state, not screenshots.

## Why and impact

Concrete perception/judgment separation: maintain image extraction outside the text-only decision step.

## Limits and reuse

Initial streak and later percentage describe different reports, not a fixed benchmark. Match count, opponent distribution, complete recordings and independent replay remain unresolved. Do not merge this implementation with another author’s earlier near-win demo or infer general player ranking.

## Sources

- [https://x.com/atp_se7en/status/2101871442417905792?s=46](https://x.com/atp_se7en/status/2101871442417905792?s=46) — access: `access_failed`; review: `inaccessible_content_pending`.
- [https://x.com/atp_se7en/status/2102107698557026683?s=20](https://x.com/atp_se7en/status/2102107698557026683?s=20) — access: `fetched`; review: `not_reviewed`.
- [Related public project or article](https://x.com/atp_se7en/status/2101871442417905792) — discovered via Discord source (private provenance retained locally); access: `access_failed`; review: `inaccessible_content_pending`.
- [Related public project or article](https://x.com/atp_se7en/status/2102107698557026683) — discovered via Discord source (private provenance retained locally); access: `fetched`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
