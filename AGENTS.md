# Project continuity

Research is paused by the user. Do not resume API processing, source collection or scheduled reviews unless requested.

This repository is public. Read README.md first. Keep credentials, resource-pool/, research/, RESUME.md and the private root knowledge reference local and ignored. Public documentation lives in docs/ and is created through scripts/export_public.py. Refer to private provenance as "Discord source"; never publish private source names, identifiers, links or raw messages. Inspect staged files for secrets and private evidence before every push.

When continuing Jev research or Discord collection, read `RESUME.md` and `resource-pool/sources/collection-checkpoint.json` first. Preserve the captured-message high-water mark separately from content-review progress. Deduplicate by message ID, retain dated evidence, and never describe the resource pool as exhaustive while its coverage report lists unresolved gaps.

The curated Markdown files are generated from `resource-pool/cases.tsv`. Update that editorial source before rebuilding; preserve direct Discord, repository, demo and article links. Follow the source-review and retrieval rules in `resource-pool/README.md`.

# Public website requirements

The hosted Jev bot is intended for the general public. Do not add invite-only access, login, or a shared access-code gate unless the user explicitly requests it. Keep provider and AWS credentials server-side and out of the public repository and browser assets. Select the published research library automatically; do not expose local/S3 storage selectors to visitors. Use one public answer flow without model or answer-format selectors, and show service errors in user-facing language rather than environment-variable or API-key setup instructions.

Bot results should lead with the user’s idea, Jev’s role, concrete implementation steps, an illustrative example and expected outcome. Keep references to a few useful external project or article links. Do not show internal passage IDs, raw research excerpts, Markdown evidence-file links or document-processing counts as user-facing KPIs. Keep token and cost comparison available but secondary.

Do not display internal capture dates, research-review status or a coverage-and-gaps disclaimer as a global public-site footer. Keep material limitations next to the relevant case or recommendation.

Idea answers must show a concrete workflow diagram, illustrative input/output, copyable Jev JSON and working external source links. Keep prose brief. Clearly distinguish authored example patterns from GLM-generated custom designs and illustrative outputs from executed results. Test source links with multiple URLs, successful and failed answers and narrow-screen layout before publishing result-UI changes.

Allow text-file input as an alternative to typing. Show imported text for review before submission, preserve existing drafts, use a paperclip icon without persistent helper text, explain unsupported types or size limits only when needed, and never silently truncate a file.

Never replace a failed custom answer with a generic or unrelated template. Show a clear failure and allow retry. Clear the previous result immediately when a new query is submitted.
