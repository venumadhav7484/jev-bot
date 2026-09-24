---
id: sovereign-rag-benchmark
title: "Legal RAG comparison: corrected baselines and a registry gate"
category: limitations
evidence: author-reported
reviewed_on: 2026-09-24
independently_reproduced: false
---

# Legal RAG comparison: corrected baselines and a registry gate

## What

A community comparison tests remote Jev judgments against local routing, reranking and entailment components for a small UK-statute workload.

## How Jev fits

Jev handles bounded routing, passage comparison and support judgments. The local design combines parsers, neural models and an explicit statute registry gate. After a reader inspected the code, the author acknowledged the original router was regex and the reranker used MiniLM rather than the named DistilBERT and ColBERT models, then reported replacements.

## Why and impact

The strongest reusable lesson is to check executed baselines and isolate the model from deterministic evidence checks. The corrected article acknowledges that standalone DeBERTa also fails the fabricated-statute probe without a registry gate.

## Limits and reuse

Do not reuse original timings as measurements of the models originally named. Current README, article and follow-up give differing routing timings. Local versus gateway execution includes different overhead; the large monthly reranking cost is a scale projection, not a measured bill. Three statutes and a targeted adversarial probe do not establish general legal accuracy or regulatory compliance. No independent reproduction.

## Sources

- [Jev System One vs Specialized Sovereign RAG. An Empirical Benchmark](https://memonsystems.com/journal/jev-system-one-vs-specialized-sovereign-rag-an-empirical-benchmark/) — access: `fetched`; review: `sections_reviewed`.
- [GitHub - azterizm/jev-vs-sovereign-benchmark](https://github.com/azterizm/jev-vs-sovereign-benchmark) — access: `fetched`; review: `sections_reviewed`.
- [Related public project or article](https://memonsystems.com/journal/jev-system-one-vs-specialized-sovereign-rag-an-empirical-benchmark) — discovered via Discord source (private provenance retained locally); access: `fetched`; review: `sections_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
