---
id: swamp-triage
title: "Swamp: alert screening before escalation"
category: operations
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Swamp: alert screening before escalation

## What

Reduce expensive analysis of low-value alerts.

## How Jev fits

The author describes Jev screening signals, Swamp routing them and Claude handling work worth escalation.

## Why and impact

Reports 91% lower cost and 14.8% faster alert triage; production use is self-reported.

## Limits and reuse

The linked article was not accessible through the initial web fetch. Accuracy was described informally, so false-negative impact remains unknown. Author reports no missed real alert among 100 signals, without positive-class count or labeling protocol. This does not establish production recall. Article reports91%cost and14.8%latency reduction but gives no visible sample count, threshold or missed-incident rate. Operational failure paging does not catch every semantic false negative.

## Sources

- [https://blog.watson-labs.co.uk/typesafe-ai-alert-fatigue/](https://blog.watson-labs.co.uk/typesafe-ai-alert-fatigue/) — access: `fetched`; review: `article_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
