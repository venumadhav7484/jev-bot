# Jev-bot

A work-in-progress knowledge base and research toolkit for a chatbot that answers:

> Describe your use case or idea. How could Jev help, what else would you need, and what are the limits?

The intended bot combines documented Jev capabilities with community implementations, failures, tools and evaluation evidence. It should explain Jev's specific role, distinguish demonstrated use from proposals, and cite supporting sources instead of inventing capabilities.

**Status: research paused.** This repository preserves the current work. The scheduled X review is also paused. The chatbot interface and end-to-end answer evaluation are not implemented.

## Start here

- [Jev capability reference](docs/jev-knowledge-reference.md): primitives, integration patterns, APIs, limits and official references.
- [262 use-case write-ups](docs/jev-usecases.md): what, how, why, reported impact, limitations and public artifact links.
- [Community findings](docs/community-evidence-findings.md): strengths, weaknesses, contradictory evidence and implementation lessons.
- [Integration patterns](docs/integration-patterns.md) and [tools and proposed integrations](docs/pending-and-ecosystem.md).
- [Bot answer guide](docs/jev-bot-answer-guide.md), including the proposed su-lekha example.
- [Completion status](docs/completion-status.md), [aggregate metrics](docs/metrics.json) and [local Jev experiment](docs/local-triage-experiment.md).

## Current state

Audit date: **19 September 2026**. These figures describe the captured snapshot, not a guarantee of complete or current source coverage.

| Layer | Current state |
|---|---|
| Discord source | 3,358 unique captured message IDs processed locally |
| Jev-assisted triage | 3,358 / 3,358 messages processed; 420 successful requests for the final prompt version |
| Curated cases | 262 write-ups; 246 eligible for default case retrieval; 16 held back |
| Editorial accounting | 350 messages cited in cases, 14 other dispositions, 2,994 still awaiting final disposition |
| External sources | 809 URLs registered; 783 marked not reviewed |
| X backlog | 182 distinct posts tracked; follow-up paused |
| Media | 370 attachment-bearing messages; 118 have sparse body text |
| Retrieval | Local SQLite full-text search for source messages, cases and reference sections |
| Product | Research tools exist; chatbot conversation flow and answer evaluation remain unfinished |

**Processing is not verification.** Model categories can be wrong. A small development sample matched 13/13 contribution categories and 11/13 Jev-use relationships; it is not a representative accuracy benchmark. Community performance claims remain attributed reports unless explicitly independently reproduced.

## How Jev is used here

The pipeline uses Choice to categorize contributions and identify the claimed relationship to Jev. Independent Noul questions flag implementation details, negative evidence, measurements, tooling and missing context. Host code handles normalization, batching, validation, caching and review priority.

Every prediction retains provenance and uncertainty. No model label automatically approves or discards evidence. Media inspection, external-source investigation and final synthesis remain separate tasks. See [TypeSafe primitives](https://docs.typesafe.ai/primitives) and the [pipeline notes](docs/research-pipeline.md).

## Repository layout

```text
docs/                       Sanitized public knowledge and case write-ups
scripts/jev_triage.py        Resumable Jev API classification
scripts/evidence.py          Local SQLite evidence indexing and search
scripts/audit_triage.py      Development-sample audit
scripts/build-*.py           Private-input provenance and retrieval builders
scripts/render-cases.py      Curated case renderer
scripts/export_public.py     Allowlisted public documentation export
tests/                      Normalization, response and cache checks
.env.example                Empty credential template
```

## Setup and checks

Python 3.10+ and the standard library are sufficient. The API runner currently uses Unix file locking (macOS/Linux).

```sh
git clone https://github.com/venumadhav7484/jev-bot.git
cd jev-bot
python3 -m unittest discover -s tests -v
```

An archive-dependent test is skipped when private source inputs are absent. Other tests run without credentials or network access.

For an explicitly resumed research run, create `.env.local` using `.env.example` as a template and set `jev_api_key` locally. Never commit that file. Research inputs are intentionally absent from the public repository: the scripts require an authorized local `resource-pool/` and `research/` workspace, including snapshots, a collection checkpoint, source registers and curated editorial data. They do not log into Discord or fetch messages automatically.

With those private inputs restored, the workflow is:

```sh
python3 scripts/jev_triage.py prepare
python3 scripts/jev_triage.py run --max-requests 4 --max-input-tokens 60000
python3 scripts/jev_triage.py report
python3 scripts/evidence.py build
python3 scripts/evidence.py search "routing email" --limit 8
```

`run` sends source text to TypeSafe and may incur API charges. Successful batches are cached and resumable. The input-token stop is soft because an in-flight batch can finish after the threshold. Search results retain evidence status; callers must respect `default_retrieval` when building recommendations.

## Public and private boundaries

Public docs use **Discord source** as the provenance label. Private message links, source identifiers, raw captures, quoted-message archives, model request/response caches, local databases, credentials and machine-specific resume state are excluded from Git. Public repository, article, demo and official-documentation links remain available in the case write-ups. Exact private provenance is retained locally for future review.

`.gitignore` provides protection, but public updates also require explicit staging and inspection. `export_public.py` exports an allowlist; it is not a general-purpose secret scanner. Do not publish raw research directories or run private builders and blindly stage every resulting file.

## Paused work

1. Give 2,994 messages a final curated disposition: attach to cases/findings, merge duplicates or exclude with reasons.
2. Investigate 783 unreviewed external URLs, including blocked X evidence.
3. Account for media across 370 attachment-bearing messages.
4. Finish cross-case synthesis and test bot recommendations against positive examples, counterexamples, source accuracy and uncertainty.

No completion claim is made for these tasks. Resume only when requested. No S3 storage or deployed chatbot is part of this snapshot.
