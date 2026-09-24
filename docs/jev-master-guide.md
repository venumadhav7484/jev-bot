# Jev master guide: capabilities, field lessons and effective use

**Consolidated:** 24 September 2026. **Main-channel evidence boundary:** 24 September 2026 at 10:59:08 UTC, within the fixed collection window ending 11:03:05 UTC. All previously known thread cursors and twelve newly discovered threads were revisited in this update; undiscovered threads and arbitrary older edits remain outside verified coverage. Official interface and pricing statements below retain their dated review scope.

This is the main practical synthesis of this project's Jev research: what Jev does, where it appears useful, where attempts fail, how to build around it, and how to judge claims. It brings together the technical reference, community cases, corrections, inspected artifacts and our own pipeline experiments. Case links preserve supporting repositories, demos, articles and public posts; private provenance stays local.

**Coverage is substantial, but incomplete.** The catalog contains 510 write-ups, including tools and counterexamples; 421 are default eligible and 89 held back. The captured corpus contains 5,183 unique message IDs. Editorial accounting includes first-pass discussion and unresolved-source dispositions; it is not full claim verification. The September 24 update adds unreviewed sources and media to the earlier backlog. Scoped text reviews do not cover every embedded video or nested document. No community benchmark has been independently reproduced. [Current source and media counts](completion-status.md).

