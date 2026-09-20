# Jev-bot knowledge and answer flow

The default bot evaluates the full exported research library with Jev, rather than sending only an idea for classification. Both answer modes use the same corpus and evaluation pipeline.

## Two answer modes

- **Jev evidence:** Jev judges every research passage for relevance and applicable cautions. A second request evaluates fit, applicable decision primitives and required surrounding components using selected passages. The interface shows typed judgments and the exact passages, including citations.
- **Jev + GLM 5.3:** the same Jev evaluation runs first. GLM receives the user's idea, selected passages and Jev judgments, then writes a cited explanation. Proposed designs and uncertain conclusions are labeled separately from source claims. Citation IDs are checked against supplied passages; this is not an independent entailment or factual-accuracy guarantee.

```mermaid
flowchart TD
    L[Current local exported research] --> C[Complete research library]
    S[Private S3 snapshot] --> V[Verify archive checksum and immutable version]
    V --> C
    I[User idea] --> B[Lossless batches within request budgets]
    C --> B
    B --> J[Jev evaluates every passage]
    J --> E[Select relevant cases, lessons and cautions]
    E --> F[Jev assesses fit and component boundaries]
    F --> M{Answer mode}
    M --> O[Typed judgments and source passages]
    M --> W[GLM 5.3 writes cited explanation]
    W --> Q[Validate structure and citation IDs]
    Q --> A[Written answer with evidence]
```

## What reaches the models

All Markdown documents under `docs/` are loaded: every exported case, the master guide, capability reference, community findings, integration lessons, review gaps, promoted YouTube transcript reviews and supporting guides. Held cases are evaluated too; their caveats are evidence, not permission to present them as validated implementations. No keyword or design-family filter removes documents before Jev evaluation.

Documents are split without discarding text. Every passage reaches a Jev request with the user's idea. The initial evaluation uses independent relevance and caution questions. Source material is explicitly treated as data, not instructions.

The final fit assessment and writer receive a smaller, reported selection, balancing cases, relevant cautions and guides. They do not receive the entire library in one request. Full-library evaluation means the text was included in successful requests; it does not prove the model interpreted every fact correctly. The interface reports documents and passages evaluated, selected passage count and failures.

The private backup also contains raw messages, caches, media, code and operational records. These are **not** automatically forwarded to either provider. This runtime uses the exported research-text layer. Image, audio and video content must be represented by reviewed text to inform an answer; unresolved media remains a recorded gap.

## S3 is an actual selectable source

S3 mode loads research documents from the archive version recorded in the verified local backup receipt. A matching local downloaded archive may be reused only after checksum verification. If absent, the application downloads the exact object version with an expected-owner check and verifies its checksum before reading it. Documents are read directly from the archive, never extracted using archive paths.

The UI labels this as a verified cache of an immutable S3 snapshot. It does not imply a fresh bucket listing on every question. S3 mode never silently falls back to current local files. Local mode reads current exported files, so it may include changes newer than the backup. Exact snapshot excerpts are shown in answers; links to whole documents open the current local export.

Bucket names, account IDs, object keys and receipts remain in ignored local storage. No credential reaches a model or the browser.

## Running and configuring

Put `jev_api_key` in local `.env.local`. Written mode additionally needs `glm_key` with access to the Z.ai model API for `glm-5.3`. The configured endpoint is `https://api.z.ai/api/paas/v4/chat/completions`; no endpoint substitution or model downgrade occurs on failure.

```sh
python3 scripts/serve_bot.py
python3 scripts/jev_bot.py "Where could Jev help with my idea?" --mode evidence --source local
python3 scripts/jev_bot.py "Where could Jev help with my idea?" --mode written --source s3
python3 scripts/jev_bot.py "Route support email" --offline
```

`--offline` preserves the old authored-template preview without network calls; it is not the full-library Jev mode. Both main modes make paid model requests. Progress is reported through background answer jobs. Successful Jev evaluations are reused in a bounded in-memory cache keyed by the exact idea, state, model, questions and prompt version. Changed text invalidates cached evaluations. Jobs expire from the accessible job list after 30 minutes when new work starts; process restart clears all in-memory state. No chat history is written to disk by the application.

Failed scan batches leave coverage incomplete and prevent a final assessment or written answer. A failed writer preserves Jev results and reports that no generated answer was produced. Provider bodies, credentials and internal tracebacks are not shown in the browser. An API key being present does not establish provider balance or model access.

## Tokens and estimated cost

Each result includes a per-stage table of model, status, input tokens, output tokens and estimated USD. Written mode compares Jev's full-library evaluation with GLM's explanation from selected evidence. These are different workloads, not an interchangeable-model benchmark. No additional model call is made for this comparison.

Token counts come from provider responses for new requests in the current run. In-memory Jev cache hits reuse earlier results and add no new requests or tokens; earlier charges are not counted again. Failed or retried attempts without usage keep the total unknown. A GLM response rejected by citation validation still retains reported usage and its estimate. Failed or skipped writing never displays a fabricated zero charge.

Rates verified on 20 September 2026: [Jev 1.13.0](https://docs.typesafe.ai/models) costs $0.042 per million input tokens, with free output. [GLM 5.3](https://docs.z.ai/guides/overview/pricing) costs $1.40 per million input tokens, $0.26 per million cached input tokens and $4.40 per million output tokens. Reported cached input is discounted; absent cache counts use a disclosed uncached-input assumption. Unknown model versions are not assigned guessed rates. Estimates exclude credits, discounts, taxes, storage and transfer; invoices may differ. Pricing must be rechecked when provider rates change.

## Verified interface references

[Jev state](https://docs.typesafe.ai/concepts/state), [typed questions](https://docs.typesafe.ai/primitives), and [context limits](https://docs.typesafe.ai/models) define the text-evaluation contract. [Z.ai chat completions](https://docs.z.ai/api-reference/llm/chat-completion) documents the GLM 5.3 endpoint and JSON output option. Request byte caps are conservative engineering limits, not exact tokenizer measurements.
