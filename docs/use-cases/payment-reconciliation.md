---
id: payment-reconciliation
title: "Payments: messy-name and bundled-invoice reconciliation"
category: domain-review
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Payments: messy-name and bundled-invoice reconciliation

## What

Financial-services experiment reconciles payments with messy names and bundled invoices.

## How Jev fits

Jev selects candidate ledger records and judges customer identity and ambiguity; host code checks exact amounts, currencies and documented fees. Ambiguous references remain unresolved and request remittance details.

## Why and impact

Eight synthetic receipts in the recording: displayed 1.29 seconds, 11,360 input tokens and $0.00048. A documented $25 fee distinguishes the correct $50,000 invoice from a competing $49,975 invoice; equal amounts alone do not force a match.

## Limits and reuse

Recorded synthetic examples, not a labeled evaluation or production audit. No measured loss/error rate. Proposed allocations require operator review; model approval is not payment authorization. Full request payloads and all collapsed judgments were not inspected.

## Sources

- [https://x.com/Anot/status/2100761008352493918?s=20](https://x.com/Anot/status/2100761008352493918?s=20) — access: `public_media_extracted`; review: `demo_trace_reviewed`.
- [Author reply demonstration video](https://x.com/Anot/status/2100761265517781273) — discovered via [external source](https://x.com/Anot/status/2100761008352493918); access: `public_media_extracted`; review: `demo_trace_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
