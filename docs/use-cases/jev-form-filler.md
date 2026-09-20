---
id: jev-form-filler
title: "Form filling from constrained profile candidates"
category: interfaces
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Form filling from constrained profile candidates

## What

Match stored profile values to form fields without generating new personal data.

## How Jev fits

The extension builds candidate strings, asks Choice per text field and Noul for checkboxes, validates outcomes, then fills only after user selection. A none option permits abstention.

## Why and impact

A concrete prepare-candidates, judge, validate, act pattern for browser assistance.

## Limits and reuse

Educational demo, not production-ready. Its README warns an inlined API key can be recovered from the build. Candidate/profile data leaves the device, validation thresholds are unproven, and no live browser-fill evaluation was performed here.

## Sources

- [github.com](https://github.com/akarsh-k/jev-form-filler-extension) — access: `fetched`; review: `sections_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
