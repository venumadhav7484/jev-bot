---
id: ai-control-monitor
title: "Non-generative trusted-monitor experiment"
category: security
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Non-generative trusted-monitor experiment

## What

Score agent behavior for suspicious actions.

## How Jev fits

The author links an AI-control experiment using Jev as a monitor.

## Why and impact

The post reports AUROC near 0.97 on its evaluation.

## Limits and reuse

Adaptive attacks reportedly degrade performance. AUROC is not an operational false-negative guarantee and does not establish secure authorization. The pilot lacks an actual LLM-monitor control. A low false-positive rate on a static sample does not guarantee detection against adaptive variant selection; raw scores were underconfident and weak on semantic variants. Source review: Strong toy-set discrimination is not production security or prompt-injection immunity.2%false-positive rate is not2%ofalltraffic audit budget. Best-of-N selection and semantic edits weaken detection; raw scores cannot estimate residual risk. Cross-paper CoT comparison unmeasured, and article has internal numeric/wording errors. Reviewed plot labels audit budget as share of honest code flagged: 1/2/5% thresholds display 88/90/93% detection against LLM-written honest code and 85/88/92% against human-written honest code. These are static experiment figures, not a production audit workload guarantee.

## Sources

- Discord source — private provenance retained locally.
- [https://www.lesswrong.com/posts/d7pQicW8EhpPBDRqz/a-non-generative-model-as-a-trusted-monitor-for-ai-control](https://www.lesswrong.com/posts/d7pQicW8EhpPBDRqz/a-non-generative-model-as-a-trusted-monitor-for-ai-control) — access: `fetched`; review: `article_reviewed`.
- [https://x.com/exploding_grad/status/2100983340602179953](https://x.com/exploding_grad/status/2100983340602179953) — access: `fetched`; review: `visible_post_text_reviewed`.
- [res.cloudinary.com](https://res.cloudinary.com/lesswrong-2-0/image/upload/f_auto,q_auto/v1/mirroredImages/d7pQicW8EhpPBDRqz/npi4f5j84gflixawyywv) — access: `public_image_extracted`; review: `image_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
