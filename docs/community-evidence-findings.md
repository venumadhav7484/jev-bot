# Findings that Jev-bot must preserve

This is a growing synthesis of inspected community discussion and selected original artifacts. It is not a claim that every channel message or external link has been fully reviewed. Performance figures below remain author reports unless explicitly identified as a local measurement.

## Demonstrated, proposed and evaluated are different

The construction-summary author had built a checker on a generic model and planned to switch to Jev. Hedgehog's author also expressed integration intent. Neither post establishes a deployed Jev integration. The future bot may explain the proposed integration point, but must label it as a proposal. [Construction source grounding](use-cases/construction-source-grounding.md) · [Hedgehog](use-cases/hedgehog-proposed.md).

Our own triage model misclassified those two relationships in a development sample. This is direct evidence that model confidence and a fluent category label cannot replace source inspection. Raw predictions remain unchanged for audit; editorial case descriptions preserve the supported interpretation. Triage sample (local-only evidence).

## Semantic judgments work inside a larger application

Doom's discussion describes ViZDoom and a host-managed tactical layer. The early story demo uses separate evidence-presence and question-validity checks. These examples support a design pattern: supply relevant state, ask bounded questions, and let application code decide what to do with the answers. They do not establish autonomous perception or general reasoning. [Doom](use-cases/doom-launch.md) · [Story validation](use-cases/story-primitive-validation.md).

## Hard requirements must survive ranking

ReadyBase's author reports that plain Jev reranking dropped important structural-risk facts. Reserving facts already marked critical in code recovered the baseline's critical-fact retention. For Jev-bot, source requirements and known counterexamples should not disappear merely because a relevance model ranks them lower. This is an architectural inference from the reported experiment, not an independently reproduced benchmark. [ReadyBase](use-cases/readybase.md).

## Independent judgments can conflict

