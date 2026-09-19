---
id: coding-tool-permission
title: "Coding-agent permission judgments"
category: quality
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Coding-agent permission judgments

## What

Terminal demo uses Jev to advise a coding-agent tool permission decision.

## How Jev fits

Visible read-only shell request receives allowed=true after timeout/retry; configured allow and confidence thresholds appear in trace.

## Why and impact

Shows integration of a bounded risk judgment before tool execution.

## Limits and reuse

One low-risk command, not an adversarial permission benchmark. No inspected fail-open/fail-closed handling, authorization enforcement or full source. Model registry pricing fallback means displayed cost may be incomplete.

## Sources


Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
