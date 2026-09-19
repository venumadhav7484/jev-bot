---
id: cerebras-typed-benchmark
title: "Typed-output gateway: Qwen on Cerebras versus Jev"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Typed-output gateway: Qwen on Cerebras versus Jev

## What

Open benchmark builds a TypeSafe-like gateway backed by Qwen 3.8 27B on Cerebras.

## How Jev fits

Compares structured-output workflows; repo iammrduncan/typesafe-ai-benchmark.

## Why and impact

Author claims similar quality/speed but much lower Jev cost.

## Limits and reuse

Prompt, task quality, caching, concurrency and billing assumptions require inspection; imitation API is not same architecture. Source review: Valid output is distinct from correct judgment. Jev was cheaper/faster in this run but weaker on approvals/home; stateful trajectories diverged. Needle direct-runtime measurements are not controlled cloud-speed comparison. Canceled-call unknown usage excluded; repeated synthetic fixtures and lack calibration limit generalization. Published Jev$0.011919 estimate uses historical rate; do not reuse as current pricing.

## Sources

- Discord source — private provenance retained locally.
- [https://github.com/iammrduncan/typesafe-ai-benchmark](https://github.com/iammrduncan/typesafe-ai-benchmark) — access: `fetched`; review: `readme_reviewed`.
- [https://x.com/iamMrDuncan/status/2100467548298899918](https://x.com/iamMrDuncan/status/2100467548298899918) — access: `fetched`; review: `post_text_reviewed_media_pending`.
- [https://t.co/H5rUhiN7EY](https://t.co/H5rUhiN7EY) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
