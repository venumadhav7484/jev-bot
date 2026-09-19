---
id: clinical-document-grounding
title: "Clinical documents: routing and stated-site grounding"
category: domain-review
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Clinical documents: routing and stated-site grounding

## What

Synexar tests document routing and an external grounding check around deterministic billing rules.

## How Jev fits

For billing, replace a broad plausibility question with Choice over anatomical sites plus not stated. Host compares the selected site with its rules-engine output and escalates unresolved cases.

## Why and impact

Author reports43/43document routes versus41/43keyword baseline at127msmedian. Broad question caught0/11seeded site errors; explicit Choice caught11/11with0/27false blocks. Across594synthetic cases, errors were detected or escalated.

## Limits and reuse

Synthetic/de-identified examples, not clinical deployment validation. Detection plus escalation is not autonomous accuracy. OCR path, adopted thresholds and dataset details are absent. Same author reports task-tier routing failed its adoption gate; small engineering-harness agreement10/10was adopted. No independent reproduction.

## Sources

- Discord source — private provenance retained locally.
- [https://www.linkedin.com/posts/raghuvadapally_𝗧𝗵𝗲-𝗤𝘂𝗲𝘀𝘁𝗶𝗼𝗻-𝗦𝗵𝗮𝗽𝗲-𝗜𝘀-𝘁𝗵𝗲-activity-7506415829442424832-95UB?utm_source=social_share_send&utm_medium=member_desktop_web&rcm=ACoAAAC35IoB5xF9GSZM4IPL1dUi1CSkUPeBLSU](https://www.linkedin.com/posts/raghuvadapally_%F0%9D%97%A7%F0%9D%97%B5%F0%9D%97%B2-%F0%9D%97%A4%F0%9D%98%82%F0%9D%97%B2%F0%9D%98%80%F0%9D%98%81%F0%9D%97%B6%F0%9D%97%BC%F0%9D%97%BB-%F0%9D%97%A6%F0%9D%97%B5%F0%9D%97%AE%F0%9D%97%BD%F0%9D%97%B2-%F0%9D%97%9C%F0%9D%98%80-%F0%9D%98%81%F0%9D%97%B5%F0%9D%97%B2-activity-7506415829442424832-95UB?utm_source=social_share_send&utm_medium=member_desktop_web&rcm=ACoAAAC35IoB5xF9GSZM4IPL1dUi1CSkUPeBLSU) — access: `fetched`; review: `visible_post_text_reviewed`.
- [static.licdn.com](https://static.licdn.com/aero-v1/sc/h/c45fy346jw096z9pbphyyhdz7) — access: `asset_no_text`; review: `excluded_asset`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
