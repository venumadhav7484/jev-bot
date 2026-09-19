# Jev-bot

A local evidence assistant for one question:

> Describe your use case or idea. Where could Jev help, what else would you need, and what are the limits?

The assistant proposes a bounded integration, retrieves related implementations and counterexamples, and preserves source links and limitations. It uses authored designs and attributed case extracts. Optional Jev Choice classifies the entered idea; no generative answer model is configured.

## Try it

Python 3.10+; standard library only. No key needed for offline mode.

```sh
git clone https://github.com/venumadhav7484/jev-bot.git
cd jev-bot
python3 scripts/serve_bot.py
```

Open **http://127.0.0.1:8765**. Describe an idea, or try the su-lekha example. Add details to the description to refine the result. No conversation history is saved. The server binds to loopback and serves only public assets; it is not a hosted production service.

For optional Jev routing, put `jev_api_key` in local `.env.local`, then select the checkbox in the interface. Only the entered idea goes to TypeSafe. API usage applies. If the service fails, the interface reports a fallback to local keyword routing.

```sh
python3 scripts/jev_bot.py "Route incoming invoices to the right queue"
python3 scripts/jev_bot.py "Monitor sensitive information in AI applications" --jev
python3 -m unittest discover -s tests -v
```

## Frozen snapshot

New source collection is paused at the boundary below. The exact last-post link and thread cursors are retained privately, so a later pass can resume with overlap and deduplication. Scheduled X reviews remain paused.

<!-- SNAPSHOT-START -->
| Layer | Frozen snapshot |
|---|---|
| Capture cutoff | 19 September 2026, 10:08:31 IST |
| Messages | 3,358 unique IDs; all editorially accounted for |
| Cases | 440; 361 default eligible, 79 held back |
| External evidence | 837 URLs; 0 await first disposition; 206 retain content gaps |
| Media | 174 / 413 attachments inspected |
| Bot | Local preview; 11 authored design families |
| S3 | Backup pending |

<!-- SNAPSHOT-END -->

**Accounting is not validation.** The catalog includes author reports, tools, proposals and counterexamples. Default eligibility does not mean independently verified. Metadata-only pages, context screening and text reviews with missing media remain distinct from substantive technical inspection. No community benchmark has been independently reproduced.

## Read the evidence

- [Capability reference](docs/jev-knowledge-reference.md): primitives, APIs, integration patterns and official sources.
- [Use-case catalog](docs/jev-usecases.md): what, how, why, reported impact, limitations and artifact links.
- [Community findings](docs/community-evidence-findings.md): strengths, failures, conflicting evidence and lessons.
- [Answer guide and su-lekha proposal](docs/jev-bot-answer-guide.md).
- [Completion status](docs/completion-status.md) and [aggregate metrics](docs/metrics.json).
- [Snapshot and update workflow](docs/system-workflow.md).
- [Cached-source grounding pilot](docs/source-grounding-pilot.md): measured API usage, citation checks and review limits.
- [Local media processing](docs/media-processing.md): frame extraction, local speech transcription, OCR and editorial review boundaries.
- [Development checks](docs/development-checks.json): authored scenarios and a live API smoke test, with scope limits.

The first assistant covers 11 authored design families: policy review, routing, semantic data filtering, media pipelines, bounded action selection, memory, evaluation, exact computation, financial evidence, clinical documents and generation boundaries. It can miss novel fits; the full catalog remains available for research. Related cases are analogies, not evidence that a new design will work. Development tests do not establish general answer accuracy.

## How Jev is used

The research pipeline used Choice to categorize contributions and their relationship to Jev, with independent Noul questions for evidence dimensions. All model suggestions remain subject to editorial review. The bot optionally uses one Choice question to map an idea to an authored integration family. Application code performs retrieval, applies evidence policy and assembles the response. [TypeSafe primitives](https://docs.typesafe.ai/primitives).

## Repository layout

```text
docs/                       Sanitized public evidence and bot snapshot
web/                        Local assistant interface
scripts/jev_bot.py          Idea routing and evidence-backed design briefs
scripts/serve_bot.py        Loopback-only web server
scripts/consolidate.py      Offline private-to-public snapshot rebuild
scripts/stage_capture.py    New/edited-message intake; no automatic collection
scripts/evidence.py         Private SQLite evidence search
scripts/jev_triage.py       Resumable Jev-assisted research triage
scripts/backup_private.py   Private S3 snapshot and download verification
tests/                     Boundary, retrieval, intake and response checks
```

## Private research and backups

Public docs identify private provenance as **Discord source**. Raw messages, source identifiers and links, private artifacts, credentials, local databases and API caches remain ignored. Public repository, demo, article and official-documentation links remain in the case write-ups.

Research rebuild and incremental intake require the authorized local `resource-pool/`, `research/`, `RESUME.md` and root knowledge reference; these are not shipped in this public repository. `scripts/consolidate.py` regenerates curated Markdown, search indexes, completion reports and sanitized public exports offline. It does not call Jev or collect new posts.

S3 backup uses credentials from `.env.local`, creates an account-owned private bucket, blocks public access, enables encryption and versioning, and verifies downloaded archive and individual file hashes. Environment files and detected credentials are excluded. Bucket names, object keys and receipts remain local. Storage and transfer charges may apply. This backs up evidence; it does not host the bot.

Never blindly stage private builder output. Use the allowlisted exporter, inspect public changes and run `python3 scripts/check_public.py --staged` before every push. The guard checks loaded local credential values and private provenance; it is not a complete secret detector. `.gitignore` alone is not a publication review.