**New field lessons:** batching can change margins; lexical search can beat semantic ranking; workflow design can matter more than a model swap; extra agent stages can increase total cost; and checking hostile instructions is different from checking poisoned evidence. Read the [September 24 synthesis](incremental-findings.md#24-september-2026-new-evidence-and-corrections) for the supporting cases and their limits.

## Guide map

- [Capabilities and boundaries](#1-what-jev-isand-which-part-of-an-application-it-supplies), [primitives](#2-use-the-primitives-correctly) and [useful patterns](#3-where-the-evidence-suggests-useful-applications).
- [Failures and counterexamples](#4-what-fails-what-underperforms-and-why), [implementation method](#5-how-to-build-an-effective-jev-integration) and [evaluation](#6-evaluate-the-claim-not-the-appearance-of-a-demo).
- [Tools and interfaces](#7-interfaces-tools-and-surrounding-infrastructure), [cost and privacy](#8-cost-latency-and-privacy-assess-the-whole-system) and [su-lekha](#9-worked-proposal-su-lekha).
- [Our own experiments](#10-what-our-own-use-of-jev-taught-us), [bot recommendation rules](#11-rules-for-recommendations-based-on-this-knowledge) and [remaining unknowns](#12-what-remains-unknown-and-how-this-guide-should-evolve).

## 1. What Jev is—and which part of an application it supplies

Jev evaluates supplied text or structured state against bounded questions. Its reviewed interface returns typed judgments: a choice among supplied alternatives, a score over ordered levels, or the probability that a proposition is true. It is useful to think of it as a semantic decision component inside an application.

The application still acquires evidence, builds state, defines eligible actions, retains memory, enforces permissions and executes actions. A separate generative model is needed when the design requires arbitrary prose, code or novel action arguments. Images, audio and video require upstream perception or transcription in the reviewed interface. Supplying an image's filename, encoded length or a video's caption does not establish visual understanding. [Official primitives](https://docs.typesafe.ai/primitives), [state](https://docs.typesafe.ai/concepts/state), [misleading robotics vision claim](use-cases/scripted-robotics-vision-claim.md).

| Need | Suitable component and boundary |
|---|---|
| Semantic classification, relevance or finite routing | Jev is a candidate; test against rules and existing classifiers. |
| Exact arithmetic, matching IDs, legal moves or schema checks | Deterministic code. Jev may select among validated candidates. |
| Search, current facts or document acquisition | Retrieval and connectors first; Jev judges the supplied evidence. |
| Images, speech or screen understanding | OCR, vision, ASR or DOM extraction first; preserve extraction uncertainty. |
| Free-form explanation, code or new text | A generative model or authored templates; Jev may route or evaluate. |
| Memory and changing environment state | Application storage and state updates; include relevant history explicitly. |
| Authorization, payment, deletion or physical actuation | Application controls and execution; a probability is not permission. |

“System One” describes the vendor's positioning for fast judgments. It does not establish that every task is fast enough, that confidence proves truth, or that general reasoning and autonomous execution are supplied. The [technical reference](jev-knowledge-reference.md) contains the fuller architecture, API and historical source discussion.

## 2. Use the primitives correctly

| Primitive | Reviewed behavior | Effective use | Common mistake |
|---|---|---|---|
| **Choice** | Selects among supplied alternatives and exposes a probability distribution; documented maximum 255 alternatives. | Mutually exclusive routes, eligible actions, categories or candidate selection. Include an unresolved option where needed. | Forcing a choice when the answer is missing; treating the selected label as verified truth. |
| **Score** | Evaluates 2–10 ordered levels and returns an expected zero-based index, which can be fractional. | A named rubric with concrete levels; ranking and prioritization when the rubric is appropriate. | Treating it as exact measurement, an arbitrary numeric extractor or a probability of success. |
| **Noul** | Returns a yes probability from 0 to 1; no separate confidence field. | Independent predicates, evidence checks and multi-label properties. | Reading 0.5 as medium business severity, or high probability as certainty. |

State may be text or structured JSON. Question identifiers are bookkeeping; express meaning in the question's instructions and criteria. Ask separate predicates when several properties may be true at once. For dependent decisions, use stages: later questions cannot rely on earlier answers that were not supplied in state. [Primitive definitions](https://docs.typesafe.ai/primitives), [advanced usage](https://docs.typesafe.ai/primitives/advanced).

Confidence is a model output. Calibration is a measured relationship across a population of predictions and outcomes. A score of 0.99 does not prove this answer is correct, and a trading classification's confidence is not the probability of profit. Choose thresholds against error costs and labeled workload data rather than adopting one universal cutoff. [Confidence documentation](https://docs.typesafe.ai/confidence), [riddle counterexamples](use-cases/riddle-probes.md), [trading interpretation](use-cases/reactor-trading-interpretation.md).

## 3. Where the evidence suggests useful applications

These are transferable patterns supported by inspected material or attributed reports, not guaranteed wins. “Impact” is often a demonstrated workflow or an author's measurement; deployment and business outcomes remain separate questions.

| Pattern | What Jev contributes; what code or other models do | Evidence and practical lesson |
|---|---|---|
| Triage and routing | Classify intent, exception type or review need; code preserves queues, policies and audit records. | [Payment exception triage](use-cases/payment-exception-triage.md) demonstrates a synthetic review flow, not a real payment authorization system. |
| Semantic matching with exact constraints | Judge candidate meaning; code verifies amounts, currency and identifiers. | [Payment reconciliation](use-cases/payment-reconciliation.md) leaves ambiguity unresolved rather than fabricating a match. |
| Document and citation review | Assess supplied passages against a claim or rubric; retrieval must first obtain the right passage. | [Citation support](use-cases/stll-citation-support.md) illustrates source-grounding checks. Agreement with a source does not prove that source is correct. |
| Cascades and escalation | Handle a narrow decision, then escalate uncertain or unsuitable work to another model or reviewer. | [Legal cascade](use-cases/stll-legal.md) and [case outcomes](use-cases/stll-case-outcome.md) suggest selective escalation; evaluation must count both mistakes and fallback costs. |
| Cheap gates before expensive review | Combine independent signals; preserve the old path on errors or uncertainty. | [Newsletter classification](use-cases/newsletter-classifier.md) keeps a printer quote in review through its counterparty label despite a low new-work score. Five examples and hypothetical skip rates do not establish production savings or safe false-negative rates. |
| Memory selection and context reduction | Rank or filter candidate context; storage retains source material and code reserves mandatory facts. | [ReadyBase](use-cases/readybase.md) and [bwmem](use-cases/bwmem.md) show why retained critical facts and recoverable dropped memories matter. |
| Semantic search and personalized views | Score content once, then let code filter, rank and display existing material. | [Personal Hacker News](use-cases/personal-hacker-news.md), [semantic relationships](use-cases/semantic-relationships.md) and [pi-detail](use-cases/pi-detail.md) illustrate useful interfaces without arbitrary text generation. |
| Dynamic interfaces | Select among registered surfaces or actions using current state. | [NoFlow](use-cases/noflow.md) changes a button's destination with state; this does not establish payment execution. |
| Speech-driven structured workflows | Judge a transcript and update structured actions; ASR hears speech, code maintains the cart. | [Drive-through](use-cases/drive-through.md) combines Parakeet transcription and a cart workflow. Transcription errors remain an upstream failure source. |
| Document transformation | Choose among known styles or conditional clauses; code edits the document and people confirm consequential changes. | [House style](use-cases/stll-house-style.md) separates generative style descriptions from per-paragraph choices; [conditional templates](use-cases/stll-conditional-template.md) preserve user confirmation. |
| Bounded agents and games | Choose valid actions from state; the host owns geometry, history and simulation. | [Football](use-cases/football-selfplay.md), [Wordle](use-cases/wordle-strategies.md) and [Things versus Stuff](use-cases/things-vs-stuff.md) show how action representation shapes behavior. |
| Developer tools | Rank files, filter findings or check a narrow condition while preserving source locations. | [Rust tsg](use-cases/rust-tsg.md) treats results as review starting points and discloses incomplete scans. |
| Moderation and quality gates | Evaluate several semantic properties; code combines them into an explicit policy. | [UGC classifier](use-cases/ugc-classifier.md) improved its rubric with deterministic grading floors. Its model-derived examples are not independent ground truth. |

The common strength is flexible semantic judgment over explicit context with a small output contract. The strongest integration argument is usually “replace or improve this bounded decision,” not “replace the entire workflow.”

## 4. What fails, what underperforms, and why

### Incomplete state and poor action choices

Jev cannot reliably act on facts the application omitted. Vampire Survivors missed obstacles absent from its state; Catan repeated rejected trades without adequate remembered context. A NetHack run was limited by a state-advance bug. Whole-word Wordle choices worked better than independent letter decisions; football improved after reachable passing options and catch-facing controls became available. These are application and representation failures as well as model-evaluation lessons. [Vampire Survivors](use-cases/vampire-survivors.md), [Catan](use-cases/catan-selfplay.md), [NetHack](use-cases/jev-nethack.md), [Wordle](use-cases/wordle-strategies.md), [football](use-cases/football-selfplay.md).

**Design response:** make relevant state observable, track rejected actions, include viable alternatives and validate actions before execution. Faster calls cannot repair missing state or an impossible action set.

### Confidence, prompt sensitivity and conflicting answers

Inspected riddle screenshots include a confidently wrong date calculation and a modified surgeon riddle answered against its explicit wording. A schema-sensitivity report describes changes with labels, order and primitive choice. The MMO experiment found that replacing a Noul decision with Choice changed behavior, while some edge cases remained. EVE commander judgments could disagree about danger and tactical posture. These examples do not quantify universal error rates, but they refute confidence-as-proof and interchangeable-prompt assumptions. [Riddles](use-cases/riddle-probes.md), [schema sensitivity](use-cases/schema-sensitivity.md), [MMO evaluation](use-cases/npc-network-latency.md), [commander](use-cases/eve-commander.md).

**Design response:** version the entire question representation; test paraphrases, missing information and option order; check cross-field consistency; retain an uncertain or safe fallback.

### Vague checks and lost critical evidence

A clinical-document experiment's broad plausibility check missed seeded errors; explicit field comparisons and a “not stated” option found all 11 in that small synthetic set. This is a prompt-design observation, not evidence of clinical readiness. ReadyBase's plain reranking dropped structural-risk facts until code reserved critical material. [Clinical grounding](use-cases/clinical-document-grounding.md), [ReadyBase](use-cases/readybase.md).

**Design response:** ask whether a specific passage supports a specific claim. Preserve mandatory facts outside relevance ranking. Measure omission rates, not merely whether the selected text looks useful.

### More model calls without a better outcome

An OpenCode experiment became slower because an LLM still prepared Jev's state and actions. An offload pilot's relay approach was slower overall; code-owned skipping saved work but sometimes lost label agreement. A specialized fine-tuned Qwen classifier beat Jev on latency. Jev-Axi's small repeated comparison yielded conflicting cost effects, not a general saving. [OpenCode](use-cases/opencode-e2e-overhead.md), [offload pilot](use-cases/offload-bench.md), [specialized classifier](use-cases/internal-classifier-qwen.md), [Jev-Axi](use-cases/jev-axi.md).

**Design response:** compare complete workflows. Include preprocessing, connection setup, generation, retries, fallback and correction. A cheap call helps only when it removes enough work or improves outcomes.

Adoption can correctly end with keeping the baseline. Empryo rejected three proposed Jev jobs; repairing its deterministic error-triage regex matched the reported 102/102 Jev result. The co-DM report's art classifier lost to an always-other baseline after prevalence adjustment. Its earlier best-run claims were withdrawn and a contaminated comparison discarded. These are valuable negative results, not failures to find a sufficiently clever prompt. [Empryo](use-cases/empryo.md), [co-DM](use-cases/co-dm.md).

### Tight control loops and misleading latency comparisons

The MMO author's original 553 ms median included fresh TCP/TLS connections on every call. A small persistent-connection sample reported a 220–225 ms warm floor and 265 ms median including a cold call. It still missed that project's 50 ms tick budget, and the project required self-hosting. Commander reports supported 1–2 Hz but missed 5–10 Hz deadlines. These are workload reports, not universal service latency. [MMO](use-cases/npc-network-latency.md), [commander](use-cases/eve-commander.md).

**Design response:** reuse connections, measure cold and warm paths separately, set deadlines, reject stale actions and decouple model decisions from faster deterministic control loops.

### Exact reasoning, unrestricted generation and perception

Early ChatJev experiments produced blanks or repetition and used many decision calls for short text. This is not native efficient prose generation. SAT screenshots are not proofs; a solver remains responsible for exact validity. Browser and robotics demos commonly rely on DOM, OCR, another model or a controller. One inspected robotics repository supplied step-indexed hints and preset actions while claiming raw-image reasoning; its code did not establish that capability. [ChatJev](use-cases/chatjev-early.md), [SAT advisory](use-cases/sat-unsat-advisory.md), [browser pipeline](use-cases/browser-use.md), [robotics claim correction](use-cases/scripted-robotics-vision-claim.md).

**Design response:** keep generation, perception and exact computation in components that supply them. A successful combined application is not proof that Jev performs every component's job.

### Detection without enforcement, and forecasts without outcomes

Pi-heed retained a webhook side effect despite a high-concern judgment. Jev-Axi's guard behavior was fail-open unless it received a deny. A moderation demo left some suspected messages visible. Trading reports include unbacktested signals, dry-run evidence conflicting with real-order claims, and explicit “no real money yet” qualifications. [Pi-heed](use-cases/pi-heed.md), [Jev-Axi](use-cases/jev-axi.md), [moderation](use-cases/scam-message-moderation.md), [news signals](use-cases/news-market-signal.md), [Kuru trading](use-cases/monad-kuru-trading.md), [crypto terminal](use-cases/crypto-intelligence-terminal.md).

**Design response:** implement enforcement separately, test error paths and preserve operational status. Concern detection is not prevention; plausible signals are not validated forecasts or returns.

Security performance can also change when an attacker adapts. The trusted-monitor pilot reported weaker backdoor detection after attackers could choose among variants; additional deployment context improved a separate injection benchmark. Pi-Warden reduced recorded policy violations without improving task completion in its matched sample. Evaluate adversarial behavior and completion together, not only favorable aggregate detector scores. [Adaptive monitor](use-cases/ai-control-monitor.md), [injection benchmark](use-cases/jev-sec-bench.md), [Pi-Warden](use-cases/pi-warden.md).

### Apparent failures that need correction before becoming lessons

The strawberry-count caption called a result wrong, but the inspected screenshot ranked the correct answer first at 56%; a different prompt later did produce a wrong count. An urgency example still said “ASAP,” which complicates its claimed negative label. A game's failed request was traced to a missing API key rather than a demonstrated judgment error. Retain failures and recoveries with exact conditions instead of repeating either headline. [Counting probes](use-cases/riddle-probes.md), [urgency wording](use-cases/urgency-wording.md), [game repair](use-cases/politician-game.md).

### Additional lessons from the deeper media and code review

The next evidence pass sharpened several practical boundaries. These are observations from source inspection and sampled recordings, not reproduced benchmarks.

| Finding | What to do with it | Supporting case |
|---|---|---|
| A local victory can hide a continuation failure. Final Fantasy wins a battle, then pauses because recovery routing is missing; Sonic advances, then repeats host recovery. | Test complete episodes, recovery and stale-state handling, not only impressive intermediate moves. | [Final Fantasy](use-cases/final-fantasy.md), [Sonic](use-cases/sonic-controller.md), [maze repetition](use-cases/maze-failure.md). |
| A supposedly safe fallback can be stale. The inspected EVE controller returns its previous command on an error/empty answer without rechecking current targets or capacity on that path. | Revalidate fallback commands against current state and permissions; retaining the last answer is not automatically safe. | [EVE commander](use-cases/eve-commander.md). |
| A bounded question gate is not a tool sandbox. Deepseek auto-mode has a decision budget but documents full tool access without an approval boundary. | Enforce permissions at the execution layer and test bypass paths. | [Deepseek auto-mode](use-cases/deepseek-auto.md). |
| More iterations can degrade output while accumulating cost. The pixel-refinement recording breaks a coherent region into fragments while its token counter grows to roughly 42 million. | Track quality and total spend per accepted result; add rollback, stopping criteria and a deterministic baseline. | [Iterative pixels](use-cases/iterative-pixels.md). |
| Benchmarks may compare different amounts of work. Pixel Race completes 4,047 Jev pixel choices but extrapolates Haiku runtime from a 300-pixel sample. | Preserve measured versus projected labels and both accuracy denominators. | [Pixel comparison](use-cases/jeroen-pixel-drawing.md). |
| Classifier output is not classifier accuracy. A failure-taxonomy dashboard's roughly 83% means model-assessed task success; two sessions failed classification. | Obtain independent outcome labels, count failures and separate retrieval time from batch throughput. | [Agent failure taxonomy](use-cases/agent-failure-taxonomy.md). |
| Host computation often supplies most of the solution. Parallel Wordle finishes many known answers without another Jev call; a Rubik recording does not expose a per-move Jev decision trace. | Attribute candidate elimination, exact solving and execution to the host where supported; measure incremental value. | [Parallel Wordle](use-cases/multi-wordle.md), [Rubik](use-cases/rubik-move-selection.md). |
| Fast cached reranking is useful but differs from fresh inference. SQL reruns use stored row probabilities; feed sliders use cached semantic scores. | Include state, condition, model and question version in cache keys, and report warm/cold paths separately. | [Semantic SQL](use-cases/pgjev.md), [personal feed](use-cases/personal-hacker-news.md). |
| A rich demo may use fixtures. Clinical dashboard metrics are explicitly simulated, keyboard weather/place data are samples, and Textured's initial sound is hand-tuned. | Do not turn attractive UI content into measured impact or demonstrated model quality. | [CLINIRISE](use-cases/clinirise.md), [keyboard](use-cases/jevin-keyboard.md), [Textured](use-cases/textured.md). |
| Artistic instructions are soft judgments. The VJ clip's dark/minimal brief still leads to bright multicolor output. | Put strict constraints in rendering code; use Jev for selection within those constraints. | [VJ director](use-cases/vj-director.md). |
| UI help can combine semantics with ordinary controls. Clippy shows model-triggered nudges, deterministic validation, dismissal and cooldowns. | Measure false interventions and completion improvements; hesitation alone is not evidence of confusion. | [Clippy](use-cases/clippy.md). |
| Unknown intent can improve authored content. The text-adventure wrapper retains catchall interactions for future event design. | Use abstention as a feedback queue; offline event tests do not validate live language judgments. | [Text adventure](use-cases/text-adventure-intent.md). |

A wrapper that converts distance from 0.5 into a field named `sure` has changed presentation, not established calibration. The inspected [Rust wrapper](https://gitlab.com/porky11/jev) illustrates why field names and transformations need reading before using confidence operationally.

The creative opportunity is often **text to bounded controls**: synth parameters, existing UI components, navigation destinations or legal game actions. Textured explicitly separates TypeSafe interpretation from browser Web Audio synthesis. This gives flexible interfaces without claiming native audio or arbitrary UI generation. [Textured](use-cases/textured.md), [json-render](use-cases/json-render.md), [visitor routing](use-cases/visitor-page-routing.md).

### Corrections from the completed external-review pass

The following findings come from inspected recordings, original posts, code or rendered applications. Review scopes vary: some clips were inspected across all sampled frames, while longer recordings used claim-focused opening, middle and ending samples. None is an independently reproduced benchmark.

| Evidence and limitation | Practical lesson | Sources |
|---|---|---|
| BTD6's author claims a CHIMPS win on attempt 38, but the attached recording ends with **DEFEAT, ROUND 95**. A source reply describes legal actions, detailed mod state and death logs supplied to subsequent runs. | Preserve the contradiction. Do not claim a verified win, model-weight learning or superiority over another model. Ten state updates per second and roughly 0.3-second choices are different rates. | [BTD6](use-cases/btd6.md). |
| The Pokémon recording explicitly combines retained Elite Four wins rather than an uninterrupted campaign. Its final card reports 403,287 input tokens and $0.0233 at $0.042/million; input-only arithmetic gives about $0.01694. | Label edited successes and unresolved billing arithmetic. Computed damage/type information belongs to the harness, and action preferences are not win probabilities. | [Pokémon campaign](use-cases/pokemon-run.md). |
| Cloaked reports **74.3% → 96.6%** as an equal-weight average over 526 scored pages, while field totals imply **44.7% → 98.8%** across 4,831 controls. The corpus has 84 original fixtures plus 480 authored scenarios; displayed median full API response is 213 ms. | Preserve denominators and aggregation. Neither metric establishes production or adversarial accuracy. | [Form classification](use-cases/cloaked-fields.md). |
| Flappy Bird reaches 97 before losing and restarting; its harness supplies lookahead, candidate pruning and safety flaps. Recorded HUD shows 13 safety saves, and a request timeout appears around restart. | Compare against the same deterministic harness without Jev. Evaluate latency spikes, overrides and full score distributions. | [Flappy Bird](use-cases/flappy-bird.md). |
| Farmer gameplay repeats an inventory-full warning without recovery; piano output becomes dominated by repeated E4 despite prior-note context. | Add explicit state transitions, escape conditions and repetition checks. Suggested MIDI-section selection remains an untested alternative, not a demonstrated fix. | [Farmer](use-cases/farmer-roleplay.md), [piano](use-cases/piano-limits.md). |
| The café simulation ends with 92 coffees and 81% happy customers but a **$308 net cash loss**. Paper-trading screenshot shows a **$17.48 simulated gain**, not realized trading profit. | Keep satisfaction, revenue, net outcome and deployment status separate. A plausible strategy or attractive dashboard does not establish business impact. | [Café](use-cases/coffee-shop.md), [paper-trading source](https://x.com/karuri945/status/2100562714376454654). |
| Greenwash demonstrates narrow changed-hunk checks for skipped tests, weakened assertions and swallowed errors. Its displayed 98–99% values are model judgments, not measured precision or recall. | Semantic checks complement deterministic regression tests and whole-program context. Measure misses as well as flags. | [Greenwash](use-cases/greenwash.md). |
| Physical-arm footage shows motion but lacks a visible task instruction, API trace and trial denominator. A separate SO-101 project uses external vision and staged controllers. | Attribute perception, orchestration and motion separately; a moving gripper does not prove successful autonomous task completion. | [Physical arm](use-cases/physical-robot-arm.md), [SO-101](use-cases/robot-arm.md). |
| The redaction post's actual attachments are two still images with per-word Noul questions and an explicit redact/keep policy. The extractor had selected a quoted failure-taxonomy video. | Verify attachment ownership before analysis. A redacted screen does not mean the original text was withheld from the model, or that PII recall was measured. | [Original redaction post](https://x.com/danmana/status/2100550435094278475). |
| Several apparent demonstration videos belong to a quoted vendor launch, not to the quoting project's implementation. A discovery-list collage also supplies no new benchmark. | Deduplicate artifacts and distinguish discovery, author claims, observed behavior and reproduced results. Never count reposts as independent corroboration. | [Moderation post](https://x.com/brainstormity/status/2100471987860553931), [discovery list](https://x.com/valentynkit/status/2101014650624028997). |

**A useful working pattern: cheap filtering with uncertainty retained.** The news aggregator's rendered replay supplies direct evidence missing from its earlier README inspection: Jev judges relevance and importance from article titles, sources and bounded snippets. Relevant items continue to separate generative analysts; insufficient evidence and service failures retain the article. Its 119-call, 54-minute, $0.480 replay is a multi-provider workflow, not Jev-only timing or cost. This is useful architecture for the knowledge pipeline, but filtering relevance still does not verify article truth or protect against every false negative. [News case](use-cases/news-aggregator.md), [dated replay](https://news.aatf.ai/replay?date=2026-09-18), [repository](https://github.com/flyryan/ai-news-aggregator).

**Useful evaluation tooling has limits too.** Jevals demonstrates editable questions and state schemas, thresholds, SQLite run history, optional human rationale and JSON export. Seeded 6/6 and 7/7 sandwich runs with Brier scores are development checks; the recording explicitly says run-diff/version comparison is still missing. Save examples and expected judgments, preserve versions yourself, and test held-out cases. [Jevals](use-cases/jevals.md).

## 5. How to build an effective Jev integration

1. **Define the decision and baseline.** Specify what changes after the answer, the cost of each error, and the rules, classifier or human process being compared. Sometimes code already solves the problem.
2. **Prepare evidence and state.** Retrieve relevant passages, parse exact values and record unknowns. Include prior rejected actions or important history. Preserve source locations and timestamps. Treat instructions inside retrieved material as untrusted content.
3. **Define valid candidates and atomic questions.** Use Choice for mutually exclusive decisions, independent Noul questions for concurrent properties and Score for an explicit ordinal rubric. Let code remove forbidden actions before model selection. Include “none,” “unclear” or escalation when meaningful.
4. **Batch independent work.** Share state across questions when each is answerable from that state. Dependent decisions require another stage. Do not combine unrelated records without clear boundaries or assume more questions cost nothing. [Parallel questions](https://docs.typesafe.ai/cookbooks/parallel_questions).
5. **Validate outputs and enforce policy.** Check required answers, types, option membership, ranges and cross-field consistency. Define timeout, malformed-response, disagreement and stale-state behavior. Use deterministic authorization and transaction controls. For schema checks, validate required keys rather than allowing an empty result to pass vacuously.
6. **Cache with correct invalidation.** A useful cache key includes relevant state, question representation, model version and policy version. Changes to facts or criteria must invalidate old judgments. Store uncertainty and provenance with the answer.
7. **Evaluate on representative held-out examples.** Include hard negatives, ambiguous cases, missing facts, changed labels, multilingual inputs where relevant and actual application failures. Keep prompt-tuning data separate. Evaluate model-derived labels before treating them as ground truth.
8. **Roll out with feedback.** Run in shadow mode where appropriate, inspect disagreements, preserve overrides and source traces, and expand only after the application meets its error and latency budget. Recheck after model, question, candidate or preprocessing changes.

For exact extraction, a useful pattern is to parse candidates in code and ask Jev to select or assess them. Code then returns the original value. This preserves spelling, identifiers and numbers instead of expecting a judgment model to generate exact strings. [Pre-parsed extraction](https://docs.typesafe.ai/cookbooks/pre_parsed_value_extraction_cookbook).

## 6. Evaluate the claim, not the appearance of a demo

Keep four separate evidence labels: **documented interface**, **inspected artifact**, **author-reported result**, and **independently reproduced result**. A proposal is a fifth, different category. A video can demonstrate visible behavior without proving its architecture, general reliability or business impact. Repository inspection can reveal contradictions without reproducing performance.

Useful evaluation measures include precision and recall by error type, retained critical facts, abstention and escalation rates, calibration on labeled outcomes, task completion, p50/p95/p99 end-to-end latency, failure and retry rates, and total cost per useful result. Count timeouts and failed runs in the denominator. Report sample size, data selection, model version and workload.

Several case corrections explain why:

- [Near Here](use-cases/near-here.md) had encouraging development results, but an additional small comparison did not establish superior quality over every competing model. Latency or cost gains are separate claims.
- [Reranking benchmark](use-cases/reranking-benchmark.md) changes comparative conclusions with query versus dataset weighting; incomplete ground truth and truncation also limit interpretation.
- [Orgtools](use-cases/orgtools.md) used five unique examples repeated three times, not fifteen independent examples.
- [AILang](use-cases/ailang.md) used shadow evaluation and differing denominators with timeouts. Direct percentages can conceal that difference.
- [Kernel review](use-cases/kernel-vulnerability-review.md) produced alerts with many author-reported false positives, not a list of independently verified vulnerabilities.
- [Enron responsiveness](use-cases/enron-responsiveness.md) plots a 78-document cohort, not every processed document. [Document experiments](use-cases/document-lab-experiments.md) contain inconsistent denominators. Preserve those qualifications instead of merging unlike measurements.
- [Three-game chess report](use-cases/stockfish-three-game-report.md) cannot establish a chess rating, and other chess harnesses give different results. [Snake](use-cases/snake-limits.md) shows that faster calls can accompany worse task outcomes; [lemma selection](use-cases/lemma-selection.md) reports better ranking without yet being faster.
- [Construction grounding](use-cases/construction-source-grounding.md) and [Hedgehog](use-cases/hedgehog-proposed.md) described planned Jev integrations. They must not become success stories through summarization.

A source-support check asks whether supplied evidence supports a sentence. It does not establish that an implementation works, a benchmark is fair or the underlying source tells the truth. No model judgment or agreement between models closes that distinction.

## 7. Interfaces, tools and surrounding infrastructure

The reviewed direct interface uses `POST https://api.typesafe.ai/v1/systemone` with `model`, `state` and `questions`. The recorded model was `jev-1.13.0`; pin the version and retain the returned version and usage. Snapshot limits included a 64k total context budget and a 32k constraint on state plus the longest question. Limits and quotas need rechecking for the selected route and account before deployment. [API](https://docs.typesafe.ai/api), [models](https://docs.typesafe.ai/models).

| Layer | Tools seen in the research; interpretation |
|---|---|
| Direct integration | Python `typesafe_sdk.TypeSafeClient` and JavaScript `@typesafe-ai/sdk`; inspect the chosen SDK's request, retry and cancellation behavior. |
| Model frameworks and gateways | PydanticAI TypeSafe integration, Vercel AI Gateway and OpenRouter listings. Wrapper field mappings, supported outputs, billing, privacy and limits need route-specific checks; listings do not establish interface equivalence. |
| Search and developer utilities | Rust `tsg`, Jev-Axi and JevLint show integration possibilities. Review their failure policies and output contracts; they do not expand the model's native abilities. |
| Media preparation | Parakeet or other ASR, OCR, vision and browser DOM extraction. Our local pipeline also uses frame extraction, transcription and PDF tools before editorial review. |
| Document and action execution | DOCX editors, browser automation, game engines and robot controllers carry out work selected or reviewed by Jev. Check whether a showcased integration is released or still proposed. |
| Evidence and operations | Source storage, deduplication, timestamps, retrieval indexes, logs, caches and tests make the workflow traceable. S3 is storage, not model reasoning or bot hosting. |

See the [SDK and gateway reference](jev-knowledge-reference.md#9-access-sdks-skills-and-gateways), [PydanticAI documentation](https://pydantic.dev/docs/ai/models/typesafe/), [Vercel listing](https://vercel.com/ai-gateway/models/jev) and [OpenRouter listing](https://openrouter.ai/typesafe/jev-1.13). The reviewed sources did not establish user fine-tuning or LoRA support. Context adaptation does not mean model weights are being trained. English performance claims do not remove the need to evaluate other languages.

Retries and cancellation need operational care: the inspected [Elixir SDK](https://github.com/nshkrdotcom/typesafe_sdk) documents at-least-once retries and that local cancellation cannot undo remote processing. Bound concurrency, requests and retry costs. Application execution must be idempotent where a repeated decision could trigger repeated effects.

## 8. Cost, latency and privacy: assess the whole system

The published direct-API price recorded on 19 September was **$0.042 per million input tokens, with output free**. At that snapshot rate, 100 successful calls with 2,000 billed input tokens each cost **$0.0084**. This is arithmetic, not an account quote: recheck current pricing and the selected provider before committing. Retries, extra questions, long state and repeated calls change usage. [Pricing source](https://docs.typesafe.ai/models).

Total cost also includes retrieval, generative models, OCR/vision, transcription, hosting, storage, network traffic and human review. Savings require a useful replacement or avoided downstream work; adding a cheap extra call can still increase total cost and latency. Prefer measured billed tokens and complete-workflow timings to a model-only headline.

Data sent to Jev or a gateway leaves the local application. Review actual vendor and route terms, retention and account controls for the intended data. Do not infer zero retention or permission to process sensitive content from the model's architecture. Keep secrets out of state, logs and public exports; minimize inputs and enforce authorization in code. [Supplier boundaries](jev-knowledge-reference.md#19-privacy-retention-and-supplier-boundaries).

## 9. Worked proposal: su-lekha

**What:** help a team review authorized AI-application activity for sensitive information, policy exceptions and follow-up needs. This is an integration proposal, not an evaluated deployment.

**How:** acquisition code supplies an approved event or excerpt, destination, relevant policy and known capture gaps. Deterministic checks handle exact identifiers and access rules. Jev answers bounded questions about sensitivity, permitted purpose, urgency and review destination. The application combines these judgments with policy, preserves evidence passages and routes uncertain or consequential cases to a person. A template or separate generative model writes any narrative explanation.

**Why Jev might fit:** policy interpretation often requires semantic context beyond literal keyword matching, while the desired actions are bounded. The proposed value is better routing and reduced unnecessary review—not a blanket compliance guarantee.

**What remains outside Jev:** capture coverage, user identity, permissions, exact matching, storage, blocking controls and audit integrity. A confident judgment cannot establish that every event was captured, authorize a destination or prove legal compliance.

**Validation and impact:** compare against existing rules and human labels using authorized examples. Measure missed sensitive events, false escalations, retained critical evidence, reviewer time, latency and cost. Test absent context, quoted policy-violating text, adversarial instructions, changed destinations and timeout behavior. Include counterexamples from [ReadyBase](use-cases/readybase.md), [clinical grounding](use-cases/clinical-document-grounding.md) and [Pi-heed](use-cases/pi-heed.md). Full design context: [su-lekha reference](jev-knowledge-reference.md#20-example-use-case-su-lekha).

## 10. What our own use of Jev taught us

Jev-assisted triage produced suggestions for all 3,358 captured message IDs; the final prompt run recorded 420 successful calls. Editorial accounting remained separate. In a 13-item development sample, two relationship classifications mistook proposed adoption for an existing Jev integration. Those errors demonstrate why high-confidence model labels cannot replace reading the supporting source. [Local experiment](local-triage-experiment.md).

The 30-cached-source grounding pilot recorded 60 calls, 130 draft claims and 206,033 input tokens, with an estimated direct Jev charge of $0.008653386 at the snapshot rate. All 30 sources were flagged for deeper review. **No editorial speedup was established.** A low API bill measures processing cost; it does not prove useful automation or reduced reviewer effort. [Pilot report](https://github.com/venumadhav7484/jev-bot/blob/main/docs/source-grounding-pilot.md).

This review pass used cached-media analysis, original browser attachments, rendered pages and transcripts; no additional Jev calls or S3 uploads were made. The most important gains were corrected attribution and preserved counterexamples, not a new universal speedup claim.

Media extraction is also separate from understanding: downloading a video, extracting frames or generating a transcript does not mean its technical claims were reviewed. OCR and transcription errors need checking, and sampled frames can omit decisive events. Source acquisition, machine suggestions, editorial interpretation and independent validation need separate progress counters.

The current user-facing bot uses local retrieval, authored integration designs and templates. Optional Jev Choice routes an entered idea; no separate generative answer model is configured. Its 11 authored design families and development checks are useful boundaries, not a claim of general recommendation accuracy. This guide adds consolidated knowledge; it does not by itself change the bot's retrieval or prove that the bot uses every lesson.

## 11. Rules for recommendations based on this knowledge

Every Jev-bot answer should supply:

1. A **strong, conditional or poor fit** assessment, with the assumption that most affects it.
2. The specific integration point, required state and a few typed questions or candidate actions.
3. What deterministic code, retrieval, perception, a generative model and people still do.
4. Relevant cases with source links, plus counterexamples or failure modes that could change the recommendation.
5. Expected value expressed as a hypothesis unless measured for this workload.
6. A small validation plan, baseline and safe fallback.

Retrieve limitations with positive case summaries. Preserve important contrary evidence even when a relevance score is low. Do not transform proposals into deployments, simulated transactions into real payments, sampled demos into benchmarks or author-reported results into independent findings. Label missing media and inaccessible evidence explicitly. For ideas outside the authored coverage, propose an experiment rather than fabricate an established pattern. [Answer contract](jev-bot-answer-guide.md), [integration patterns](integration-patterns.md).

## 12. What remains unknown and how this guide should evolve

**Review paused at the user’s request on 20 September.** This pass closed 140 of the original 206 external gaps at documented scope. **66 external URL records remain: 8 media reviews, 20 incomplete pages, 37 access failures and 1 unavailable book.** The original 109 media-pending entries were reviewed or resolved as duplicate/contextual media; the remaining 8 are previously metadata-only YouTube/Twitch URLs now read at transcript or description level. Aliases count separately. Separately, 239 Discord source attachments still need inspection, and 38 X posts retain reply/thread-expansion work. These inventories can overlap; adding them does not yield a count of independent missing use cases. Missing replies, media or implementation details may reveal further failures and corrections. [Remaining-review backlog](review-backlog.md), [completion status](completion-status.md).

There is no defensible universal accuracy, latency, savings, calibration or business-impact claim across this catalog. Evidence also does not establish reliable native multimedia reasoning, general exact computation, profitable trading, clinical readiness or blanket security enforcement. Absence of evidence in this pool is not proof that every possible implementation fails.

For each new finding, retain the dated source, actual Jev role, what was observed, what the author claimed, what contradicted it and what remains untested. Update the authoritative case first; then revise the corresponding lesson here and any affected bot design or test. Keep capture progress separate from review progress. Recheck official capabilities and prices when product versions or deployment decisions change.

This guide is the single entry point and synthesis, not a replacement for the underlying evidence. Use the [technical reference](jev-knowledge-reference.md) for API details, the [case catalog](jev-usecases.md) for individual applications and artifact links, the [community findings](community-evidence-findings.md) for additional corrections, and the [completion report](completion-status.md) for unresolved work.


## 20 September incremental findings

[New implementation lessons and grouped leads](incremental-findings.md) cover the next 825 captured messages, including retrieval, evaluation failures, uncertainty, guarded actions and unresolved proposals. These scoped reports do not establish independent benchmark validation.

## 13. Lessons from the latest source review

Reviewed source text adds practical distinctions below. These are scoped documentation reviews and attributed experiments, not independently reproduced benchmarks. A text review does not inspect its embedded video, prove production behavior or validate every linked file.

### Design the decision before choosing the model

Preston's author found that a seven-way relationship classifier hid overlapping labels: two conventions could both make the same choice and deliberately omit the same thing. Independent yes/no questions exposed that overlap. Use Choice for exclusive routes; use separate predicates when multiple properties may hold. Preserve an explicit undecided outcome rather than turning a failed confidence check into `false`. Measure accepted-answer precision and coverage separately for each question. [Working with Jev](https://rodrigopsasaki.com/blog/working-with-jev).

The same report separates candidate retrieval from judgment. Sending roughly the same 22,000-token collection in 21 concurrent requests shortened visible waiting but still repeated the input. Its reported stage improvement from 19.4 to 8.7 seconds did not eliminate duplicated work. Cache acquisition, retrieve candidates, share state across independent questions and measure total calls and tokens as well as wall time. Those numbers describe one author's workload, not a general speed guarantee. [Preston report](https://rodrigopsasaki.com/blog/working-with-jev).

Polar Llama reports that grouping many rows under one semantic question diluted isolated violations; arithmetic aggregates belonged in code. Its experiments favored explicit field names and wider context in some tasks. JevNQL likewise leaves arithmetic to DataFusion. Moving a top-k operation ahead of a semantic filter can change the result: optimize only when the query's meaning is preserved. [Polar Llama](https://github.com/pnthn-ai/polar_llama), [JevNQL](https://github.com/Adityakhalkar/JevNQL).

### Fast screening must preserve exceptions

Revolve documents several different failure policies. Its safety and instruction gates can fail open; its event router leaves uncertain or failed judgments undelivered. Its instruction gate stops blocking after three refusals. These are application policies, not properties of Jev. For a research queue, retain every original item, record an explicit unresolved state and make dropped or delayed work recoverable. Do not inherit an agent helper's fail-open behavior without checking its suitability. [Revolve integration](https://porky11.gitlab.io/revolve-agent/docs/jev.html).

A probability threshold is useful only at the branch where it is enforced. The log-triage documentation places suppress/watch outcomes before its confidence floor; the claimed review boundary therefore needs checking for those paths. Hunch documents fail-open validators and a spam-drop example. These are reasons to test each outcome and failure path, including false negatives, rather than treating a helper's reassuring name as a guarantee. [Log triage](https://github.com/jyatesdotdev/jev-logtriage/tree/main), [Hunch](https://github.com/carldaws/hunch).

Pi Jev Sentinel's author distinguishes task alignment, risk and deterministic execution policy, and explicitly says prompt injection is not solved. Its examples report model probabilities, not measured detection rates. The author also notes that secrets printed through other commands can evade an `.env` exclusion. Keep credentials out of model state through application controls; a semantic screening result is neither permission nor a complete data-loss defense. [Sentinel report](https://x.com/harsh_w98/status/2101366309875548252).

### Keep the actual model and fallback visible

Jevbridge's documented `auto` mode can choose native Jev, a different LLM or a local heuristic. Its heuristic includes words from the question in its evidence and is explicitly a smoke-test backend. A typed response shape does not establish that Jev produced the answer. Record the backend and distinguish fixtures from live calls. [Jevbridge](https://www.github.com/tacticocc/jevbridge).

The LocalJev article describes a stand-in built before its author obtained a Jev key. Its 2.4-second ticket result and local-model benchmark concern open models behind a compatible API. They are not measurements of hosted Jev. Similarly, the Laya Vision model card describes a separate experimental model; its action head received no training gradient and must not be used as a learned safety gate. [LocalJev article](https://www.digitaldias.com/blog/2026-09-19-jev-before-the-waitlist), [Laya Vision card](https://huggingface.co/thaitea/laya-vision-smolvlm-256m).

The circular-maze author initially requested no game logic, then added a calculated move when model confidence was low. Reported successful play therefore includes deterministic assistance. Evaluate the raw decision path and the assisted system separately. SeeFood similarly depends on upstream image labels or captions; a misleading caption can degrade the final Jev decision. [Maze experiment](https://www.viswakumar.com/blog/jev_system_one_model), [SeeFood](https://github.com/wescrockett/seefood).

### Compare quality and latency on the same workload

OpenRouter reports a five-model comparison on 200 synthetic requests across 30 task types. Jev was over five times faster than the next-fastest model and second-cheapest, with accuracy within a handful of cases of the others. The report also discloses different reasoning settings and provider routing. This supports a narrow routing experiment, not a claim of equal accuracy everywhere. [OpenRouter evaluation thread](https://x.com/OpenRouter/status/2101412965765529853).

The Jev-versus-classical-ML report shows a mixed picture: Jev's raw IMDb score exceeds the best reported classical score, while Bank Marketing and Online Shoppers favor classical methods. The three training seeds share a fixed holdout; repeated Jev requests use a cache, so zero standard deviation is not independent repeatability. Adjusted binary results use labeled policy data. Tiny holdouts, missing request diagnostics and unavailable latency summaries limit conclusions. [Benchmark and artifacts](https://quicqdev.github.io/Jev-vs-ML?v=d4f60e6).

A production-adoption report preserves losses alongside wins: 61/69 model-routing answers for both Jev and its LLM baseline; 65% versus 70% on 20 UI prompts; and 779 versus 800 correctly filled static fields for Jev versus script. The author keeps weaker paths in shadow and documents schema drift and an uncapped backfill caught before execution. Use per-path flags, bounded backfills, pinned models, rollback and ongoing labeled failures. Shadow mode still sends data and spends tokens. [Adoption report](https://x.com/yonyoniz/status/2101241236107542549).

Linkmap's author reports 679 proposed links but only 287 retained by an editor. Its roughly $67 full comparison-model run was extrapolated, while rubric development incurred a separate reported $15. Agreement with another model is not independently established accuracy, and proposal throughput is not publication throughput. Count editing, rejected proposals, development and fallback costs. [Linkmap report](https://x.com/stas_sorokin_/status/2101389998608281849).

A separate production-judge report provides an important counterexample: its author found only 2 of 12 genuine contradictions in 36 human-labeled pairs, with ten misses assigned probabilities at or below 0.13. The same report describes stronger fixed-label classification and weaker publication-quality and PR-review results. Low probability therefore cannot be treated as proof that no conflict exists. For research curation, test false-negative rates against labeled cases and retain spot checks of records that screening would discard. The underlying fixtures were not independently reproduced here. [Production-judge comparison](https://x.com/drewdil/status/2100684145286684872).

### What this changes in our research flow

Use deterministic collection and deduplication first; keep immutable source text and dated versions. Use Jev for explicit, independently answerable screening questions and routing. Retain uncertain, contradictory, media-dependent and failed records in a review queue. Source fetching, video inspection, claim attribution and editorial acceptance remain separate steps. Cache reviewed evidence by content hash so unchanged material needs no new model call.

The current review saved 219 scoped source dispositions without new Jev or GLM requests. This demonstrates an offline review path, not measured review-time savings. The public model context receives these curated lessons after export and deployment; private raw captures and review ledgers are not silently supplied to visitors' queries.


## 14. Lessons from recovered recordings and screenshots

The recovered jev-commit recording separates semantic warnings from deterministic enforcement. A commit with contradiction/debug findings succeeds; a private-key-shaped example is blocked by the application belt. Choose explicitly which findings warn, hold or block, and test bypass and failure paths. A fast model response alone does not enforce a policy. [jev-commit](https://github.com/valentynkit/jev-commit).

The shell-vetting CTF screenshot shows a direct read blocked but a script-write followed by script execution displaying a synthetic flag. This observed multi-step bypass reinforces the need to reason across actions and enforce containment outside the model. It is not an independently repeated attack. [Challenge case](use-cases/terminal-guard-ctf.md).

OpenPoke's displayed 33/36 agreement is agreement with another model, not labeled accuracy. Its initial 95.3% email suppression led to quarantine rather than silent dropping. Include unresolved items, quarantine work, fallback calls and total pipeline cost when evaluating a screening stage. Its small synthetic-email comparison does not establish production savings. [OpenPoke evidence](use-cases/openpoke-meets-jev.md).

The LangWatch SQL illustration is a concrete bounded-trace evaluation pattern. Promotional throughput artwork is a separate evidence class: a stated 10,000 conversations in about 20 seconds provides no reproducible trace or accuracy labels. Preserve truncation and digest indicators so a judgment on shortened context is not confused with inspection of the entire conversation. [LangWatch](use-cases/langwatch.md).
