# Snapshot, assistant and incremental updates

## Current architecture

```text
Authorized source capture → private immutable snapshots + capture cursor
                         → Jev triage + explicit editorial review
                         → cases.tsv + source/media review ledgers
                         → offline consolidation
                           ├─ private searchable evidence index
                           ├─ sanitized public Markdown + bot-cases.json
                           └─ private encrypted S3 backup

User idea → local keyword routing or optional Jev Choice
          → authored integration family + curated topical neighborhood
          → related cases + counterexamples + complete limitations
          → proposed design, source links and validation plan
```

The bot reads the sanitized public snapshot. Raw source messages, private links and credentials never enter its browser response. Optional Jev routing sends only the idea text. No generative model or automatic action execution is enabled.

## Freeze and rebuild

The saved capture ends on 19 September 2026 at 10:08:31 IST. The last post and main/thread high-water marks remain in the private checkpoint. Every captured message ID has an editorial disposition; supporting external sources and media still have gaps.

With private inputs available:

```sh
python3 scripts/consolidate.py
python3 scripts/evaluate_bot.py
python3 -m unittest discover -s tests -v
python3 scripts/backup_private.py backup --region us-east-1
```

Consolidation performs no network calls. Backup is a separate explicit operation. It writes a unique snapshot prefix, uses versioned objects, verifies encryption and private access settings, then downloads the archive and checks every file hash. Receipts stay under ignored `research/storage/`. Never restore an untrusted archive by blindly extracting its paths.

## Next collection pass

1. Reopen the saved last post with overlap; inspect known threads for later replies and edits. Do not assume a single main-channel cursor covers thread updates.
2. Save an authorized local capture using the existing schema: `guild_id`, plus `messages` containing `id`, `text`, and `links` entries with `text` and `url`. Message IDs use `chat-messages-<channel-id>-<message-id>`. Exact identifiers stay private.
3. Run `python3 scripts/stage_capture.py incoming.json`. New, edited and unchanged rows are retained in an immutable, content-addressed incoming batch. Repeating the same batch is idempotent. This stage does not advance the frozen capture cursor or the review cursor.
4. Review the delta and promote an approved immutable snapshot through the existing private snapshot/checkpoint workflow. Merge by message ID, preserve changed versions and update separate thread cursors. Promotion is currently manual; no unattended Discord crawler or auto-publisher exists.
5. Normalize and triage the approved snapshot. Use bounded API requests; changed batches may require reprocessing. Clear stale editorial decisions only after reviewing changed content. Update the editorial source and source/media review ledgers.
6. Consolidate, test, inspect the public export, and create another private backup. A future scheduled collector can call this flow once its authenticated capture mechanism and review policy are explicitly chosen.

Capture completeness, editorial accounting, source validation, bot quality and backup success are separate gates. The fully-reviewed cursor remains unset while substantive evidence gaps exist.

## Current assistant limits

The interface supports an idea and iterative edits, not persistent multi-turn memory. Local routing is a keyword heuristic; optional Jev routing is a model prediction with an uncalibrated development threshold. The assistant uses 11 authored families and manually selected relevant case neighborhoods, then ranks cases locally. It does not invent project facts, benchmark numbers or sources. It can miss an appropriate family or precedent. Financial and clinical examples remain evidence discussions, not advice.

Development fixtures check natural-language ideas, policy boundaries, abstention, source resolution and retention of case limitations. They are authored during development, not independent measurements of general usefulness.
