# Research pipeline and completion contract

Discord is the primary discovery source for community practice. The original implementation, repository and evaluation artifact are supporting primary evidence for a particular claim. Official documentation remains the reference for API contracts. None of these sources alone guarantees a claim is correct.

## What changed

The first pass captured messages and drafted cases but did not account for every message or inspect most external evidence. This pipeline makes the missing work explicit. It does not turn model labels into verified findings.

1. Normalize all saved Discord snapshots while retaining original rows, variants, IDs, timestamps, links and quoted context.
2. Use Jev Choice for contribution type and established Jev relationship; use independent Noul questions for implementation details, negative evidence, measurements, tooling and missing context.
3. Preserve every prediction and probability. No low-confidence or apparently irrelevant post is discarded automatically. Quoted posts and neighboring conversation are context, not new claims by the reply author.
4. Review implementations, limitations, corrections, evaluations, tools and questions in linked queues. Inspect original sources before promoting claims to the curated pool.
5. Search both message evidence and curated cases locally with source links and evidence status.

## Run and resume

Python standard library only. Credentials load from `jev_api_key` in the process environment, then `.env.local`, then `.env`. Environment files are Git-ignored. Do not put credentials in reports or source records.

```sh
python3 scripts/jev_triage.py prepare
python3 -m unittest discover -s tests -v
python3 scripts/jev_triage.py run --max-requests 4 --max-input-tokens 60000
python3 scripts/jev_triage.py run --max-requests 450 --max-input-tokens 5000000
python3 scripts/jev_triage.py report
python3 scripts/evidence.py build
python3 scripts/evidence.py search "routing email" --limit 8
```

`run` sends captured text to the TypeSafe API. Each successful batch is saved immediately. Restarting skips matching completed request hashes. Changed source context, prompts or models cause a new hash; old responses remain available for audit. The per-run input-token stop is soft: one in-flight window may exceed it. At most four calls are in flight, with bounded server-error retries. Ambiguous transport failures are not automatically retried because the server may already have processed the request.

Triage index (local-only evidence) links to every category queue. Machine-readable summary (local-only evidence) separates triaged counts from editorial approval. Response files include returned model and usage, never request headers or API keys. The SQLite database is a rebuildable local retrieval artifact; no data is uploaded to S3.

## Applying TypeSafe primitives

The [primitives guide](https://docs.typesafe.ai/primitives) recommends focused judgments, independent questions over shared state, explicit field paths, and host-code composition. Accordingly, questions identify the exact message body with a backticked path. Choice includes `unclear` and `not_established` outcomes. Noul values prioritize review; they are not impact scores or proof of correctness. Score is not needed for the current routing task. Dependent link discovery and synthesis happen after classification, outside the request.

The [API reference](https://docs.typesafe.ai/api) defines request and response validation. The [model reference](https://docs.typesafe.ai/models) documents text-only inputs: this pipeline cannot inspect videos or screenshots through Jev. Media remains an explicit gap. The primitives page's approximate 32k request-budget wording differs from the model page's 64k-total/32k-state-plus-longest-question limits; batching uses conservative byte bounds instead of assuming either maximum can safely be filled.

## Completion gates

| Workstream | Completion condition | Evidence retained |
|---|---|---|
| Capture | Known snapshot boundaries and reconciled accessible IDs, or an explicit reconciliation limitation | Raw snapshots, source hashes, main and thread cursors |
| Triage | Every captured ID has a machine disposition or explicit processing error | Predictions, model/rubric versions, attempt records |
| Editorial accounting | Every ID is linked to a case, finding, tool, correction, discussion, or reasoned exclusion | Editorial disposition and cited source IDs; distinct from model suggestion |
| External evidence | Every substantive URL inspected or assigned a specific access blocker | Access method/date, review notes, artifacts and unresolved media |
| Case synthesis | What/how/why/impact, Jev's exact role, surrounding tools, uncertainty, limits and source links | Curated case plus contradictory and supporting sources |
| Cross-case synthesis | Capabilities, strengths, weaknesses, creative patterns, tools and open questions supported by cases | Finding ledger with evidence type and source links |
| Bot readiness | Retrieval preserves evidence status; sample answers cite correct evidence, abstain when unsupported, and handle counterexamples | Answer evaluations and failures, separate from collection coverage |

Comprehensive coverage means every accessible source is accounted for and every unavailable source has a visible gap. It does not mean every claim is true or every benchmark was reproduced. Do not report a single completion percentage that mixes these gates.

## Known remaining risks

- UI capture has not been reconciled against an independent server export. New or undiscovered threads can remain outside the archive.
- Rendered text contains embed previews and some reaction counts. Header extraction is conservative and preserves raw text, but is not equivalent to Discord's structured message API.
- 118 initially captured messages have fewer than 30 body characters and a Discord attachment. Text-only classification cannot resolve their substantive content.
- Model relation labels can miss explicit proposed use. Keep low-value and unrelated predictions available for review; do not let a classification remove evidence.
- Thread context can extend beyond adjacent messages and quoted previews. Final case synthesis must inspect the whole relevant discussion.
- The daily X automation covers only its saved X backlog, not Discord updates or completion of all editorial work.
