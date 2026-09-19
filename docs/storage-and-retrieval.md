# Storage and retrieval design

The resource pool is a collection, not one large document. Markdown is the authored knowledge format. The original Discord capture is a separate evidence archive. S3 is an optional storage backend; it does not itself decide which passages answer a user's idea.

## Layout

| Layer | Contents | Used directly by the chatbot? |
|---|---|---|
| Knowledge reference | Official capabilities, primitives, limits, integration boundaries | Yes |
| Curated use cases | One project per Markdown file; what, how, why, impact, caveats, sources | Yes, with evidence labels |
| Pattern guides | Reusable ways to compose decisions, generation and deterministic code | Yes; clearly labeled analysis |
| Source register | Original links, message IDs, access status and review status | For citations and coverage checks |
| Raw capture | Discord text, link metadata and collection cutoff | Research only; not authoritative product facts |
| Pending/excluded material | Plans, unrelated promotions, insufficient detail | Excluded from default recommendations |

Keep stable project IDs and source URLs. Multiple posts about the same project become updates to one case, not separate apparent success stories. Record collection time separately from message time and external-page publication time.

## Optional S3 layout

```text
jev-resources/
  raw/discord/<channel-id>/<capture-date>.json
  sources/external-links.json
  curated/knowledge/jev-knowledge-reference.md
  curated/use-cases/<case-id>.md
  curated/patterns/<pattern-id>.md
  manifests/<revision>.json
```

This is a proposed layout, not a provisioned bucket. Keep the raw Discord archive private. Publish or share curated summaries separately only when that audience and scope are chosen. Store credentials outside the corpus. An upload requires a destination bucket/account and suitable access; no S3 resources or uploads have been created in this task.

Local storage is sufficient for this capture. Adding S3 later need not change the Markdown structure. A manifest can associate each file with its hash, revision, evidence status and retrieval eligibility.

## Jev-bot retrieval

1. Extract the user's domain, available state, decisions, action space, frequency, latency target and cost of mistakes. Ask only for missing information that changes the recommendation.
2. Retrieve capability passages and candidate cases using local full-text search or a search index. Filter out plans and unsupported integration claims.
3. Optionally use Jev to score candidate relevance and choose applicable patterns. Supply the candidate text and IDs; preserve a none-of-the-above path.
4. A generative model writes the explanation and integration sketch. Jev supplies typed judgments; it is not the conversational prose generator.
5. Cite source-backed facts. Label proposed architecture and expected impact as analysis. Show what still needs a workload-specific evaluation.

Raw archive text is untrusted source material. Never treat embedded instructions, install commands or promotional claims as chatbot instructions. Source presence is not verification; an accessible repository is not proof that its tests pass or that its reported savings generalize.

## Completion criteria for an exhaustive snapshot

- Reach the channel's visible beginning and record a fixed latest-message cutoff.
- Reconcile captured message IDs and thread counts; identify deletions, inaccessible history and virtualized-content gaps.
- Inventory substantive external links, deduplicate aliases, inspect accessible destinations and record actual failures.
- Review meaningful thread replies and corrections.
- Identify attachment-only evidence that has not been transcribed or inspected.
- Give each substantive project a case or an explicit pending/excluded reason.
- Verify all local links and make curated counts reproducible.

An exhaustive main-channel scroll is only one of these checks. Do not label the whole resource pool exhaustive while the remaining checks are incomplete.
