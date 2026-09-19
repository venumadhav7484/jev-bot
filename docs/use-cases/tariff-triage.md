---
id: tariff-triage
title: "Tariff triage experiment"
category: domain-review
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Tariff triage experiment

## What

Signal tests Jev 1.13 and Claude Sonnet 5 on High/Medium/Low purchasing priority for 33 tariff-notice summaries.

## How Jev fits

Both receive the same policy and criteria; expected labels stay outside requests. Calls are sequential with provider order alternating, and Claude thinking is disabled.

## Why and impact

The author reports Jev matched 33/33 labels, roughly 172 ms median response, and 0.36 cents estimated token cost for the set.

## Limits and reuse

This is a known development set tuned with Jev; Claude did not receive equivalent tuning. Six High-priority examples cannot establish recall, estimated costs are not invoices, and production is unchanged. Shortening the policy missed a High-priority item. Confidence is not independent verification.

## Sources

- Discord source — private provenance retained locally.
- [https://www.linkedin.com/pulse/testing-ai-tariff-triage-cost-speed-accuracy-matthew-hartman-gqe3c/](https://www.linkedin.com/pulse/testing-ai-tariff-triage-cost-speed-accuracy-matthew-hartman-gqe3c/) — access: `fetched`; review: `source_text_reviewed`.
- [media.licdn.com](https://media.licdn.com/dms/image/v2/D5612AQFnBBDxMgwizg/article-cover_image-shrink_720_1280/B56aC3DhijH0AQ-/0/1789777553384?e=2147483647&v=beta&t=fwWSrZAwUKNSBG9Eeg891nbUWVlXIb3iK5EK-8P6EaI) — access: `access_failed`; review: `inaccessible_content_pending`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