The EVE-inspired commander report describes a danger judgment that did not agree with the selected tactical posture. Its deterministic controller caught some failures, but not all. Recommendation: check cross-field consistency and preserve a valid fallback action before applying a bundle of predictions. [Commander case](use-cases/eve-commander.md) · [Inspected author report](https://github.com/Diabolacal/eo-map-carbon/blob/main/experiments/typesafe/JEV_TACTICAL_COMMANDER.md).

## End-to-end latency matters

An MMO developer reports EU network overhead preventing the intended responsiveness; the linked PDF remains inaccessible. Separately, the commander author's public-API experiment supported its 1–2 Hz cadence while missing 5–10 Hz deadlines. Jev-bot should ask about deployment location, update frequency and stale-answer handling before promising real-time behavior. [MMO latency report](use-cases/npc-network-latency.md) · [Commander case](use-cases/eve-commander.md).

## Question representation belongs in the versioned design

One discussion reports different probabilities when changing Choice labels or order, and differences between Noul and equivalent binary Choice questions. The author explicitly separates sensitivity from correctness: ground-truth outcomes are needed to assess calibration. Keep model, primitive, instructions, criteria, labels and order together when comparing versions. [Schema sensitivity](use-cases/schema-sensitivity.md).

## Calibration claims do not validate new domains

The news/market experiment's author says no backtest had been run; other participants challenge the claim that additional calibration is unnecessary. Retain this discussion as a counterexample to unsupported success claims. The pool does not establish profitable trading or valid forecasts. [News-to-market experiment and replies](use-cases/news-market-signal.md).

## Failure reports are research leads, not universal verdicts

The Unfair-ToS report lacks protocol details and its author suspects a mistake. The dimensional-reasoning post supplies a prompt but no full result distribution. Both deserve preserved links and a reproducible evaluation, rather than either dismissal or promotion into universal claims about Jev. [Unfair-ToS](use-cases/unfair-tos-probe.md) · [Dimensional probe](use-cases/dimensional-reasoning-probe.md).

## Creative game rules require balance testing

Things versus Stuff maps semantic judgments onto invented tower interactions. Its README describes shared-question evaluation, caching and a decision trace; Discord replies question balance. Semantic plausibility and enjoyable mechanics are separate evaluation targets. [Game case and source links](use-cases/things-vs-stuff.md).

## Useful tooling returns readers to evidence

The Rust `tsg` example supports semantic ranking and predicate filtering while retaining file locations. Its documentation explicitly treats results as review starting points and reports incomplete scans. That is a useful model for this resource pool: retrieval should return source evidence and gaps, not conceal them behind a generated recommendation. [Rust client and tsg](use-cases/rust-tsg.md).

## Media requires a separate acquisition step

Text-only Jev inputs cannot inspect videos or images. The local archive contains 118 messages with a Discord attachment and fewer than 30 extracted body characters. Those require attachment inspection, transcription or an explicit unresolved-media status. They must not be dropped as empty chatter. [Pipeline limits](research-pipeline.md) · [Official model inputs](https://docs.typesafe.ai/models).

## A valid output can still be confidently wrong

Two visually inspected riddle screenshots show a date-arithmetic error at 0.99 confidence and a modified surgeon riddle answered against explicit wording. These are small probes, not a population accuracy estimate. They still rule out interpreting a confidence field as a per-answer correctness guarantee. Use code for exact arithmetic and test paraphrases, option order and missing information. [Riddle probes](use-cases/riddle-probes.md) · [Schema sensitivity](use-cases/schema-sensitivity.md).

## Action-space design can matter more than model speed

Whole-word Wordle choices worked where independent letter choices repeated invalid patterns. Football initially completed no passes; adding reachable pass options and catch-facing controls improved the reported run. The host calculates geometry and enforces legal moves. Exposing an incomplete action set can make the right decision impossible. [Wordle comparison](use-cases/wordle-strategies.md) · [Football self-play](use-cases/football-selfplay.md) · [Sudoku validation](use-cases/sudoku.md).

## Keep memory, perception and execution separate

Catan repeated rejected trades; Vampire Survivors missed obstacles absent from state; a NetHack run was limited by a game-state-advance bug. These failures involve the application as well as the model. Browser examples use DOM/OCR and small LLMs for text; robotics examples use another model or controller for perception and motion. Jev is not thereby demonstrated to see raw images, remember every turn or execute actions itself. [Catan](use-cases/catan-selfplay.md) · [Vampire Survivors](use-cases/vampire-survivors.md) · [NetHack](use-cases/jev-nethack.md) · [OCR computer use](use-cases/computer-use-aaron.md) · [Physical arm](use-cases/physical-robot-arm.md).

## Lower call cost does not guarantee a better workflow

An OpenCode experiment became slower after adding a Jev layer because the LLM still prepared state and actions. The offload pilot found relay slower overall; its code-owned cascade saved work by skipping agent calls, but some paths lost label agreement. A specialized fine-tuned Qwen classifier also beat Jev on latency. Measure the complete path, including preprocessing, network, fallback and correction. [OpenCode overhead](use-cases/opencode-e2e-overhead.md) · [Offload pilot](use-cases/offload-bench.md) · [Fine-tuned classifier](use-cases/internal-classifier-qwen.md).

## Benchmarks need matching denominators and timing boundaries

The reranking winner changes between equal-dataset and equal-question weighting. A private screenshot comparison reports gains overall but loses on mixed requests and one real-comment subset; another column compares two baseline stages with one Jev stage. The Enron chart labels 78 documents, not all 9,840 processed documents. Report the exact cohort and stage, retain losses, and separate throughput from accuracy. [Reranking](use-cases/reranking-benchmark.md) · [Screenshot audit](use-cases/private-process-comparison.md) · [Enron](use-cases/enron-responsiveness.md).

## Fast repeated scoring also helps an adaptive attacker

The trusted-monitor pilot reports lower backdoor detection when an attacker can select among several variants. Kernel screening produced roughly 75% false positives in the author's top-20 alert review. Conversely, deployment context materially improved the separate injection benchmark. This supports workload-specific triage and layered controls, not a universal security boundary. [Trusted monitor](use-cases/ai-control-monitor.md) · [Kernel review](use-cases/kernel-vulnerability-review.md) · [Injection benchmark](use-cases/jev-sec-bench.md).

## Cache judgments when users change the view, not the evidence

The personalized Hacker News demo stores multidimensional scores and reranks locally when sliders move. Argument Mapper and the Pi detail extension similarly change the view over stored judgments. This is a useful pattern when the content and rubric stay fixed; changing either requires cache invalidation. [Hacker News](use-cases/personal-hacker-news.md) · [Argument Mapper](use-cases/semantic-relationships.md) · [Pi detail](use-cases/pi-detail.md).

## Simulation, production claims and real-world validity remain distinct

Driving, flying and ATC demos mostly use simulations. The physical-arm author clarifies an additional orchestrating model and positional feedback. Trading posts mix paper trades, dry runs and claimed live orders; none establishes persistent profitable prediction. A novelty suspicion score, lottery choice or job roast is not validated personal assessment. [Driving demo](use-cases/justin-driving-demo.md) · [Physical arm](use-cases/physical-robot-arm.md) · [Paper trading](use-cases/jev-trade.md) · [On-chain orders](use-cases/monad-kuru-trading.md) · [Lottery novelty](use-cases/lottery-novelty.md).

## Evidence status must travel with retrieval

Default retrieval excludes proposals, thin reports, unsupported financial predictions and novelty claims. Counterexamples and mixed results have a separate retrieval path so useful warnings are not lost by filtering positive examples. Community SDKs remain tools, not independent capability validation. Every recommendation should pair relevant mechanisms with limits and a local validation plan. [Answer guide](jev-bot-answer-guide.md).

## Remaining evidence work

All captured message IDs now have case assignments or explicit dispositions. That completes accounting, not evidence validation. External implementation review, inaccessible media, collapsed replies, capture completeness and recommendation evaluation remain tracked separately in the [completion report](completion-status.md). No community benchmark has been independently reproduced.

## Question wording changes what a result demonstrates

A synthetic clinical-document report found that broad plausibility checks missed all 11 seeded coding errors, while asking for the explicitly stated site with a not-stated outcome found all 11 in that small set. A separate urgency screenshot calls a positive-outcome message a failure even though it still explicitly asks for help ASAP. Ground truth must match the question, and explicit grounding can be more useful than an abstract plausibility judgment. Neither small experiment validates clinical deployment or general reliability. [Clinical grounding](use-cases/clinical-document-grounding.md) · [Urgency wording](use-cases/urgency-wording.md).

## Version the surrounding application, not only the model

Pi-heed's current README moves constraint capture into a main-model ledger; Jev handles narrower semantic checks. It also documents fail-open behavior and a webhook restriction that executed despite a concerning score. The drone author's later successful run differs from an earlier matched comparison where both methods failed. Describe the exact pipeline and scenario before comparing results. [Pi-heed](use-cases/pi-heed.md) · [Drone simulation](use-cases/drone-sim.md).

## Preserve contradictions inside published evaluations

The six-experiment document article gives different trace-checking denominators in its prose and table. The official batching cookbook reports a serial-latency comparison and a small difference in one probability mean despite broad no-change wording. Preserve these details; do not convert a headline multiplier into a workload guarantee. [Document experiments](use-cases/document-lab-experiments.md) · [Official batching cookbook](https://docs.typesafe.ai/cookbooks/parallel_questions).
