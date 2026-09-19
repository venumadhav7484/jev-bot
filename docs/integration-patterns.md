# Reusable Jev integration patterns

Editorial synthesis of the linked cases. These are design patterns and evaluation starting points, not vendor guarantees or independently reproduced outcomes.

| User's need | Jev's bounded job | Work outside Jev | Examples |
|---|---|---|---|
| Triage messages or documents | Category, urgency, relevance, ordered priority | Ingestion, permissions, routing policy, human review | [Forum-to-issues](use-cases/forum-to-issues.md), [GitLab triage](use-cases/gitlab-triage.md), [document profiles](use-cases/document-profile.md) |
| Reduce context before a larger model | Score candidate files, passages or tool descriptions | Candidate retrieval, recall checks, context assembly | [Relevant files](use-cases/task-file-filter.md), [MCP gateway](use-cases/mcp-gateway.md), [reranking](use-cases/reranking-benchmark.md) |
| Check generated work | Judge explicit claims or rules | Generation, deterministic tests, revision limits | [Wellposed](use-cases/wellposed.md), [breaking changes](use-cases/breaking-change-cascade.md), [comment loop](use-cases/comment-rewrite-loop.md) |
| React to ongoing speech | Score transcript against topics or conditions | Audio capture, speech recognition, UI | [Intelliprompter](use-cases/intelliprompter.md), [drive-through](use-cases/drive-through.md) |
| Control a browser or game | Select a legal action and candidate target | Perception, current-state capture, execution, permissions | [Browser Use](use-cases/browser-use.md), [Mario memory](use-cases/mario-memory.md), [OpenRA](use-cases/openra.md) |
| Build UI from a design system | Choose components and bounded arguments | Component library, rendering, optional copy generation | [Saypage](use-cases/saypage.md), [separate-copy UI](use-cases/component-copy-ui.md) |
| Route among tools or models | Select a suitable option; assess uncertainty | Registry, credentials, execution, fallback and budget | [Jot](use-cases/jot.md), [RouteKit](use-cases/routekit.md), [AILANG](use-cases/ailang.md) |
| Judge visual material | Evaluate textual/structured observations | Vision model, OCR, video segmentation | [Ad shots](use-cases/ad-shot-review.md), [SDE vision cascade](use-cases/sde-vision-cascade.md) |

## What the examples do not establish

- A valid Choice answer is not necessarily the right action. Candidate generation and state quality are part of the system. OpenRA's first refinery placement was poor despite low latency.
- A model probability does not authorize a side effect. Approval, hard bans, access control and execution validation belong to the application. Pi-heed's reported shadow/fail-open behavior is advisory, not a hard security boundary.
- Repeated feedback in game state is not evidence of model-weight training. Track what the harness actually remembers and updates.
- Generated prose, source code, images and speech can appear in a Jev-powered application because other components produce them. Record those components explicitly.
- A cheaper call does not always improve the workflow. [Empryo](use-cases/empryo.md) rejected some integrations after evaluation; [co-DM](use-cases/co-dm.md) found an art-classification baseline that beat the model.
- Dataset composition, schema wording and class prevalence matter. [Norwegian documents](use-cases/norwegian-hearing.md), [adversarial advisory cases](use-cases/advisory-adversarial.md) and [bilingual email](use-cases/bilingual-email.md) illustrate different evaluation limitations.

## Minimal evaluation before recommending automation

Define the decision and an explicit abstain/escalate path. Compare against existing code or a simple baseline on human-reviewed examples, including hard negatives and missing context. Measure precision/recall where relevant, calibration, retained coverage, complete-workflow latency and cost. Repeat identical requests and perturb labels/order separately. Freeze the model version, question schema, preprocessing and decision policy. Evaluate side effects and recovery separately from model accuracy.

For a new domain, cite an analogous case as precedent for an architecture, not proof of expected savings or accuracy.
