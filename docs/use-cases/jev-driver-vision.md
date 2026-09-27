---
id: jev-driver-vision
title: "Jev Driver: captions in, driving actions out"
category: robotics
evidence: author-reported
reviewed_on: 2026-09-27
independently_reproduced: false
---

# Jev Driver: captions in, driving actions out

## What

A browser toy car reacts to images dropped on the road: an in-browser vision model captions each image and Jev chooses the action.

## How Jev fits

Florence-2 runs in the browser and the image never leaves the device; the caption and its zone go to Jev through Cloudflare Workers AI, which chooses among continue, slow down, stop, wait and similar actions plus a category and speed limit. There is no rule table on top.

## Why and impact

The author reports about 330 ms median per decision and about 25,000 decisions per dollar, and shows the probabilities including wrong calls.

## Limits and reuse

A toy. Jev never sees the image, only a caption, so caption errors become driving errors. Letting the model drive with no rule layer is the opposite of what a safety-relevant system should do.

## Sources

- [Jev Driver](https://drive.mrza.ch/) — access: `fetched`; review: `not_reviewed`.
- [GitHub - reinhard-z/vision-jev: Can Jev drive a car? This demo puts...](https://github.com/reinhard-z/vision-jev) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
