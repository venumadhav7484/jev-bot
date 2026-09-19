---
id: security-probe-notifier
title: "Security screening: injection datasets and synthetic probes"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Security screening: injection datasets and synthetic probes

## What

Community authors report prompt-injection screening and Jev connected to an infrastructure-alert notifier.

## How Jev fits

One author tests unspecified injection datasets; another generates attacks from an agent box and routes notifier decisions through Jev. Larger-model escalation is proposed.

## Why and impact

Qualitative good results and catching every tested probe are author reports.

## Limits and reuse

Unspecified corpus size, attack diversity, benign examples and ground truth prevent estimating detection or false-positive rates. Not sufficient evidence to trust autonomous security enforcement. Same tester later reports 1.2% false positives out of 16,000 examples, then 1.2% missed on a 600,000-row set. These denominators and metrics differ and have not been reconciled; do not combine them into one benchmark.

## Sources


Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
