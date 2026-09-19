# Use-case write-up template

Template only. Exclude this file from the chatbot's factual retrieval corpus.

```yaml
id: <stable-project-slug>
title: <application name>
source_kind: community
domains: []
patterns: []
primitives: [] # choice, score, noul; use unknown when not established
evidence: [] # author-report, artifact-inspected, independently-tested
source_published_at: <date or unknown>
last_reviewed_at: <date>
implementation_version: <commit/model/version or unknown>
```

## What

Application, intended user and concrete problem, in two or three sentences.

## How

Observed workflow: input acquisition → representation sent to Jev → questions and outputs → application action. Identify external models, integrations and deterministic code. Mark unknown implementation details explicitly.

## Why Jev

Author's stated rationale, followed separately by any analysis of task fit. Do not invent comparative advantages.

## Impact

Reported outcomes and measurement conditions. Distinguish measured results from qualitative reports and expected benefits. State when no results are available.

## Reusable integration pattern

Which other ideas could use this pattern, what prerequisites they need and where it does not fit. Any illustrative questions must be labeled as proposed examples unless copied within permitted limits from an inspected implementation.

## Limits and validation

Failure modes, missing evidence, model/version dependencies and checks needed before reuse.

## Sources

| Source | Author / publisher | Published | Reviewed | What was inspected | What it supports / access gap |
|---|---|---|---|---|---|
| Discord message permalink | | | | | |
| Linked X post / repository / demo / article | | | | | |

## Updates

Dated corrections, follow-up posts and evidence changes for this project.
