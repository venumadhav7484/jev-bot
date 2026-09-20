# Snapshot and completion status

Published-library capture boundary: **20 September 2026, 22:25:06 IST / 16:55:06 UTC**. Staged incoming batches remain separate until promotion. The exact last-post link and capture cursor are preserved privately. Capture progress is separate from content-review progress.

| Layer | Current state | Remaining scope |
|---|---|---|
| Captured source | 4051 main rows, 142 supplementary thread rows; 4183 unique IDs; 14 discovered threads | No independent server-total reconciliation; newer posts and undiscovered threads excluded |
| Editorial accounting | 4183 IDs have case links or explicit dispositions; 0 uncatalogued | Unresolved-media and insufficient-evidence dispositions remain unresolved |
| Cases | 466 write-ups; 386 eligible for default retrieval; 80 held back | Further source validation can correct or merge cases |
| External URLs | 1083 registered; 219 await first disposition; 285 retain explicit content gaps | Access failures, metadata shells and uninspected media remain unresolved; scoped reviews do not validate every nested link |
| Context screening | 192 links scoped as unrelated context; 20 metadata-only pages | Scope screening does not establish absence of a possible Jev integration |
| X | 211 distinct posts: 140 reviewed, 0 media-pending, 38 thread-expansion pending, 33 pending | Text review does not inspect video/images; scheduled review remains paused |
| Attachments | 174 / 570 attachment URLs reviewed; 148 / 511 messages complete | 396 attachments across 363 messages pending |
| Bot | Local web/CLI assistant; full-library Jev evaluation, optional GLM 5.3 writing and local/S3 research sources | Source/media gaps remain; no independent answer-accuracy or production validation |
| S3 | Encrypted private snapshot uploaded and download/file hashes verified | Backup state is separate from evidence review |

## What the counts mean

The original review covered 2,994 queued messages. Current accounting counts appear above; newer captured records require separate dispositions. It does not turn every message into a verified implementation. The case-linked count overlaps with unresolved evidence flags, which remain in the editorial ledger.

External-source statuses distinguish full saved-text inspection, README inspection, visible post text, metadata shells, limited context screening, media gaps and access failures. Old attachment URL failures do not prove the images are inaccessible in the authenticated source UI. No community benchmark has been independently reproduced.

The earlier first pass through the 296-URL backlog assigned every entry a disposition: 224 received text, artifact or relevance review, 39 had access failures and 33 needed non-text inspection. Those were historical first-pass counts, not completed validations or current gap totals. Subsequent recovery reviews update the table above and preserve previous attempts in the source ledger. The 30-source Jev pilot completed 60 calls and 130 draft claim checks; all 30 sources still needed deep review, so no reduction in editorial effort is established. Pilot report (local-only evidence).

The original Jev triage experiment processed all 3,358 IDs with 420 successful requests for its final prompt. Its 13-item development sample matched 13 contribution labels and 11 relationship labels; it is not a representative accuracy estimate.

## Run and update

`python3 scripts/serve_bot.py` starts the local assistant. `python3 scripts/consolidate.py` rebuilds curated files, evidence indexes and sanitized public docs from the frozen private snapshot without network calls. `python3 scripts/stage_capture.py incoming.json` deduplicates a later authorized local capture and queues new or edited rows without changing the frozen snapshot. Promotion and editorial review remain explicit steps; there is no unattended Discord crawler.

The next collection pass should read overlap around the saved post and revisit known threads. Preserve edits, identify new IDs, review the delta, then publish a new snapshot. Do not advance a fully-reviewed cursor from mere capture, triage or upload success.

## Source of counts

Coverage (local-only evidence) · Source review ledger (local-only evidence) · Media accounting (local-only evidence) · [Answer guide](jev-bot-answer-guide.md) · [Research pipeline](research-pipeline.md). Development check results are stored locally in `research/evaluations/`.
