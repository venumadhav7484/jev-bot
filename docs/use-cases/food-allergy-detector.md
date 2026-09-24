---
id: food-allergy-detector
title: "Recipe allergen prototype: unknown must not mean absent"
category: domain-review
evidence: author-reported
reviewed_on: 2026-09-24
independently_reproduced: false
---

# Recipe allergen prototype: unknown must not mean absent

## What

A recipe-screening prototype uses typed questions to flag possible allergens and meat ingredients.

## How Jev fits

The README separates detection from a later ingredient-attribution request and describes a visibly labelled keyword fallback when the provider fails.

## Why and impact

Useful as a counterexample to overclaiming: missing vocabulary or unmatched input should remain unchecked rather than become an assurance of absence.

## Limits and reuse

Not a validated food-safety tool. The README itself notes unvalidated vocabulary, geographic coverage bias and weaker keyword fallback; recipe text cannot establish ingredients, contamination or label accuracy. No clinical or allergen-detection accuracy evidence. Held from default recommendations.

## Sources

- [https://github.com/SysCoder/FoodAllergyDetector](https://github.com/SysCoder/FoodAllergyDetector) — access: `fetched`; review: `sections_reviewed`.
- [https://faas-sfo3-7872a1dd.doserverless.co/api/v1/web/fn-a6ef956d-73a5-4702-b7c9-d9286272d233/app/http](https://faas-sfo3-7872a1dd.doserverless.co/api/v1/web/fn-a6ef956d-73a5-4702-b7c9-d9286272d233/app/http) — access: `fetched`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
