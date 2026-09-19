# Frozen snapshot and completion status

Capture cutoff: **19 September 2026, 10:08:31 IST / 04:38:31 UTC**. New source collection is paused while this snapshot becomes a usable system. The exact last-post link and capture cursor are preserved privately. Capture progress is separate from content-review progress.

| Layer | Current state | Remaining scope |
|---|---|---|
| Captured source | 3,226 main rows, 142 supplementary thread rows; 3,358 unique IDs; 14 discovered threads | No independent server-total reconciliation; newer posts and undiscovered threads excluded |
| Editorial accounting | All 3,358 IDs have case links or explicit dispositions; zero uncatalogued | Unresolved-media and insufficient-evidence dispositions remain unresolved |
| Cases | 420 write-ups; 362 eligible for default retrieval; 58 held back | Further source validation can correct or merge cases |
| External URLs | 826 registered; 296 not reviewed | Metadata-only and context-only dispositions are not technical validation |
| Context screening | 146 links scoped as unrelated context; 93 metadata-only pages | Scope screening does not establish absence of a possible Jev integration |
| X | 182 distinct posts: 42 reviewed, 128 media-pending, 8 thread-expansion pending, 4 pending | Text review does not inspect video/images; scheduled review remains paused |
| Attachments | 10 / 413 attachment URLs visually reviewed; 7 / 370 messages complete | 403 attachments across 363 messages pending |
| Bot | Local web/CLI assistant, 11 authored design families, attributed case cards, counterexamples and optional Jev routing | No free-form generative model, broad conversational memory or production validation |
| S3 | Requested; no verified backup yet | Backup state is separate from evidence review |

## What the counts mean

All original 2,994 pending messages were read and given explicit editorial decisions. That closes message accounting. It does not turn every message into a verified implementation. The case-linked count overlaps with unresolved evidence flags, which remain in the editorial ledger.

External-source statuses distinguish full saved-text inspection, README inspection, visible post text, metadata shells, limited context screening, media gaps and access failures. Old attachment URL failures do not prove the images are inaccessible in the authenticated source UI. No community benchmark has been independently reproduced.

The original Jev triage experiment processed all 3,358 IDs with 420 successful requests for its final prompt. Its 13-item development sample matched 13 contribution labels and 11 relationship labels; it is not a representative accuracy estimate.

## Run and update

`python3 scripts/serve_bot.py` starts the local assistant. `python3 scripts/consolidate.py` rebuilds curated files, evidence indexes and sanitized public docs from the frozen private snapshot without network calls. `python3 scripts/stage_capture.py incoming.json` deduplicates a later authorized local capture and queues new or edited rows without changing the frozen snapshot. Promotion and editorial review remain explicit steps; there is no unattended Discord crawler.

The next collection pass should read overlap around the saved post and revisit known threads. Preserve edits, identify new IDs, review the delta, then publish a new snapshot. Do not advance a fully-reviewed cursor from mere capture, triage or upload success.

## Source of counts

Coverage (local-only evidence) · Source review ledger (local-only evidence) · Media accounting (local-only evidence) · [Answer guide](jev-bot-answer-guide.md) · [Research pipeline](research-pipeline.md). Development check results are stored locally in `research/evaluations/`.
