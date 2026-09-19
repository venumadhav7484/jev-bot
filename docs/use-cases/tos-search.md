---
id: tos-search
title: "Terms-of-service line search"
category: retrieval
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Terms-of-service line search

## What

Locate ownership-related clauses in AI vendor terms.

## How Jev fits

The author adapts the official semantic-find cookbook to score/select source lines and compares with DeepSeek V4 Flash.

## Why and impact

Reports 23x faster execution and one avoided false positive.

## Limits and reuse

Later correction: more than 5x token use and higher cost in that implementation. Speed does not automatically imply lower total cost.

## Sources

- Discord source — private provenance retained locally.
- [https://docs.typesafe.ai/cookbooks/semantic_find](https://docs.typesafe.ai/cookbooks/semantic_find) — access: `fetched`; review: `not_reviewed`.
- [ts-docs.mintlify.app](https://ts-docs.mintlify.app/mintlify-assets/_next/image?url=%2F_mintlify%2Fapi%2Fog%3Fdivision%3DHow-to%26title%3DLine-by-line%2Bsearch%26description%3DBuild%2Bsemantic%2Bsearch%2Bfor%2BGitHub%2527s%2BTerms%2Bof%2BService.%2BIn%2Bone%2Brequest%252C%2Bscore%2B218%2Bline%2Bids%2Bagainst%2Ba%2Bplain-language%2Bquery%2Bwith%2Ba%2BChoice%2Bquestion%252C%2Band%2Buse%2Ba%2BNoul%2Bqu%26theme%3Df0580ae664a0195833f0555d&w=1200&q=100) — access: `fetch_failed`; review: `not_reviewed`.
- [https://www.linkedin.com/pulse/sandbox-side-quest-1-jev-system-one-model-ryan-bruins-rpesc/](https://www.linkedin.com/pulse/sandbox-side-quest-1-jev-system-one-model-ryan-bruins-rpesc/) — access: `fetch_failed`; review: `not_reviewed`.
- [media.licdn.com](https://media.licdn.com/dms/image/v2/D5612AQEJ65A8ePu2Qg/article-cover_image-shrink_720_1280/B56aC1zlKNJAAU-/0/1789756593082?e=2147483647&v=beta&t=fxcxt5g-RAZpW9aSoa-yUHgNtcwjbq1APDC6eQD6BZg) — access: `fetch_failed`; review: `not_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
