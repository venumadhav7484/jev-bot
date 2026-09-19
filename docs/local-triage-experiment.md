# Local use case: Jev helps build the Jev knowledge base

This is our own implementation, not a community showcase or an independent reproduction of someone else's benchmark.

## What

Route every saved Discord message into evidence-review queues while preserving original IDs, context, source links and uncertainty. Keep weak and negative evidence visible alongside positive applications.

## How

The host normalizes rendered Discord headers, separates quoted previews and thread snippets, and retains original variants. Eight target messages normally share one state, with neighboring messages supplied as context. Each target receives two Choice questions and five Noul questions. Request size checks reduce batch size when necessary; no target text is silently truncated.

Choice identifies the contribution type and the relationship to Jev. Noul flags implementation detail, negative evidence, measurements, tooling and missing context. Host code combines these signals into review priority. Every response is checked against expected IDs, option sets, probability ranges and usage fields. Cache keys preserve criterion insertion order because order may affect predictions.

Successful responses are written atomically. Interrupted runs resume missing request hashes. API credentials come from `.env.local` and never appear in request caches or reports. A process lock prevents concurrent duplicate runs. External link fetching, source review and prose synthesis remain separate work.

## Measured result

The final prompt version processed **3,358 unique captured message IDs in 420 successful requests**, using **4,389,184 reported input tokens**. All returned `jev-1.13.0`. Six earlier development calls are retained separately; their outputs are not mixed into the final-version counts. Failed transport attempts have uncertain server processing and are not represented as successful calls.

A small, assistant-reviewed development sample contained 13 messages. Primary category matched the allowed labels for 13; Jev-use relationship matched for 11. The two misses concerned proposed integrations. This sample is too small and selected during development, so it does not estimate corpus accuracy or validate automatic exclusion.

## Why this helps

Every captured message now has a machine suggestion and a direct route back to evidence. Review can prioritize implementation details, disagreements, failure modes and tools. Local SQLite search covers messages and curated cases together, with distinct evidence status and default-retrieval eligibility.

## Limits

Classification does not resolve duplicate projects, validate authors' claims, inspect external destinations, transcribe attachments or write trustworthy case synthesis by itself. The pipeline therefore makes no automatic editorial approvals. It preserves apparently irrelevant and low-value predictions for audit, and gives sparse attachment posts a review priority regardless of the model label.

## Sources and reproducibility

- [Pipeline implementation](../scripts/jev_triage.py)
- [Tests](../tests/test_jev_triage.py)
- Final-version metrics (local-only evidence)
- Sample audit and specific errors (local-only evidence)
- Queues and predictions (local-only evidence)
- [TypeSafe primitives](https://docs.typesafe.ai/primitives), [API schema](https://docs.typesafe.ai/api), [model reference](https://docs.typesafe.ai/models)
