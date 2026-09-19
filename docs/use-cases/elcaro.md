---
id: elcaro
title: "Elcaro: second opinion on prompt injection"
category: security
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Elcaro: second opinion on prompt injection

## What

Elcaro describes indirect prompt-injection detection for autonomous agents.

## How Jev fits

The optional Jev comparison never changes the verdict; the rules retain veto power.

## Why and impact

Jev can be evaluated alongside the existing decision path without authorizing actions. This is an architectural inference from the comparison-only integration.

## Limits and reuse

The reported notice-placement compliance experiment cannot be treated as Jev detection accuracy: Jev is comparison-only. Media review: Reviewed28 sampled frames plus transcript of quoted Elcaro launch video: local detector reports30/150 bypasses before hardening and0/150 afterwards, signed verdict and sandbox-email receipts. This is earlier detector marketing/demo, not a Jev detection benchmark. Later Jev integration is optional second opinion; rules retain veto. Held-out attack quality and false-positive rate not established.

## Sources

- [https://x.com/UNgethe/status/2100652324418945273?s=20](https://x.com/UNgethe/status/2100652324418945273?s=20) — access: `fetched`; review: `demo_trace_reviewed`.
- [https://t.co/j9hsV64WW6](https://t.co/j9hsV64WW6) — access: `fetched`; review: `source_text_reviewed`.
- [Author-linked implementation artifact](https://github.com/udirobert/elcaro) — discovered via [external source](https://x.com/UNgethe/status/2100652324418945273); access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
