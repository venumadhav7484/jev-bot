---
id: jev-svg-recognition
title: "SVG recognition: 100 yes/no questions as features"
category: experiments
evidence: author-reported
reviewed_on: 2026-09-27
independently_reproduced: false
---

# SVG recognition: 100 yes/no questions as features

## What

A research task asks Jev many broad questions about an SVG and trains a classifier on the answers.

## How Jev fits

Each SVG goes into context with 100 yes/no questions (is it red, is it an animal, is it a physical object); a simple classifier learns from the probabilities. Training and test SVGs come from different drawing models.

## Why and impact

On 23 object classes from a public SVG benchmark, one zero-shot Choice scored 39.7%, while question features trained on other models’ drawings did better than code-feature classifiers and in one case came close to CLIP on rendered pixels.

## Limits and reuse

The author calls it not a meaningful project on its own; small dataset and selected classes. Jev still cannot read images; this works only because SVG is text.

## Sources

- [https://jev-svg.lexic.cloud/](https://jev-svg.lexic.cloud/) — access: `fetched`; review: `not_reviewed`.
- [GitHub - Fox-Islam/jev-svg-recognition: Research task on weighting ...](https://github.com/Fox-Islam/jev-svg-recognition) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
