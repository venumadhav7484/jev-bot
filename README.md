# Jev-bot

A public web app and local CLI for one question:

> Describe your use case or idea. Where could Jev help, what else would you need, and what are the limits?

The assistant evaluates the complete exported research library with Jev: every use case, guide, finding and recorded lesson. The public website combines Jev judgments with a GLM 5.3 visual design grounded in selected evidence. The local CLI also supports Jev-only judgments and a verified private S3 snapshot. See the [knowledge and answer flow](docs/bot-knowledge-flow.md).

## Try it

**[Open Jev-bot](https://dm6rtlrn56ej8.cloudfront.net/#bot)** · **[Browse 466 use cases](https://dm6rtlrn56ej8.cloudfront.net/#use-cases)**

The hosted app needs no account or API key from visitors. Describe an idea, review its proposed workflow and example request, then leave feedback. The progress spinner runs until the answer arrives or the request fails.

### Run locally

Python 3.11+; standard library only. Full-library modes need `jev_api_key`; written mode also needs `glm_key`. The legacy CLI `--offline` preview needs no key.

```sh
git clone https://github.com/venumadhav7484/jev-bot.git
cd jev-bot
cp .env.example .env.local
# Add your own jev_api_key and glm_key to .env.local for web answers.
python3 scripts/serve_bot.py
```

Open **http://127.0.0.1:8765**. Describe an idea, or try the su-lekha example. Add details to the description to refine the result. No conversation history is saved. The server binds to loopback and serves only public assets; it is not a hosted production service.

The public site has one answer flow: Jev reviews the library and GLM builds a visual proposed design with example inputs, copyable JSON and external sources. Users can type or import UTF-8 TXT, MD, CSV or JSON into the editable idea field (6,000 characters total; files up to 256 KB). Files are read in the browser; only the reviewed text is sent on submission. PDF, Word and images are not supported. Preview outputs are illustrative, not live inference.

Use **Explore Jev use cases** to browse the full public catalog, filter six broad categories, search, or randomize the tiles. Each case page includes a prebuilt visual workflow, two illustrative inputs with matching Jev JSON, expected application actions, and original public links. Project reports remain separate and expandable; weak evidence and reported failures stay visible. Examples are teaching adaptations, not original project code or guaranteed outputs. Browsing makes no model requests. Fit signals describe evidence types, not benchmark scores. Bot answers show a visual workflow, selectable example inputs and outputs, copyable Jev JSON, and external project links; supporting notes and usage details remain expandable. Navigation back to the bot preserves the current idea and result during the session.

Put `jev_api_key` and, for written mode, `glm_key` in local `.env.local`. Jev receives your idea and all exported research text in bounded batches. GLM receives your idea, Jev judgments and selected passages. Each answer shows provider-reported input/output tokens and estimated USD per stage; written mode compares Jev with GLM 5.3 and shows a combined estimate. These stages perform different work. Local Jev cache hits add no new requests; missing usage or unreported attempts keep total cost unknown. API usage applies. Progress and actual coverage are shown; failed evaluations never silently become local-template answers. S3 mode uses the verified snapshot receipt and checksum-checked archive cache; AWS CLI and credentials are needed if that archive must be downloaded.

```sh
python3 scripts/jev_bot.py "Route incoming invoices to the right queue" --mode evidence
python3 scripts/jev_bot.py "Monitor sensitive information in AI applications" --mode written --source s3
python3 scripts/jev_bot.py "Route support email" --offline
python3 -m unittest discover -s tests -v
node --test tests/*.mjs  # Browser logic and catalog checks; Node.js 18+
```

## AWS hosting

`python3 scripts/deploy_cloud.py` prepares an allowlisted site and Lambda bundle without contacting AWS. `python3 scripts/deploy_cloud.py --apply` deploys private S3, CloudFront, HTTP API Gateway, Lambda workers and DynamoDB; `python3 scripts/cloud_status.py` checks rollout and records its HTTPS URL. AWS deployment permissions and local API keys are required. Deployment receipts, bundles and the verification records stay in ignored `research/hosting/`.

The hosted site is public: no login or access code. The deployment allows 10 simultaneous answers and 5,000 starts per UTC day, with a 15-minute worker limit. Capacity can be set with `--daily-limit` and `--max-concurrent`; subsequent deploys preserve those settings. Busy slots and the daily cap produce separate errors. The deployed library includes every exported research document; the older private S3 backup is not used as live context. Research updates require redeployment. No custom domain is purchased. Deployment submission alone is not a successful live-site check.

## Response feedback

Completed bot answers show thumbs up/down and an optional comment (up to 2,000 characters). Each answer accepts one rating and one comment; identical retries do not log duplicate feedback. Only completed, unexpired answer IDs are accepted. Feedback does not invoke Jev or GLM or consume answer capacity.

Hosted feedback is recorded as structured `answer_feedback` events in the API Lambda CloudWatch log group (`/aws/lambda/jev-bot-hosted-api`), retained for 30 days. Events contain `job_id`, `submitted_at`, and `rating` or `comment`; no query text, answer body, IP address or browser identity is added. The job ID can be correlated with its private answer result during the existing one-day result lifetime. Feedback is also saved on that short-lived job to deduplicate retries. Local feedback goes to ignored `research/feedback/local.jsonl`.

CloudWatch Logs Insights, with the API log group selected:

```text
fields @timestamp, job_id, rating, comment
| filter event = "answer_feedback"
| sort @timestamp desc
| limit 100
```

## Published snapshot

The latest published main-channel capture boundary appears below. The exact last-post link and thread cursors are retained privately, so a later pass can resume with overlap and deduplication. Scheduled X reviews remain paused.

<!-- SNAPSHOT-START -->
| Layer | Frozen snapshot |
|---|---|
| Capture cutoff | 20 September 2026, 22:25:06 IST / 16:55:06 UTC |
| Messages | 4193 unique IDs; 4193 editorially accounted for |
| Cases | 466; 386 default eligible, 80 held back |
| External evidence | 1086 URLs; 0 await first disposition; 125 retain content gaps |
| Media | 430 / 571 attachments inspected |
| Bot | Full-library Jev; optional GLM 5.3 writing |
| S3 | Private backup verified |

<!-- SNAPSHOT-END -->

**Accounting is not validation.** The catalog includes author reports, tools, proposals and counterexamples. Default eligibility does not mean independently verified. Metadata-only pages, context screening and text reviews with missing media remain distinct from substantive technical inspection. No community benchmark has been independently reproduced.

## Read the evidence

- **[Jev master guide](docs/jev-master-guide.md):** start here for the consolidated capabilities, strengths, failures, effective designs, evaluation lessons, tools, costs and remaining unknowns.
- [Capability reference](docs/jev-knowledge-reference.md): primitives, APIs, integration patterns and official sources.
- [Use-case catalog](docs/jev-usecases.md): what, how, why, reported impact, limitations and artifact links.
- [Latest implementation lessons and leads](docs/incremental-findings.md).
- [Community findings](docs/community-evidence-findings.md): strengths, failures, conflicting evidence and lessons.
- [Answer guide and su-lekha proposal](docs/jev-bot-answer-guide.md).
- [Completion status](docs/completion-status.md) and [aggregate metrics](docs/metrics.json).
- [Paused review backlog](docs/review-backlog.md): remaining evidence gaps and next actions.
- [Snapshot and update workflow](docs/system-workflow.md).
- [Cached-source grounding pilot](docs/source-grounding-pilot.md): measured API usage, citation checks and review limits.
- [Local media processing](docs/media-processing.md): frame extraction, local speech transcription, OCR and editorial review boundaries.
- [Development checks](docs/development-checks.json): authored scenarios and a live API smoke test, with scope limits.

Both main answer modes evaluate every exported research document before selecting relevant passages. No fixed design-family neighborhood limits the search. Raw messages, unprocessed media, code and credentials in the private archive are not model context. Related cases remain analogies, not evidence that a proposed design will work. The older 11-family template preview remains available only through `--offline`; its tests do not establish general answer accuracy.

## How Jev is used

The research pipeline used Choice to categorize contributions and their relationship to Jev, with independent Noul questions for evidence dimensions. All model suggestions remain subject to editorial review. The bot uses Noul questions to evaluate every passage for relevance and applicable cautions, then Choice and Noul questions to assess selected evidence. Application code loads the corpus, preserves source text, handles budgets and checks citation IDs. Optional GLM 5.3 produces the written explanation. [TypeSafe primitives](https://docs.typesafe.ai/primitives).

## Repository layout

```text
docs/                       Sanitized public evidence and bot snapshot
web/                        Shared hosted and local browser interface
scripts/jev_bot.py          CLI and legacy offline design preview
scripts/research_answer.py  Full-library Jev evaluation and answer modes
scripts/knowledge_corpus.py Local/S3 research-text loading
scripts/answer_writer.py    GLM 5.3 cited explanation adapter
scripts/serve_bot.py        Loopback-only web server
scripts/cloud_bot.py        Hosted answer jobs and feedback endpoint
scripts/cloud_stack.py      AWS infrastructure template
scripts/deploy_cloud.py     Public asset and Lambda packaging/deployment
scripts/case_designs.py     Resumable prebuilt teaching examples
scripts/consolidate.py      Offline private-to-public snapshot rebuild
scripts/stage_capture.py    New/edited-message intake; no automatic collection
scripts/collect_discord.py  Optional read-only Discord bot history collector
scripts/plan_delta_review.py Reuse prior source reviews and cases in private batch packets
scripts/research_flow.py    Jev comparison, source refresh, GLM drafts and grounding checks
scripts/evidence.py         Private SQLite evidence search
scripts/jev_triage.py       Resumable Jev-assisted research triage
scripts/backup_private.py   Private S3 snapshot and download verification
tests/                     Boundary, retrieval, intake and response checks
```

## Add YouTube transcripts

Share transcript text and its video URL. The [transcript workflow](docs/youtube-source-workflow.md) preserves originals privately, extracts anchored claims, records source checks and contradictions, and exports reviewed summaries into the bot's local library. Unreviewed text is excluded. Local research is the default; S3 snapshots require a new backup to include later reviews. First reviewed video: [I Paired Jev With Astra](docs/youtube/youtube-2XFXe-oGnrI.md), including transcript corrections and unverified benchmark claims.

## Private research and backups

Public docs identify private provenance as **Discord source**. Raw messages, source identifiers and links, private artifacts, credentials, local databases and API caches remain ignored. Public repository, demo, article and official-documentation links remain in the case write-ups.

Research rebuild and incremental intake require the authorized local `resource-pool/`, `research/`, `RESUME.md` and root knowledge reference; these are not shipped in this public repository. `scripts/consolidate.py` regenerates curated Markdown, search indexes, completion reports and sanitized public exports offline. It does not call Jev or collect new posts.

S3 backup uses credentials from `.env.local`, creates an account-owned private bucket, blocks public access, enables encryption and versioning, and verifies downloaded archive and individual file hashes. Environment files and detected credentials are excluded. Bucket names, object keys and receipts remain local. Storage and transfer charges may apply. This backs up evidence; it does not host the bot.

Never blindly stage private builder output. Use the allowlisted exporter, inspect public changes and run `python3 scripts/check_public.py --staged` before every push. The guard checks loaded local credential values and private provenance; it is not a complete secret detector. `.gitignore` alone is not a publication review.

## Optional Discord API collection

The research pause remains in effect until a collection run is requested. This collector is optional and is not part of the public website or an automatic schedule. It requires the private source checkpoint and archives.

1. Create a bot in the Discord Developer Portal and enable **Message Content Intent**. A server administrator or member with **Manage Server** must install it in the source server. Restrict its channel access to the intended source; it needs **View Channel** and **Read Message History**, not send, moderation or administrator permissions.
2. Save its bot token as `discord_bot_token` in ignored `.env.local` (or `DISCORD_BOT_TOKEN` in the process environment). A browser login is not a bot credential. Never share the token in chat or commit it.
3. Install the optional dependency in a virtual environment, then explicitly run collection:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-discord.txt
.venv/bin/python scripts/collect_discord.py --limit 100
# Use --limit 0 to fetch all new main-channel messages through the run's start time.
```

`discord.py` handles pagination and API rate limits. The collector visits the main text channel, known public threads, and discovered active/archived public threads. Thread replies are additional to the main-channel limit. It revisits 20 messages at/before each saved cursor for edits; older edits, deleted messages and inaccessible/private threads are not exhaustively covered. New threads are read after the global capture boundary. It saves original message text, attachment metadata, embeds and available reply context under ignored `research/discord-captures/`, then stages a capture under `research/incoming/`. Media files are not downloaded or interpreted. API-format overlap can appear as edited against older browser-format captures; review these as format changes rather than presumed author edits.

Each run fixes its upper time boundary, records coverage, preserves partial output on failure, and leaves both frozen capture and review checkpoints unchanged. A bounded run explicitly reports `partial` when more main-channel messages remain. Repeated runs use the frozen checkpoint until a reviewed snapshot is promoted; they do not silently advance past pending evidence. No model is called by collection.

Use the printed `staged_batch` to prepare or explicitly run Jev triage in a separate private output directory:

```sh
python3 scripts/jev_triage.py prepare --batch-id BATCH_ID
python3 scripts/jev_triage.py run --batch-id BATCH_ID --max-requests 20 --workers 4
python3 scripts/plan_delta_review.py --batch-id BATCH_ID
```

The incremental research runner reuses existing case context, fetches public sources
into a private batch cache, asks Jev what changed, generates provisional GLM notes,
validates exact citations, and checks grounding with Jev. Start with a bounded sample:

```sh
python3 scripts/research_flow.py run --batch-id BATCH_ID --limit 12 --workers 4
python3 scripts/research_flow.py report --batch-id BATCH_ID
# Once the sample is reviewed, expand the persisted selection:
python3 scripts/research_flow.py extend --batch-id BATCH_ID --limit 0
python3 scripts/research_flow.py run --batch-id BATCH_ID --limit 0 --workers 4
```

`run` makes paid Jev and GLM calls and fetches unauthenticated public source text.
Completed request hashes are reused. `--refresh` re-fetches sources while preserving
old versions; changed evidence invalidates draft and grounding checks. Failed or
uncertain model calls are not retried automatically. Local repairs only restore
unambiguous exact citation references, source whitespace, or JSON framing; trailing
writer prose stays flagged for review. Every message remains in a private routine or
exception queue. Media, inaccessible sources, unsupported claims and uncalibrated
model judgments never become automatic verification or publication. Review approved
changes in `resource-pool/cases.tsv`, then rebuild with `scripts/consolidate.py` and
run the public-content checks before deployment.

`run` sends the staged text and available context to Jev and incurs API usage. Overlap rows are included for review; request/token limits may leave work pending. Cached successful batches are reused on another run with the same batch ID. Predictions remain unverified review suggestions. Collection and triage neither promote sources nor rebuild, deploy or change the public knowledge base. Review the private receipt and queue before promoting a snapshot.

## Prebuild case examples

`python3 scripts/case_designs.py --workers 3` prepares missing teaching designs from the sanitized public catalog with GLM. Private receipts in `research/case-designs/` preserve model usage and source fingerprints. Existing current designs are reused. Explicit rate-limit rejections back off; uncertain network failures are not automatically retried. `--retry-failed` explicitly retries failed attempts. Interruptions drain the current batch before stopping.

`python3 scripts/check_case_requests.py` optionally sends the two sample requests per prepared case to Jev, caches private results, and reports differences from illustrative expectations. It executes no application actions. Agreement on authored examples is not a quality benchmark. Review discrepancies before publishing.

Run `python3 scripts/export_public.py` to export validated examples to `docs/case-designs.json`. Changed source records invalidate their examples; deployment requires complete, current coverage. Generated JSON is separate from the factual Markdown knowledge corpus. No new source collection is performed by these commands.
