---
id: resume-review-silence
title: "Resume review that stays silent unless the evidence agrees"
category: domain-review
evidence: author-reported
reviewed_on: 2026-09-27
independently_reproduced: false
---

# Resume review that stays silent unless the evidence agrees

## What

A free resume reviewer points to the introduction and experience lines most worth improving, instead of writing a general critique.

## How Jev fits

Code handles page count, missing sections, duplicates, repeated openers and dates. Redacted text then goes to Jev as narrow questions about single lines (does it mostly describe a responsibility, does it give any sense of scale, can a reader tell what the person did). Code decides whether the signals agree strongly enough to show anything; each finding pairs pre-written guidance with the user's own quoted line, so the model cannot invent metrics.

## Why and impact

Uncertain or conflicting signals produce no card at all. The author removed an "unclear" state because users read it as the tool not knowing, and fixed a calibration bug by looking at where probability mass falls relative to the pass/improve boundary on an ordered scale, not at the winning level's confidence.

## Limits and reuse

Author write-up; no accuracy or user-outcome figures published. Names, contact details, locations and profile links are removed before text is sent.

## Sources

- [What’s Wrong With My Resume? Free Review](https://freeresume.site/whats-wrong-with-my-resume) — access: `fetched`; review: `landing_page_reviewed`.
- [Jev and the Problem With AI That Always Has an Answer](https://dev.to/999thelastpage/jev-and-the-problem-with-ai-that-always-has-an-answer-1k6f) — access: `fetched`; review: `article_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
