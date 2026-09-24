---
id: jevkit
title: "jevkit: measured review bands around a voice assistant"
category: voice
evidence: author-reported
reviewed_on: 2026-09-24
independently_reproduced: false
---

# jevkit: measured review bands around a voice assistant

## What

A Python decision layer prepares context, asks typed questions and routes answers into act, confirm or escalate bands.

## How Jev fits

A German voice assistant uses Jev for addressed-speech detection, tool routing and memory checks. Code handles candidate extraction, numeric/date preprocessing, validation, fallback and outcome logs. A guard was rewritten to detect manipulation instead of merely detecting instructions addressed to an assistant.

## Why and impact

Author reports the revised guard handled all 14 tested legitimate commands without errors and used 92 labelled cases to revise a decision band. The useful lesson is to measure the actual application path: mocked unit tests had missed false positives.

## Limits and reuse

Tiny local labelled sets do not establish broad safety or calibration. The post and current README give different initial command counts; do not combine them into one precise before/after rate. Minimum confidence across judgments is a heuristic, not a calibrated joint-success probability. A guard judgment cannot enforce permissions or guarantee injection resistance.

## Sources

- [GitHub - tegersdorfer-collab/jevkit: Decision kernel for TypeSafe J...](https://github.com/tegersdorfer-collab/jevkit) — access: `fetched`; review: `sections_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
