---
id: qualm-screen-time
title: "Qualm: screen-time rules written as sentences"
category: consumer
evidence: author-reported
reviewed_on: 2026-09-27
independently_reproduced: false
---

# Qualm: screen-time rules written as sentences

## What

A macOS screen-time app steps in when you drift into endless short video or feeds and stays out of the way for learning or work.

## How Jev fits

On each new screen it asks what kind of page it is, whether it is for learning, work or entertainment, whether it is private, and how likely it breaks each user rule; plain code decides. Rules are sentences such as “short videos made for endless swiping”. A local Kev model is the default; hosted Jev is optional.

## Why and impact

A lecture and its Shorts sidebar on the same site get different answers, which a site blocker cannot do. The README reports about 0.2 s per check with Jev.

## Limits and reuse

Screen text leaves the Mac when the hosted model is used. No accuracy figures; mistakes interrupt the user or let a feed through.

## Sources

- [GitHub - RoderickQiu/qualm: The first screen-time app built on Kev ...](https://github.com/RoderickQiu/qualm) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
