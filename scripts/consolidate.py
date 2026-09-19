"""Rebuild the frozen snapshot offline, preserving capture and review boundaries."""
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def run(name, *args):
    subprocess.run([sys.executable, str(ROOT/'scripts'/name), *args], cwd=ROOT, check=True)


def write_status():
    pool = ROOT/'resource-pool'
    summary = json.loads((pool/'coverage-summary.json').read_text())
    media = json.loads((pool/'sources/media-accounting.json').read_text())
    x_queue = json.loads((pool/'sources/x-review-backlog.json').read_text())
    x_counts = x_queue['counts']
    cp_path = pool/'sources/collection-checkpoint.json'
    cp = json.loads(cp_path.read_text())
    cp.setdefault('research_status', 'frozen_snapshot_bot_preview')
    if summary['s3_uploaded']:
        cp['s3_status'] = 'verified_private_backup'
    else:
        cp.setdefault('s3_status', 'backup_requested_not_yet_verified')
    cp['s3_uploaded'] = summary['s3_uploaded']
    cp['review_progress'].update(curated_cases=summary['curated_cases'],
        editorial_uncatalogued_rows=summary['editorial_review']['unassigned_messages'],
        external_review_status_counts=summary['external_review_status_counts'],
        media_reviewed_messages=media['content_review_counts'].get('content_reviewed', 0),
        fully_reviewed_through_message_id=None, exhaustive=False)
    cp_path.write_text(json.dumps(cp, indent=2)+'\n')
    n, enabled = summary['curated_cases'], summary['default_retrieval_cases']
    pending = summary['external_review_status_counts'].get('not_reviewed', 0)
    gaps = summary['external_urls_with_content_gaps']
    text = f'''# Frozen snapshot and completion status

Capture cutoff: **19 September 2026, 10:08:31 IST / 04:38:31 UTC**. New source collection is paused while this snapshot becomes a usable system. The exact last-post link and capture cursor are preserved privately. Capture progress is separate from content-review progress.

| Layer | Current state | Remaining scope |
|---|---|---|
| Captured source | 3,226 main rows, 142 supplementary thread rows; 3,358 unique IDs; 14 discovered threads | No independent server-total reconciliation; newer posts and undiscovered threads excluded |
| Editorial accounting | All 3,358 IDs have case links or explicit dispositions; zero uncatalogued | Unresolved-media and insufficient-evidence dispositions remain unresolved |
| Cases | {n} write-ups; {enabled} eligible for default retrieval; {n-enabled} held back | Further source validation can correct or merge cases |
| External URLs | {summary['external_urls']} registered; {pending} await first disposition; {gaps} retain explicit content gaps | Access failures, metadata shells and uninspected media remain unresolved; scoped reviews do not validate every nested link |
| Context screening | {summary['external_review_status_counts'].get('context_only_not_jev_evidence', 0)} links scoped as unrelated context; {summary['external_review_status_counts'].get('metadata_only', 0)} metadata-only pages | Scope screening does not establish absence of a possible Jev integration |
| X | {len(x_queue['entries'])} distinct posts: {x_counts.get('reviewed', 0)} reviewed, {x_counts.get('pending_media', 0)} media-pending, {x_counts.get('pending_thread_expansion', 0)} thread-expansion pending, {x_counts.get('pending', 0)} pending | Text review does not inspect video/images; scheduled review remains paused |
| Attachments | {media['attachments_reviewed']} / {media['unique_urls']} attachment URLs reviewed; {media['content_review_counts'].get('content_reviewed', 0)} / {media['messages']} messages complete | {media['attachments_pending']} attachments across {sum(r['remaining_attachments'] > 0 for r in media['entries'])} messages pending |
| Bot | Local web/CLI assistant, 11 authored design families, attributed case cards, counterexamples and optional Jev routing | No free-form generative model, broad conversational memory or production validation |
| S3 | {'Encrypted private snapshot uploaded and download/file hashes verified' if summary['s3_uploaded'] else 'Requested; no verified backup yet'} | Backup state is separate from evidence review |

## What the counts mean

All original 2,994 pending messages were read and given explicit editorial decisions. That closes message accounting. It does not turn every message into a verified implementation. The case-linked count overlaps with unresolved evidence flags, which remain in the editorial ledger.

External-source statuses distinguish full saved-text inspection, README inspection, visible post text, metadata shells, limited context screening, media gaps and access failures. Old attachment URL failures do not prove the images are inaccessible in the authenticated source UI. No community benchmark has been independently reproduced.

The earlier first pass through the 296-URL backlog assigned every entry a disposition: 224 received text, artifact or relevance review, 39 had access failures and 33 needed non-text inspection. Those were historical first-pass counts, not completed validations or current gap totals. Subsequent recovery reviews update the table above and preserve previous attempts in the source ledger. The 30-source Jev pilot completed 60 calls and 130 draft claim checks; all 30 sources still needed deep review, so no reduction in editorial effort is established. [Pilot report](../docs/source-grounding-pilot.md).

The original Jev triage experiment processed all 3,358 IDs with 420 successful requests for its final prompt. Its 13-item development sample matched 13 contribution labels and 11 relationship labels; it is not a representative accuracy estimate.

## Run and update

`python3 scripts/serve_bot.py` starts the local assistant. `python3 scripts/consolidate.py` rebuilds curated files, evidence indexes and sanitized public docs from the frozen private snapshot without network calls. `python3 scripts/stage_capture.py incoming.json` deduplicates a later authorized local capture and queues new or edited rows without changing the frozen snapshot. Promotion and editorial review remain explicit steps; there is no unattended Discord crawler.

The next collection pass should read overlap around the saved post and revisit known threads. Preserve edits, identify new IDs, review the delta, then publish a new snapshot. Do not advance a fully-reviewed cursor from mere capture, triage or upload success.

## Source of counts

[Coverage](coverage-summary.json) · [Source review ledger](sources/source-reviews.json) · [Media accounting](sources/media-accounting.json) · [Answer guide](jev-bot-answer-guide.md) · [Research pipeline](../research/README.md). Development check results are stored locally in `research/evaluations/`.
'''
    (pool/'completion-status.md').write_text(text)
    resume = f'''# Frozen Jev snapshot — continuation checkpoint

User chose to stop new source collection and consolidate a usable assistant. S3 backup is authorized. Scheduled X reviews remain PAUSED. Never expose credentials or private provenance in the public repository.

## Exact capture boundary

- Last saved main post: [{cp['capture_high_water_message_id']}]({cp['capture_high_water_url']}).
- Timestamp: **19 September 2026, 10:08:31 IST / 04:38:31 UTC**.
- Content: dating-message demo, `https://jevdating.pages.dev/`.
- Earliest saved ID: {cp['earliest_captured_message_id']}; visible beginning reached, not independently reconciled.
- Thread cursors remain in `resource-pool/sources/collection-checkpoint.json`.
- Fully reviewed through: **unknown**. Never substitute the capture cursor.

## Consolidated state

All 3,358 IDs have editorial dispositions. {n} cases; {enabled} default eligible. {pending}/{summary['external_urls']} external URLs await first disposition; {gaps} retain explicit content gaps. {media['attachments_reviewed']} attachments inspected; {media['attachments_pending']} pending. Existing source/media review notes remain authoritative. No independent community benchmark reproduction.

Local assistant: `python3 scripts/serve_bot.py`. Optional Jev sends entered ideas only. Public assets come from sanitized `docs/bot-cases.json`. Offline rebuild: `python3 scripts/consolidate.py`. Private backup: `python3 scripts/backup_private.py backup`; verified receipt under `research/storage/latest-backup.json` if present.

## Resume after this frozen version

1. Only resume source collection when requested. Read the exact last post with overlap and revisit existing threads for replies/edits.
2. Stage a local capture with `scripts/stage_capture.py`. It retains new and edited rows without changing the frozen corpus or review cursor. A new approved immutable snapshot and updated private checkpoint are required before normalizing/reviewing the delta.
3. Original editorial queue: `research/editorial/queue.json` (2,994 entries, complete). Do not regenerate or reclassify it as new work.
4. Stable external queues: `research/external-other-queue.json` (600 original entries) and `research/external-x-queue.json` (183 URL entries, 182 posts). Index-based review scripts depend on these exact queues. New discoveries live separately.
5. Do not rerun `review-x-0000.py`; it appends prose. Use idempotent review helpers. Update `resource-pool/cases.tsv` before rendering.
6. Preserve private GitHub artifact exclusions and message/attachment pair validation. Export then inspect public files before any push.

Current detailed gaps: `resource-pool/completion-status.md`. S3 backup does not close evidence gaps.
'''
    resume_path = ROOT/'RESUME.md'
    if resume_path.exists():
        previous = resume_path.read_text()
        # Storage approvals and active-work notes are operator-owned continuity.
        markers = ('## Pending storage approval', '## Active authorized work')
        positions = [previous.index(m) for m in markers if m in previous]
        if positions:
            resume += '\n' + previous[min(positions):]
    resume_path.write_text(resume)
    readme = ROOT/'README.md'
    body = readme.read_text()
    start, end = '<!-- SNAPSHOT-START -->', '<!-- SNAPSHOT-END -->'
    if start in body and end in body:
        table = f'''\n| Layer | Frozen snapshot |\n|---|---|\n| Capture cutoff | 19 September 2026, 10:08:31 IST |\n| Messages | 3,358 unique IDs; all editorially accounted for |\n| Cases | {n}; {enabled} default eligible, {n-enabled} held back |\n| External evidence | {summary['external_urls']} URLs; {pending} await first disposition; {gaps} retain content gaps |\n| Media | {media['attachments_reviewed']} / {media['unique_urls']} attachments inspected |\n| Bot | Local preview; 11 authored design families |\n| S3 | {'Private backup verified' if summary['s3_uploaded'] else 'Backup pending'} |\n\n'''
        readme.write_text(body.split(start)[0]+start+table+end+body.split(end, 1)[1])


def main():
    for name, args in [('build-source-index.py', []), ('render-cases.py', []), ('build-x-backlog.py', []),
                       ('audit_media.py', ['--offline']), ('build-pool-index.py', [])]:
        run(name, *args)
    write_status()
    run('evidence.py', 'build')
    run('evaluate_retrieval.py', '--output', str(ROOT/'research/evaluations/retrieval-report.json'))
    # Rehash after generated status/checkpoint changes.
    run('build-pool-index.py')
    run('export_public.py')
    run('evaluate_bot.py')


if __name__ == '__main__':
    main()
