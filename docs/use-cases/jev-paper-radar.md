---
id: jev-paper-radar
title: "Paper Radar: filter research feeds and label your misses"
category: filtering
evidence: author-reported
reviewed_on: 2026-09-27
independently_reproduced: false
---

# Paper Radar: filter research feeds and label your misses

## What

A daily paper feed uses Jev to judge title/abstract evidence against user interests and publish selected records.

## How Jev fits

Each interest gets a Noul and contribution type gets a Choice; code owns thresholds, feed intake, dates and publishing. Optional prose comes from a separate writer. User labels feed a calibration command.

## Why and impact

The author reports 501 papers processed in 33 seconds for $0.0196. A separate 299-paper observation found more high-probability hits for concrete interests than for broad comparative claims, suggesting question wording should be tested. The author’s later post reports that on four Cochrane reviews held out from development, the screener kept 96.9% of included studies across 19,447 records while removing 78% of the reading, for $0.60; 5 of 12 pre-registered predictions were wrong and all were published.

## Limits and reuse

Hit counts alone cannot establish precision or recall. The current README includes newer screening claims beyond the original post; those datasets were not independently audited here. Offline demo output uses a heuristic rather than live Jev. Missing abstract evidence or broad interests can hide relevant papers. The same post notes that combining Nouls matters: interests combine with max (one more interest is one more chance to match) but screening criteria combine as a conjunction (one more criterion is one more chance to veto); splitting a compound criterion cut one review’s saved workload from 10.0% to 0.1%. A criterion that looked wrong was the author’s wording, not the model: Jev matched NLM indexing on 8 of 8 checked studies. Abstracts only, and thresholds were fitted on evaluation data.

## Sources

- [GitHub - Eliot5566/JEV-Paper-Radar: Let Jev read every new arXiv pa...](https://github.com/Eliot5566/JEV-Paper-Radar) — access: `fetched`; review: `sections_reviewed`.
- [https://eliot5566.github.io/JEV-Paper-Radar/public/](https://eliot5566.github.io/JEV-Paper-Radar/public/) — access: `fetched`; review: `not_reviewed`.
- [Related public project or article](https://eliot5566.github.io/JEV-Paper-Radar/public) — discovered via Discord source (private provenance retained locally); access: `fetched`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
