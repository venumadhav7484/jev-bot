---
id: pi-warden
title: "Pi Warden: steer coding-agent behavior"
category: quality
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Pi Warden: steer coding-agent behavior

## What

Flag risky, off-task or unsupported agent actions.

## How Jev fits

Jev judges tool calls, tool outputs and replies for irreversible actions, injection, loops and unverified completion claims. Author clarification: separate Noul checks target stubs, restating comments, dead/duplicate code, hedging, wordiness and jargon; steering names the symptom and fix. A 22-case tuning set is mentioned.

## Why and impact

The author reports roughly 250 ms judgments and ongoing personal use.

## Limits and reuse

Steering is not a security boundary. Retain hard permissions and independent completion checks; the author labels it early-stage. README reports 150 paired agent runs with six rule violations in control versus zero with Warden; this remains a project-maintained experiment. Offline pattern guards and steer/confirm/advise modes differ from probabilistic checks. Source review: Rule compliance improved on small authored traps; general code quality and destructive-action prevention not established. Most guards advise rather than block. Repeat stability is distinct from correctness; retrospective hold labels use model inference.

## Sources

- Discord source — private provenance retained locally.
- [https://pi.dev/packages/pi-warden](https://pi.dev/packages/pi-warden) — access: `fetched`; review: `readme_reviewed`.
- [https://github.com/DevMortimer/pi-warden](https://github.com/DevMortimer/pi-warden) — access: `fetched`; review: `source_text_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
