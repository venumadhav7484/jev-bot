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

## What remains before comprehensive synthesis

Finish editorial review of every machine queue, including likely chatter and unrelated classifications; investigate uncaptured context; resolve or document every substantive external source; associate all corrections with the relevant cases; and test the bot's answers against both positive and negative examples. The [completion contract](research-pipeline.md) separates those gates from successful API processing.
