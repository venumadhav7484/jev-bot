# Jev: comprehensive knowledge reference

**Start with the [Jev master guide](jev-master-guide.md)** for the consolidated practical synthesis, including the latest reviewed community lessons and counterexamples. This reference retains the deeper API and historical source details.

**Prepared:** 19 September 2026 · **Revision:** 5 · **Context:** Jev capabilities and integration reference

This document focuses on understanding Jev: its capabilities, typed decisions, API, integration patterns, limitations, evidence and unanswered questions. It consolidates the substantive lessons, examples, demonstrations and claims in three supplied Jev transcripts, supplemented by the official documentation reviewed for the original research. **su-lekha is one illustrative use case**, alongside email triage, routing, document review, lead qualification and interactive simulations; it does not define the scope of this reference.

**Revision 3 scope:** quick web refresh on 19 September 2026, following revision 2’s Jev-first reframing. Added structured questions, model discovery, framework integration, official cookbook patterns and gateway data-handling details. Rechecked the model specification and gateway promotion; no authenticated requests, installations or independent benchmark runs were performed. This was a targeted refresh, not a full re-audit of every historical source.

**Revision 4 scope:** added the community resource pool (local-only evidence), linked application patterns and corrected OpenRouter availability using its official model listing. The Discord snapshot and selected linked-source reviews expand the evidence; they do not establish exhaustive coverage. See the coverage report (local-only evidence).

**Revision 5 scope:** resumed message curation, linked-source reviews, screenshot counterexamples and retrieval checks. Official primitives and state pages rechecked on19 September2026. The local project has now made authenticated Jev triage requests, as recorded in the final section.

**Research status:** all captured messages have editorial dispositions; linked-source and media review remain incomplete. No community benchmarks independently reproduced, security guarantees established or customer deployment performed. “Documented” means a provider publishes the capability—not that this project has independently verified its performance. Product proposals below remain proposals.

## Contents

1. [Evidence and transcript provenance](#1-evidence-and-transcript-provenance)
2. [What Jev is](#2-what-jev-is)
3. [System One, classifiers and RLCD](#3-system-one-classifiers-and-rlcd)
4. [Inputs, questions and the evaluation loop](#4-inputs-questions-and-the-evaluation-loop)
5. [Choice, Score and Noul](#5-choice-score-and-noul)
6. [Probability, confidence and business ratings](#6-probability-confidence-and-business-ratings)
7. [API and integration example](#7-api-and-integration-example)
8. [Versions, limits and supported inputs](#8-versions-limits-and-supported-inputs)
9. [Access, SDKs, skills and gateways](#9-access-sdks-skills-and-gateways)
10. [Speed, parallelism and benchmark evidence](#10-speed-parallelism-and-benchmark-evidence)
11. [Pricing and corrected arithmetic](#11-pricing-and-corrected-arithmetic)
12. [Transcript 1: complete chapter digest](#12-transcript-1-complete-chapter-digest)
13. [Transcript 2: complete chapter digest](#13-transcript-2-complete-chapter-digest)
14. [Transcript 3: complete chapter digest](#14-transcript-3-complete-chapter-digest)
15. [Use cases and implementation boundaries](#15-use-cases-and-implementation-boundaries)
16. [Claim corrections and unresolved assertions](#16-claim-corrections-and-unresolved-assertions)
17. [Known limitations](#17-known-limitations)
18. [Every character: capture versus judgment](#18-every-character-capture-versus-judgment)
19. [Privacy, retention and supplier boundaries](#19-privacy-retention-and-supplier-boundaries)
20. [Example use case: su-lekha](#20-example-use-case-su-lekha)
21. [Validation and production readiness](#21-validation-and-production-readiness)
22. [Commercial lessons](#22-commercial-lessons)
23. [Open questions and update triggers](#23-open-questions-and-update-triggers)
24. [Glossary](#24-glossary)
25. [Source directory](#25-source-directory)

## 1. Evidence and transcript provenance

Four evidence labels apply throughout:

| Label | Meaning |
|---|---|
| **Transcript** | A supplied presenter says or describes something. Demonstration footage, code and results were not independently inspected. |
| **Documented** | A relevant official source states it. Useful evidence of the advertised interface or contractual language. |
| **Analysis / proposal** | Reasoning or design derived for this project. Not a vendor guarantee. |
| **Unverified** | Available evidence cannot establish the claim. No substitute fact invented. |

The original reference records that the three source files were preserved unchanged under `research/jev-sources/`, with a manifest (local-only evidence) containing original attachment paths, byte lengths and SHA-256 hashes. Those files and the manifest are not included in this workspace, so their contents and integrity have not been rechecked for this revision.

| ID | Supplied opening chapter | Coverage | Local source |
|---|---|---|---|
| T1 | “What is Jev?” | 12 chapters; final timestamp 12:43 | Transcript 1 (local-only evidence) |
| T2 | “Intro” | 11 chapters; final timestamp 28:17 | Transcript 2 (local-only evidence) |
| T3 | “Introduction to Jev” | 7 chapters; final timestamp 12:17 | Transcript 3 (local-only evidence) |

These are opening chapter labels, not verified video titles. Original video URLs, publication dates and complete channel identities were not supplied. T2 addresses a host as Greg and a guest as Ryan; proper-name transcription may be imperfect. References therefore use **T1/T2/T3 plus timestamps**, rather than invented YouTube links or author attribution.

Transcripts contain automatic-transcription errors, including Jev/Jeb/Jeff, TypeSafe/type safe, Noul/new, JSON/Jason and Vercel/Verscell. Technical terms are normalized in this document; archived originals retain original wording. “Link below,” shared playgrounds and social demos cannot be resolved from transcript text alone.

## 2. What Jev is

**Jev evaluates supplied information against predefined questions and returns typed decisions.** Across the transcripts, the recurring distinction is between producing an open-ended explanation and choosing within an answer space the developer defines. Inputs might describe an email, a contract clause, a customer request or an application’s current state. Outputs might identify a department, estimate whether escalation is needed or rate something against a rubric. [T1, 0:23–2:59; T2, 3:16–4:29 and 7:23–13:40; T3, 3:13–4:09.]

TypeSafe’s introduction describes independent typed questions evaluated against shared state. A request can mix question types. The application supplies context, receives structured results and decides what to do next. The useful abstraction is an intelligent evaluation function embedded in ordinary software. [Official introduction](https://docs.typesafe.ai/introduction).

**Service boundaries:** Jev is a model service. A finished product still needs data access, identity, authorization, policy enforcement, persistence, user interface, monitoring and support. The model does not acquire an email inbox, inspect another application or execute a business action merely because a question refers to it. Those are responsibilities of the surrounding integration.

TypeSafe’s 15 September 2026 launch post identifies Diogo Almeida as founder and introduces Jev in early access. Almeida describes contributions to methods behind ChatGPT; the transcripts’ shorthand does not establish sole authorship. Jev references William Stanley Jevons; System One references Kahneman. [Launch post](https://typesafe.ai/blog/introducing-system-one-models-and-jev).

### Capability map

This map summarizes the evidence already recorded in this reference. Documented interfaces, demonstrated ideas and untested application proposals remain distinct.

| Capability or pattern | What Jev contributes | Boundary / detail |
|---|---|---|
| Semantic classification | Select one named alternative and return its distribution | Choice; alternatives and ambiguity handling are caller-defined (§5) |
| Rubric evaluation and prioritization | Return an expected index across ordered levels | Score; not an exact measurement or calculation (§5) |
| Yes/no assessment | Estimate the probability of a proposition | Noul; no separate confidence field (§5) |
| Multiple independent assessments | Evaluate separate typed questions against shared state | Mixed question types; request and context limits still apply (§§4, 7–8) |
| Routing and action selection | Select among supplied eligible labels or actions | Application supplies candidates, permissions and execution (§15) |
| Document and evidence review | Assess supplied text against explicit criteria | Retrieval, source validity and completeness remain external (§15) |
| Candidate-value selection | Choose among values already extracted in code | Preserve exact values and spans outside the model (§18) |
| Interactive decision loops | Supply bounded choices that code translates into behavior | Game, browser and simulation examples are transcript reports, not reproduced benchmarks (§§12–15) |
| Uncertainty-aware workflows | Expose probabilities and, for Choice/Score, confidence | Calibration and action thresholds need workload-specific validation (§6) |

**Input and output:** the reviewed interface accepts text or JSON state and returns structured decisions. It is not a native image/audio/video interface, an open-ended prose generator, a browser executor or an automatic data collector (§§7–8, 15, 17–18).

**Understanding Jev requires both sides:** what its interface can express and where its judgments can fail. Schema validity, speed claims and low published token cost do not establish semantic accuracy, domain calibration or production reliability (§§10–11, 16–17, 21).

## 3. System One, classifiers and RLCD

### Classifier analogy

T1 compares Jev with older classifiers trained to distinguish categories such as cats and dogs. Its proposed advantage is flexibility: the caller supplies new questions and answer categories rather than training a separate narrow classifier for each workflow. T2 uses a phone-color example and explicitly says the phone is represented in text. These are teaching analogies; neither establishes native image understanding. [T1, 1:03–2:05; T2, 3:16–4:29.]

Classification itself is not new. The opportunity described in the transcripts is making semantic classification convenient, fast and inexpensive enough to embed in many application decisions. That is a product hypothesis to test against existing rules, specialist classifiers and model-based evaluators—not proof that all earlier approaches are obsolete.

### Training vocabulary

TypeSafe’s primer distinguishes **RLHF**, which uses human preferences; **RLVR**, which uses verifiable rewards; and **RLCD**, reinforcement learning for calibrated decisions. Its stated objective is useful probability estimates rather than persuasive explanations. The primer’s broader account of human preference, sycophancy and machine-oriented intelligence is TypeSafe’s framing. It does not establish that RLHF alone causes hallucinations or that RLCD eliminates semantic errors. [AI primer](https://docs.typesafe.ai/introduction/machine-learning-primer).

### What remains undisclosed or unverified

The reviewed material does not establish model parameter count, full training corpus, detailed architecture, reproducible training procedure, publicly available weights or a customer-operated deployment. T2 first claims there is no internal reasoning, then acknowledges uncertainty about server-side processing. The supported conclusion is narrower: the interface returns decisions rather than a generated chain of reasoning. [T2, 13:02–13:32; System One concepts](https://docs.typesafe.ai/concepts/system-one).

An external interface cannot, by itself, establish what computations happen internally. This document therefore makes no claim that Jev is a particular neural architecture, has no reasoning ability, or uses no internal intermediate computation.

## 4. Inputs, questions and the evaluation loop

**Documented input design:** `state` contains the material to evaluate and can be a string, object or array. Questions are supplied separately; each receives the same state. Labeled fields help distinguish records and context. Sending unrelated material together can make the intended target unclear. [State](https://docs.typesafe.ai/concepts/state).

Recommended application loop:

1. Acquire data through an authorized integration.
2. Preserve source identifiers and determine what may leave the environment.
3. Parse and prepare relevant state; resolve exact calculations locally.
4. Define atomic questions with complete instructions and explicit criteria.
5. Submit independent questions together where appropriate.
6. Validate the response and apply versioned application policy.
7. Act, request review or record an unresolved result.
8. Retain evidence needed to reproduce and evaluate the decision.

Example distinction:

| Application need | Input supplied | Model question | Application responsibility |
|---|---|---|---|
| Support routing | Ticket text and relevant account facts | Which eligible department fits? | Confirm eligibility, assign ticket and track resolution |
| Contract review | Clause and review rubric | Is this condition satisfied? | Preserve clause reference and route to reviewer |
| AI data protection | Approved excerpt and policy context | Does this imply restricted disclosure? | Enforce policy and record actual outbound payload |

These are proposed workflows, not demonstrations performed for this document. Missing evidence must remain missing: a model cannot reliably establish facts that the integration never supplied.

## 5. Choice, Score and Noul

### Choice: one option from a defined set

Choice accepts named alternatives with descriptions and returns the selected option, a probability distribution and confidence. Documentation allows up to **255 alternatives**. If several labels can simultaneously apply, use separate questions rather than forcing an exclusive choice. Include an explicit “other” or “insufficient evidence” category when needed. [Choice](https://docs.typesafe.ai/primitives/choice).

**Original example:** classify an AI event as `customer_support`, `engineering`, `finance` or `unclear`. This is classification of observed content; it should not overwrite a department established by authenticated identity.

### Score: position on a defined rubric

Score uses **2–10 ordered levels**, indexed from zero, and returns a probability-weighted expected index. It can be fractional:

```text
score = Σ(level_index × probability_of_level)
```

Each level needs a standalone description. Preserve the distribution: certainty about a middle level and uncertainty between extremes can produce the same average. A rubric score is not an exact measurement in dollars, dates or other physical units. [Score](https://docs.typesafe.ai/primitives/score).

**Original example:** urgency levels might distinguish “routine queue,” “same business day” and “immediate human attention.” A result of 1.6 does not mean 1.6 hours, 80% correctness or a certified service priority.

### Noul: probability of yes

Noul evaluates one yes/no proposition and returns `noul` between 0 and 1. Optional true/false criteria clarify the boundary. It has **no separate `confidence` field**. Near 0.5 means neither answer dominates; it does not mean medium intensity. Code applies a threshold only when a hard decision is required. [Noul](https://docs.typesafe.ai/primitives/noul).

**Original example:** “Does this excerpt contain information about an identifiable customer?” This question is different from “How sensitive is this excerpt?” The first is a proposition; the second requires a sensitivity rubric.

### Question-writing lessons

Question IDs organize responses but are not themselves seen by the underlying model. Important meaning belongs in `instructions` and `criteria`. Separate mixed concerns: urgency, topic, sensitivity and authorization should not be compressed into one ambiguous question. [Primitives overview](https://docs.typesafe.ai/primitives).

### Structured questions and precise field references

The advanced documentation accepts JSON objects and arrays in instructions and rubric descriptions, including Choice option descriptions, Score levels and Noul true/false criteria; it also lists `null` as an accepted entry. This allows a question to carry a schema, examples or a taxonomy subtree directly. However, the HTTP reference lists narrower types for some of these fields. **Documentation discrepancy:** verify the chosen SDK version and live endpoint before depending on the broader shapes; this review did not execute them. [Advanced structure](https://docs.typesafe.ai/primitives/advanced), [HTTP reference](https://docs.typesafe.ai/api).

For structured state, instructions can identify a specific field using a backtick-delimited path such as `ticket.messages[0].text`. This helps direct the judgment; it does not make the field reference a permission boundary. [Primitives](https://docs.typesafe.ai/primitives).

## 6. Probability, confidence and business ratings

These values answer different questions:

| Term | Meaning | Mistake to avoid |
|---|---|---|
| Probability | Estimated likelihood of a particular answer | Treating a high estimate as proof |
| Confidence | Statistic describing the answer distribution | Assuming it always equals the largest probability |
| Calibration | Whether predicted probabilities match observed frequencies across cases | Calling one result “calibrated” without population evidence |
| Rubric score | Expected position among defined levels | Treating it as an exact numeric measurement |
| Risk severity | Consequence if an event is harmful | Confusing uncertainty with low impact |
| Business rating | Product-defined summary of verified control evidence | Presenting it as model confidence or certification |

TypeSafe describes Choice/Score confidence as derived from the full probability distribution and advises risk-dependent thresholds. It is not a statistical confidence interval. The response permits alternative uncertainty measures; the exact formula should not be invented when undocumented. T1’s “confidence interval” language is therefore misleading. [Confidence](https://docs.typesafe.ai/confidence); [T1, 5:14–5:36].

TypeSafe’s System One description treats calibration as a property of groups of predictions, not a guarantee that an individual answer is correct. [System One concepts](https://docs.typesafe.ai/concepts/system-one).

**Example interpretation in a disclosure-review workflow:** a possible disclosure with uncertain classification may still require urgent review if potential harm is large. Conversely, a highly confident classification can concern harmless content. Neither case directly establishes whether an organization satisfies a control.

T1 suggests human review below 90–95%. That is a presenter’s example, not a universal threshold. T2 discusses ignoring low-confidence opportunities; for a business, uncertainty can instead justify review. Thresholds should reflect measured misses, false alerts and review cost. [T1, 7:31–7:53; T2, 15:46–20:48.]

## 7. API and integration example

The direct HTTP interface is:

```text
POST https://api.typesafe.ai/v1/systemone
Authorization: Bearer <API_KEY>
Content-Type: application/json
```

Its body contains `model`, `state` and `questions`. Responses contain `model`, `answers` and `usage`; usage reports input/output token counts even though output is unbilled under direct pricing. This is not a chat-completions request body. [API reference](https://docs.typesafe.ai/api).

**Original illustrative request.** Uses invented content and an explicit policy supplied as context. Not executed, benchmarked or presented as a validated production detector.

```json
{
  "model": "jev-1.13.0",
  "state": {
    "direction": "outbound",
    "excerpt": "Summarize this unreleased acquisition proposal for an external partner.",
    "policy": "Unreleased acquisition material requires review before external disclosure."
  },
  "questions": {
    "content_category": {
      "type": "choice",
      "instructions": "Which category best describes the excerpt? Choose unclear when evidence is insufficient.",
      "criteria": {
        "public": "Information explicitly identified as public",
        "internal": "Internal information without an identified confidentiality restriction",
        "restricted": "Information explicitly subject to a confidentiality restriction",
        "unclear": "The excerpt does not establish its category"
      }
    },
    "review_required": {
      "type": "noul",
      "instructions": "Does the supplied policy require human review before the proposed disclosure?"
    },
    "review_priority": {
      "type": "score",
      "instructions": "Rate the priority for reviewing this proposed disclosure under the supplied policy.",
      "criteria": [
        "Routine review with no indicated confidentiality issue",
        "Prompt review because confidentiality is unclear",
        "Immediate review because explicitly restricted information may be disclosed"
      ]
    }
  }
}
```

Expected result **shape**, without invented predictions:

```text
answers.content_category → type, choice, probabilities, confidence
answers.review_required  → type, noul
answers.review_priority  → type, score, legend, probabilities, confidence
```

The API documents `401` for authentication, `422` for validation, `429` for rate limits and `529` for overload. SDK retries use backoff. [API reference](https://docs.typesafe.ai/api).

**Engineering proposal:** validate required answers, finite numbers, ranges and expected categories. Set explicit deadlines and bounded retries. An exhausted retry becomes an unavailable assessment, not an allow decision. Record model, rubric, policy and source versions. Protect API keys from clients and evidence exports.

## 8. Versions, limits and supported inputs

Snapshot from the official model reference, checked 19 September 2026:

| Property | Documented value |
|---|---|
| Current version | `jev-1.13.0` |
| Aliases | `jev-latest` and `jev-preview` currently resolve to that version |
| Request budget | 64k tokens total |
| Per-question context boundary | State plus longest individual question: 32k tokens |
| Input modality | Text; string, JSON object or array; no native image/audio/video input |
| Published throughput limits | 250,000 tokens/second; 1,200 requests/minute |
| Stability of limits | Dynamic; higher limits require commercial discussion |
| Languages | English strongest; other languages require workload testing |
| Customer adaptation | No per-customer fine-tuning or LoRA; use request context and rubrics |

Aliases can change; pin versions for controlled rollout and record the returned version. [Models](https://docs.typesafe.ai/models).

**Implications:** user count alone cannot predict capacity. Requests, tokens, bursts, question counts and retries matter. A character count is not an exact token budget. Split oversized work deliberately and retain information about which sections were included. A request fitting the limit is not evidence that every fact within it was interpreted correctly.

### Discover available model names

Authenticated `GET https://api.typesafe.ai/v1/models` lists model names available to the account, with descriptions and release dates. The documentation says the list currently contains aliases; versioned IDs can still be accepted without appearing there. The refresh confirmed the existing version, aliases, price and limits in the table above. [Models](https://docs.typesafe.ai/models).

## 9. Access, SDKs, skills and gateways

### Direct access and clients

T2 describes a direct waitlist and a gateway alternative; T1 shares a temporary playground funded by the presenter. Neither anecdote establishes access for this account or a permanent free allowance. [T1, 11:52–12:43; T2, 26:23–27:17.]

TypeSafe publishes Python and JavaScript client entry points: Python `typesafe_sdk.TypeSafeClient` and JavaScript `@typesafe-ai/sdk`. Verify installed package versions against documentation before adopting examples. [Models and client examples](https://docs.typesafe.ai/models).

### Coding-agent skill

The TypeSafe skill supplies API context, patterns and evaluation-writing guidance to coding agents. It helps an agent build an integration; it does not automatically monitor all of that agent’s traffic. Official installation guidance supports Claude Code and other agent environments, with project-local installation described as default for the general installer. Keep questions and thresholds easy to review, and update stale skill references when fields change. [Agent skill](https://docs.typesafe.ai/agent-skill).

No skill or plugin was installed for this research.

### Vercel Gateway: current pricing correction

Vercel lists `typesafe-ai/jev` and demonstrates `experimental_evaluate` from the `ai` package. Its example uses a `boolean` question type, illustrating that wrapper vocabulary can differ from TypeSafe’s direct `noul` interface. **On this review, the page lists free promotional pricing ending 25 September 2026.** Earlier research recorded a displayed rounded $0.04/M price; that earlier observation is superseded for the current promotion. Availability for this account and post-promotion billing remain unverified. [Vercel Jev listing](https://vercel.com/ai-gateway/models/jev).

A gateway introduces another service relationship and potentially another data-processing boundary. Direct and gateway routes require separate checks of schemas, billing, logging, retention and availability. No native Zapier connector is established by this research.

### OpenRouter: availability correction

The earlier revision had not established OpenRouter availability. Its official listing now confirms `typesafe/jev-1.13`, text input and structured-decision output, $0.042/M input tokens, free output, and a displayed 32K context. The `~typesafe/jev-latest` listing links to that version. These are provider-published facts, not a successful authenticated request by this project. [Versioned model listing](https://openrouter.ai/typesafe/jev-1.13), [latest alias](https://openrouter.ai/~typesafe/jev-latest).

Do not silently equate the gateway's displayed 32K context with TypeSafe's direct API budgets: the direct documentation separately states 64K total and 32K for state plus the longest question. Validate the chosen transport and schema before implementation. [Direct model documentation](https://docs.typesafe.ai/models).

Community adapters report using an OpenRouter Decisions endpoint rather than ordinary chat completions. Their adapter details are implementation evidence, not an authenticated compatibility test here; consult the [AILANG case](use-cases/ailang.md) and its linked primary repository before adopting them.

### Gateway options beyond the model listing

Vercel’s launch documentation specifies AI SDK **7.0.105 onward** for `experimental_evaluate`. Choice/Score confidence is exposed at `result.providerMetadata.typesafe.confidence`. It documents gateway ZDR and No Training support, demonstrating `providerOptions: { gateway: { zeroDataRetention: true } }`. Evaluation calls also participate in gateway logs, reporting and budgets. These are gateway features; they do not establish this account’s settings or default direct-API retention. [Vercel launch documentation](https://vercel.com/changelog/typesafe-ai-jev-now-available-on-ai-gateway).

### Pydantic AI integration

Pydantic AI documents `TypeSafeModel`, the `typesafe` installation extra and `typesafe:jev-latest`. Supported output fields map to typed questions: booleans, string enums/Literals, probability floats, rubric IntEnums, option lists, optional choices and nested models. It can select an output type or tool, then fill supported fields/arguments in a second request; unsupported routes can hand off to a configured fallback model. The framework executes the functions. This is bounded argument selection, not unrestricted argument generation.

The adapter also supports conversation judging. Its confidence representation is adapter-specific; do not treat it as identical to the direct API’s field. Jev returns a complete answer rather than token streaming. Option ordering can affect results, and generic sampling settings such as temperature are ignored. Pin and check the installed version: the live page contains capabilities absent from its search excerpt. Integration was read, not installed or tested. [Pydantic AI TypeSafe documentation](https://pydantic.dev/docs/ai/models/typesafe/).

## 10. Speed, parallelism and benchmark evidence

T3 emphasizes fast game decisions and multiple questions in parallel. T2 highlights batch email processing and interactive workflows. These demonstrate the intended workload shape: many bounded judgments, with little need for prose. [T2, 4:37–7:18; T3, 1:07–4:09.]

TypeSafe reports **193.6× faster and 444.6× cheaper** on selected workflow evaluations and **70–500 ms** response times, mostly measured from the US West Coast. Its workflow reference uses averaged predictions from other models rather than independent human ground truth. The launch post acknowledges possible workflow-selection bias and says these gains are toward the high end. Its “0% hallucination” graph is based on schema guarantees, not an empirical semantic-error measurement. [Launch post](https://typesafe.ai/blog/introducing-system-one-models-and-jev).

**Interpretation:** these figures justify investigation; they do not establish universal superiority, Indian-region latency, worst-case latency, audit accuracy or a service-level guarantee. T2’s suggestion of roughly 200 ms regardless of input should not become a product promise. [T2, 15:46–20:48.]

Three different kinds of concurrency matter:

| Kind | What can overlap | Remaining constraint |
|---|---|---|
| Questions within one request | Independent judgments over shared state | Token budget and actual service performance |
| Multiple requests | Independent records or customers | Concurrency, rate limits, queueing and fairness |
| Dependent workflow stages | Only work whose inputs are ready | Later stages wait for earlier results |

For example, classify a request and assess disclosure context together. If a later question depends on an answer from the first call, either make a second call or explicitly prepare possible branches. Parallel execution cannot remove a real data dependency.

**Speculative fan-out:** ask both the routing question and branch-specific questions in one request, then use only the relevant answers. For example, ask ticket category, bug severity and refund intent together. This removes a follow-up round trip when every question is answerable from the original state. TypeSafe describes little typical latency overhead; extra question tokens and context limits still matter. It cannot resolve a question requiring newly fetched information. [Fan-out pattern](https://docs.typesafe.ai/patterns/fan-out).

**Benchmark plan:** measure end-to-end p50/p95/p99 latency, failure rate and accepted decision quality from intended customer regions. Include parsing, policy checks, gateway hops, persistence and retries. Compare against the cheapest approach that meets the same quality requirement. Do not compare a short classification call with an unnecessarily verbose reasoning response and call that a universal speedup.

## 11. Pricing and corrected arithmetic

Direct published pricing is **$0.042 per million input tokens**, with output tokens free. Calculations below use that direct rate, not Vercel’s temporary promotion. [Models](https://docs.typesafe.ai/models).

```text
Model cost in USD = billable input tokens ÷ 1,000,000 × 0.042
```

| Workload | Input tokens | Direct model cost |
|---|---:|---:|
| One small evaluation | 1,000 | $0.000042 |
| One 10k-token evaluation | 10,000 | $0.00042 |
| 1,000 evaluations at 10k tokens | 10,000,000 | $0.42 |
| 10,000 evaluations at 10k tokens | 100,000,000 | $4.20 |
| 100,000 evaluations at 10k tokens | 1,000,000,000 | $42.00 |
| T2’s reported batch | 4,200,000 | $0.1764 |

**T1 correction:** the presenter quotes approximately $0.0042 for one 10k-token request. At the documented rate, that is ten times too high. The later $4.20 and $42 batch examples match the corrected per-request amount. [T1, 10:43–11:10.]

**T2 correction:** 1,700 emails with 4.2 million input tokens imply about **18 cents for the batch**, not 18 cents per email. The transcript momentarily uses “for each,” contradicting both context and arithmetic. Its 500,000 reported output tokens do not add direct output-token fees. Actual invoice and token counts were not inspected. [T2, 6:17–7:18.]

### Illustrative company-size scenario

Assumptions—not measured usage: 50 evaluations/user/day, 22 working days/month, 2,000 billable input tokens/evaluation including questions. One evaluation is one model request; request and response inspections can require separate evaluations.

| Users | Monthly evaluations | Monthly input tokens | Direct Jev cost |
|---:|---:|---:|---:|
| 1 | 1,100 | 2.2 million | $0.0924 |
| 10 | 11,000 | 22 million | $0.924 |
| 100 | 110,000 | 220 million | $9.24 |
| 1,000 | 1,100,000 | 2.2 billion | $92.40 |

These are arithmetic illustrations, not customer quotes or predictions of application margins. Include actual returned usage, rubric overhead, retries, repeated stages and re-evaluations when forecasting.

Total product cost also includes integrations, storage, encryption, evidence retention, queues, alerts, access controls, support, review labor and security operations. Very low evaluation cost can enable a product; it does not prove that product will be profitable. T2’s $5-credit anecdote and “$10 lasts months” intuition depend entirely on workload. [T2, 15:46–20:48.]

## 12. Transcript 1: complete chapter digest

Source for this section: T1 (local-only evidence). Timestamps mark approximate chapter boundaries from the pasted transcript.

| Chapter / time | What the presenter teaches | What to retain or qualify |
|---|---|---|
| 1 · 0:00–1:03 · What is Jev? | Supply information, pose a question and constrain possible answers. Contrasts this with variations in generated prose. | Core answer-space concept. Fixed format does not establish repeatable semantic correctness. |
| 2 · 1:03–2:05 · Classifiers explained | Compares fixed-label cat/dog classifiers with generalized classification through prompts and criteria. Notes architecture not fully revealed. | Useful analogy. Images in the analogy do not establish Jev image input. |
| 3 · 2:05–3:06 · When to use | Rubric evaluation, selecting A/B/C and choosing next workflow action. Introduces checking LLM work. | Look for repeated decisions with defined outcomes. Explicitly include ambiguous cases. |
| 4 · 3:06–4:06 · Checking LLM work | Contracts, proposals, intelligence and estimates. Contract stages: review, final QA, ready to send. Repeated LLM judges can add errors and cost. | A narrower evaluator can reduce workflow overhead. Another model’s judgment remains fallible. |
| 5 · 4:06–5:00 · Comparison | Input-only billing; three question families; agent skill can assist integration. | These are separable interface, pricing and developer-experience claims. |
| 6 · 5:00–6:02 · API and hotel fine print | Questions map to structured answers. Hotel “free cancellation” may mean credit instead of cash. Uses “confidence interval” loosely. | Ask about the actual requirement: cash returned to original payment method. Correct uncertainty terminology. |
| 7 · 6:02–8:02 · Practical uses | Search documents and papers; check whether evidence supports a longevity claim; support routing; contract escalation; track one changed detail across email threads. | Evidence relevance and source coverage matter. A model cannot establish scientific causation merely by labeling a claim. |
| 8 · 8:02–9:00 · Routing | Detect changed launch day; route to coding/model families. Includes speculation about another provider’s past routing incentives. | Retain routing pattern. Provider-motive allegation remains unverified and is not adopted. |
| 9 · 9:00–10:02 · Agents/browser | Replace narrow reasoning substeps, choose agents, identify browser actions or a download button. | Requires a supplied representation and a separate executor. No universal screenshot-reading conclusion. |
| 10 · 10:02–11:10 · More uses/pricing | Clinician-reviewed triage; finance alerts as ignore/review/watchlist; cheap bulk evaluation. | Triage proposals are not medical or financial validation. Correct arithmetic in §11. |
| 11 · 11:10–12:05 · Jev versus LLM | Use Jev for recurring bounded judgments; generative models for explanations and content. Introduces a shared playground with $7 credits. | Workflow fit is the lesson. Presenter-funded access is not an official allowance. |
| 12 · 12:05–12:43 · Playground | Open-ended sky-color question gives poor fit; explicit yes/no oxygen question produces a high estimated probability. | Question design matters. One easy example does not measure calibration. Playground URL absent. |

**Distinctive contribution:** T1 connects typed evaluation with business review workflows and supplies the clearest fine-print example. It also introduces recurring interpretation mistakes: “deterministic,” “confidence interval,” assumed screen access and unreliable cost arithmetic.

## 13. Transcript 2: complete chapter digest

Source for this section: T2 (local-only evidence).

| Chapter / time | What the presenters teach or show | What to retain or qualify |
|---|---|---|
| 1 · 0:00–2:28 · Intro | New classifier-style AI, founder background, invite-only access, productivity and startup potential. | Context and enthusiasm. Revenue possibilities are brainstorming, not business evidence. |
| 2 · 2:28–4:37 · What Jev is | Email problem; phone-color classification with text input and a distribution across colors. | Strong explanation of a probability distribution over a supplied answer space. |
| 3 · 4:37–7:23 · Email triage | Email objects include subject, description/body and sender. Four outputs: category, priority, spam and reply likelihood. Reports 1,700 emails, 4.2M input and 500k output tokens, about $0.18. | Batch economics are plausible at published rate. Accuracy, full runtime and billing remain unverified. “Per email” wording corrected in §11. |
| 4 · 7:23–15:46 · Decision maker | Probability precedes application action; predefined labels and numeric output; no prose response. Discusses uncertainty about internal reasoning. Attempts generation by making alphabet letters choices. | A schema is an output contract, not necessarily a database. Letter-by-letter generation is a curiosity, not a replacement for a text model. |
| 5 · 15:46–20:48 · Business uses | Lead qualification for graphic-design services, mining historical emails for missed work, qualification during a lead form, and routing support questions to prepared teams/agents. Credit anecdotes and near-fixed-latency claims. | Semantic fit can speed routing. Historical intent may be stale; uncertain opportunities need review; accounts and response times must be measured. |
| 6 · 20:48–22:54 · Startup ideas | Match local service requests, such as driveway powerwashing, to suitable businesses. Make qualification and quotes immediate. | Matching requires current availability, geography and service records. Quote amounts need pricing rules, not an unconstrained semantic estimate. |
| 7 · 22:54–24:10 · Bitcoin example | Buy/hold/sell experiment performs poorly. Comparison model receives more information, including news. Presenter cautions against relying on it. | Useful counterexample to “any decision.” No trading edge or controlled model comparison established. |
| 8 · 24:10–25:31 · Video clipping | Transcribe video to word-level text, then rank moments. Reports scoring 17 moments around three seconds. | Jev evaluates a transcript. Transcription, timing alignment, editing and rendering remain separate stages. |
| 9 · 25:31–26:23 · Browser flight selection | Describes Zurich-to-London flight selection in 7.1 seconds. | A specific demo, not a general browser benchmark or proof of successful booking/payment. |
| 10 · 26:23–27:33 · Access | Direct waitlist, Vercel gateway and using documentation with a coding agent. | Check present access and SDK interface. Do not assume transcript-era terms still apply. |
| 11 · 27:33–28:17 · Closing | Encourages inexpensive experiments and looking for classification opportunities. | Start with a measurable workflow rather than extrapolating from excitement. |

**Distinctive contribution:** T2 makes the abstraction concrete through an email application, shows how numerical outputs become application actions, and supplies commercially plausible workflow ideas. The failed Bitcoin example and caveat about unknown internals are as important as successful-looking demos.

### Details worth preserving from the email and lead examples

Topic, urgency, spam likelihood and need for reply are separate dimensions. An informational payment email can be legitimate without needing a response; a possible account violation may warrant attention regardless of category. A sales inquiry may match a company’s services without establishing budget, authority or intent to purchase. These examples favor decomposed questions over one large “good/bad” score. [T2, 4:37–6:17 and 15:46–20:48.]

Historical inbox analysis is an opportunity-discovery proposal. Outreach permission, current customer intent, duplicate handling and human review are separate business requirements. A model’s classification does not itself authorize contacting anyone.

## 14. Transcript 3: complete chapter digest

Source for this section: T3 (local-only evidence).

| Chapter / time | What the presenter teaches or shows | What to retain or qualify |
|---|---|---|
| 1 · 0:00–1:07 · Introduction | Viral launch, founder history, fast decisions and free output tokens. Calls the model “free.” | Output pricing is not total service pricing. Separate current gateway promotion from direct API rates. |
| 2 · 1:07–3:13 · How it works | RLCD versus RLHF, up to roughly 200× faster/400× cheaper, benchmark comparisons, Doom and Wikipedia races. Reports five hops in half a second. | Training objective and bounded choices are useful concepts. Timings and rankings are demo/marketing claims, not independently reproduced measurements. |
| 3 · 3:13–4:18 · Decision engine | Duplicate-charge support ticket with account facts; classify request, urgency and priority in parallel. | Concrete example of independent questions on shared state. Branding slogans are not technical capabilities. |
| 4 · 4:18–5:17 · Reliability | Attributes hallucination to human-feedback training, cites zero hallucinations and mentions high-stakes domains. | Schema guarantees do not establish correct judgments or suitability for medical, traffic or military decisions. |
| 5 · 5:17–6:24 · Zapier sponsor | Promotes workflows linking thousands of apps and suggests plugging Jev into them. Includes prominent customer logos. | Sponsored segment. No native Jev connector, shared customer relationship or end-to-end speed multiplier verified here. |
| 6 · 6:24–8:40 · Practical demos | A generative coding model builds a town; Jev drives 50 characters reacting to a bakery sale or snake threat. Another simulation sorts 150,000 virtual Skittles. | Distinguish app generation, textual state, model decisions and animation. Neither establishes sensor processing or physical robotics capability. |
| 7 · 8:40–12:17 · Advanced examples | Chess, model router, ad/slop filtering, simulated Tesla-like driving built quickly, and Melee control. | Demonstrates breadth of possible wrappers. Does not establish production reliability, FSD equivalence or general strategic superiority. |

**Distinctive contribution:** T3 broadens the design space from business classification to fast interactive loops. Its strongest lesson is that ordinary code can translate typed decisions into visible behavior. Its weakest inference is equating schema-constrained output with error-free understanding.

### Chess and simulation details

The transcript says Jev loses to Astra but beats Fable on time despite being outplayed on the board. That illustrates how latency changes an outcome under a game clock. It does not establish stronger chess play or a reliable win rate. The presenter’s extrapolation to winning bullet chess almost every time is unsupported by the described sample. [T3, 9:23–10:28.]

The town demo reports 50 decisions: 39 characters continue, six investigate, four join and one warns others after a bakery announcement. The snake prompt changes most agents’ behavior. The exact first timing is garbled in the transcript; no precise latency is inferred from that text. [T3, 6:24–7:48.]

The Skittles, driving and Melee examples are described through rendered behavior. Without their code, the number of API requests, batching method, state construction, physics and safety constraints remain unknown. A large number of animated objects does not by itself prove an equal number of live model calls. [T3, 7:48–8:40 and 11:17–12:17.]

## 15. Use cases and implementation boundaries

This inventory consolidates all substantive application ideas across the transcripts. **All are transcript ideas/demos or project analysis; none was reproduced here.** “Model role” describes a plausible decomposition, not a validated detector.

| Use case / transcript reference | Bounded model role | Work that remains outside Jev |
|---|---|---|
| Hotel fine print · T1 5:40–6:19 | Cash-refund condition satisfied? | Acquire correct terms; verify booking-specific applicability |
| Paper/document screening · T1 6:19–7:02 | Relevant to criterion? | Retrieval, document extraction, coverage and citations |
| Claim/evidence review · T1 6:36–7:02 | Supported, unsupported or unclear? | Source validity, causal analysis and expert review |
| Contract progression · T1 3:27–4:06 | Review stage or unresolved condition | Authorized reviewer and release workflow |
| Contract risk triage · T1 7:31–7:53 | Which clauses deserve review? | Jurisdiction, complete evidence and professional judgment |
| Support routing · T1 7:02–7:31; T3 3:13–4:09 | Department and priority | Identity, eligibility, queue assignment and escalation |
| Email topic/urgency · T2 4:37–7:18 | Categories and rubric levels | Mail access, user preferences and correction feedback |
| Spam/reply triage · T2 5:14–6:17 | Spam and reply-needed probabilities | Sender verification and reversible filtering policy |
| Email-thread changes · T1 7:53–8:18 | Select relevant stated update | Thread ordering, exact dates and source message IDs |
| Model routing · T1 8:18–9:00; T3 10:28–10:45 | Choose eligible model class | Current capabilities, cost, permissions and fallback rules |
| Agent routing · T1 9:15–9:30 | Choose prepared agent | Tool permissions, execution and success verification |
| LLM-work checking · T1 2:59–4:06 | Evaluate explicit requirements | Ground truth, tests and residual-error handling |
| Workflow substeps · T1 9:00–9:15 | Replace a narrow judgment | Dependency graph and exact transformations |
| Browser action selection · T1 9:30–10:02 | Choose candidate element/action | DOM/accessibility extraction, browser control and confirmation |
| Flight selection · T2 25:31–26:23 | Rank eligible flight/actions | Current fares, restrictions and booking authorization |
| Clinical attention triage · T1 10:02–10:25 | Flag evidence for clinician review | Clinical validation, privacy and qualified decisions |
| Financial-alert triage · T1 10:25–10:43 | Ignore, review or watchlist | Data quality, user objectives and action controls |
| Lead qualification · T2 15:46–20:48 | Fit to service criteria | Budget/availability verification and sales process |
| Historical opportunity mining · T2 15:46–20:48 | Identify overlooked inquiries | Current relevance, consent and duplicate handling |
| Local-service matching · T2 20:48–22:54 | Rank suitable vendors | Geography, availability, contractual pricing and fulfillment |
| Instant quotes · T2 21:38–22:49 | Classify job requirements | Exact price calculation and scope confirmation |
| Bitcoin action experiment · T2 22:54–24:10 | Choose from buy/hold/sell | No demonstrated predictive edge; equal-input evaluation absent |
| Video clipping · T2 24:10–25:31 | Score candidate transcript moments | Transcription, timestamps, clip assembly and editorial judgment |
| Wikipedia navigation · T3 2:20–3:13 | Choose among known links | Fetch pages, enumerate links and maintain traversal state |
| Doom/game control · T3 2:11–2:20; 12:01–12:17 | Choose legal actions from supplied state | Game engine, state adapter and timing loop |
| Simulated town · T3 6:24–7:48 | Character response category | Character state, rendering and behavior execution |
| Virtual Skittles · T3 7:48–8:40 | Select bucket/action | Object state, animation and batching; no physical sensing proved |
| Chess · T3 9:23–10:28 | Select a candidate move | Legal moves, clock, board state and strategic evaluation |
| Ad/slop filtering · T3 10:45–11:17 | Classify candidate page regions | Browser extension, DOM mapping and reversible hiding |
| Driving simulation · T3 11:17–12:01 | Choose steering/action label | Simulator, perception representation and constraints |
| Alphabet generation experiment · T2 14:05–15:46 | Choose a next character | Repeated sequential calls; not a supported prose-generation workflow |

The common design pattern is **context → bounded semantic judgment → controlled application action**. Applications differ in data access and consequences, even when they reuse the same evaluation service.

### Additional patterns from official cookbooks

The web refresh found a broader set of worked patterns than the transcript inventory alone captured. These are provider-authored implementations and examples, not capabilities independently validated in this workspace.

| Pattern | How Jev is used | What remains in code or another component |
|---|---|---|
| Retrieval reranking | Noul scores each shortlisted query–passage pair for relevance. [Cookbook](https://docs.typesafe.ai/cookbooks/rerank_typesafe) | Initial retrieval, ranking and evaluation; omitted candidates cannot be recovered by reranking. |
| Semantic line search | Choice ranks supplied line IDs; a separate Noul asks whether an answer exists at all. [Cookbook](https://docs.typesafe.ai/cookbooks/semantic_find) | Assign IDs, preserve source lines and handle missing answers. A top-ranked line alone does not prove relevance. |
| Hierarchical classification | Repeated Choice questions traverse taxonomies; beam search retains several plausible paths. [Cookbook](https://docs.typesafe.ai/cookbooks/hierarchical_classification) | Tree traversal, pruning and path scoring. Multiple bounded questions can cover a taxonomy larger than one Choice menu. |
| Function and argument selection | Questions select a function and its closed-set arguments, including optional and set-valued selections. [Cookbook](https://docs.typesafe.ai/cookbooks/function_calling) | A dispatcher assembles and executes calls. Arbitrary text/numbers are not generated by this pattern. |
| Entity matching | Score assesses whether candidate records describe the same entity; Nouls identify field disagreements. [Cookbook](https://docs.typesafe.ai/cookbooks/entity_alignment) | Candidate generation, review and actual merge operations. |
| Date-part extraction | Choice selects stated date components and relative-date forms. [Cookbook](https://docs.typesafe.ai/cookbooks/date_extraction_cookbook) | Calendar arithmetic, missing/invalid-date handling and final date construction. |
| Extraction verification cascade | Jev checks fields extracted by a smaller generative model and flags cases for a stronger model. [Cookbook](https://docs.typesafe.ai/cookbooks/sde_cascade) | Both extraction stages and escalation logic; Jev is the verifier. |
| Feature discovery for supervised learning | Jev converts text into numeric answers to questions proposed by an LLM; those features train a CatBoost regressor. [Cookbook](https://docs.typesafe.ai/cookbooks/autoresearch_feature_discovery) | Question proposal, training and error-driven iteration. This adapts a downstream model, not Jev’s weights. |

The official index also lists skill suggestion, RAG passage classification, citation checking, guardrails, confidence-based classification and Markdown structure recovery. These extend existing routing/review themes. The structure-recovery page failed to load during this refresh; only its index description was inspected. [Documentation index](https://docs.typesafe.ai/llms.txt).

**Version and benchmark caution:** some cookbooks still use `jev-1.12` and replay packaged cached responses. For example, entity alignment identifies historical cached results, and semantic line search documents a keyless replay path. A successfully rendered notebook therefore does not prove a new live request or performance on `jev-1.13.0`. [Entity alignment](https://docs.typesafe.ai/cookbooks/entity_alignment), [Line search](https://docs.typesafe.ai/cookbooks/semantic_find).

## 16. Claim corrections and unresolved assertions

| Claim or implication | Evidence-based treatment |
|---|---|
| “Zero hallucinations” means zero wrong decisions | Unsupported. Type/format validity and semantic correctness are different. See §10 and §17. |
| A fixed answer space makes every result deterministic | Not established. Consistent shape does not prove identical probabilities or choices across runs or versions. |
| Every answer includes a confidence score | Noul is an exception. See §5. |
| Confidence values are confidence intervals | Incorrect terminology; see §6. |
| A 95% threshold guarantees safety | No. Threshold selection needs task-specific evidence and consequence analysis. |
| No generated prose means no output payload/tokens | Incorrect. Structured response data and usage still exist; see §7. |
| Jev performs no internal reasoning whatsoever | Not established by the exposed interface; T2 itself qualifies this assertion. |
| Jev can make any decision reliably | The Bitcoin failure and documented weaknesses contradict that generalization. |
| Jev is free | Route/date dependent. Direct input is priced; current Vercel promotion is temporary. See §§9–11. |
| 10k input tokens cost $0.0042 | Arithmetic correction: $0.00042 at the reviewed direct rate. |
| The email demo cost $0.18 per message | Context and arithmetic support roughly $0.18 total. |
| Any input size takes approximately 200 ms | Unsupported latency guarantee. Measure realistic inputs and tail latency. |
| Parallel questions imply unlimited scale | Request budgets, throughput and application bottlenecks still apply. |
| Doom/browser demos prove native screenshot understanding | Current modality specification does not support that inference; see §8. |
| A one-hour driving simulation recreates production FSD | Unsupported. Simulation is not road deployment or a safety case. |
| A chess clock win establishes better chess intelligence | Unsupported. Board quality and timing are different performance dimensions. |
| Zapier sponsorship proves a native Jev integration | No verified connector or configuration supplied. |
| A coding-agent skill sees every model interaction | Incorrect inference. Documentation assistance is not traffic interception. |
| No training on customer data means no retention | Incorrect inference. See §19. |
| Other models cannot produce structured outputs/probabilities | Overbroad. Even TypeSafe’s launch evaluation describes an LLM wrapper returning compatible structured decisions. Compare actual interfaces and measured quality. |
| Third-party routing motives or launch scandals are established facts | Not corroborated here; excluded from conclusions. |
| Viral views, logos or enthusiastic demos prove customer demand | No. They provide discovery signals, not paid-demand evidence. |

References for corrections: [API](https://docs.typesafe.ai/api), [primitives](https://docs.typesafe.ai/primitives), [confidence](https://docs.typesafe.ai/confidence), [model limits](https://docs.typesafe.ai/models), [launch methodology](https://typesafe.ai/blog/introducing-system-one-models-and-jev), [known weaknesses](https://docs.typesafe.ai/model-jaggedness/jev-1.13), [privacy](https://typesafe.ai/legal/privacy-policy), and the timestamped digests above.

## 17. Known limitations

TypeSafe’s Jev 1.13 limitation note, reviewed by the provider on 17 September 2026, identifies these weaknesses:

| Documented weakness | Engineering response proposed here |
|---|---|
| Literal reading | State boundaries and exceptions explicitly |
| Arithmetic and counting | Compute exact values in code |
| Date/time comparison | Parse timestamps and compare normalized values |
| Multi-step indirection | Supply direct references and reduce inference hops |
| Large irrelevant context | Select relevant evidence while recording omissions |
| Adversarial input | Treat source text as untrusted and test attacks |
| Conflicting instructions/criteria | Review rubrics as versioned configuration |
| Inconsistent related answers | Enforce required invariants in code |
| Generation | Use a generative component when prose is required |

The same note warns against reconstructing exact quantities by interpolating Score levels. [Jev 1.13 jaggedness](https://docs.typesafe.ai/model-jaggedness/jev-1.13).

**Integration implication:** Jev cannot be the sole source of truth for “no secrets exist,” “all characters were checked,” “all obligations are satisfied” or “the action is safe.” Negative findings need measured detector coverage. Explanations shown to customers must reference actual evidence and policy, not fabricate a model rationale that the API never returned.

## 18. Every character: capture versus judgment

This addresses the earlier question: **can Jev efficiently parse every character sent to model servers and every response?**

The defensible answer separates four tasks:

| Task | Responsible component in a proposed system | Evidence needed |
|---|---|---|
| Observe bytes at a supported boundary | Application gateway or supported device adapter | Captured request/response fixtures and coverage tests |
| Parse bytes into fields, text and exact spans | Protocol parser and deterministic code | Encoding, escaping, streaming and offset tests |
| Interpret meaning | Jev with explicit context and rubric | Labeled evaluations, error analysis and calibration |
| Enforce an action | Authorized policy engine at the relevant boundary | Proof that block/redaction occurs before release |

The token budget and known counting weaknesses in §§8 and 17 prevent a blanket character-perfect interpretation claim. Even complete capture does not guarantee complete semantic understanding. Conversely, a strong classifier cannot inspect content that bypasses the integration.

TypeSafe’s extraction cookbook illustrates a useful split: code finds candidate values and the model selects among them, preserving original values rather than generating replacements. [Pre-parsed extraction](https://docs.typesafe.ai/cookbooks/pre_parsed_value_extraction_cookbook).

**Proposed exact-redaction method:** keep source bytes and offsets locally; identify candidate spans; ask semantic questions only where necessary; apply approved edits to known spans; validate the resulting payload. If the exact span cannot be established, request review or block under policy rather than redact a guessed substring.

Streaming adds timing constraints. Logging response chunks after release provides observation. Preventing release requires buffering or a tested incremental policy. Split secrets, Unicode, escaped JSON, attachments and tool arguments belong in the test corpus. OCR/transcription can introduce errors and must be labeled as a transformation, not exact capture of the original content.

A captured outbound payload is evidence of what crossed that observed boundary. It does not reveal the provider’s internal training, retention, downstream processing or hidden model reasoning. Those need separate contractual or operational evidence.

## 19. Privacy, retention and supplier boundaries

### What reviewed sources say

TypeSafe’s privacy policy, dated 19 November 2025, covers its APIs and Playground. It states that prompts and other input are not used to train or fine-tune models, describes service-provider disclosures, and says services are hosted in the US. Its retention language is “reasonably necessary,” rather than a universal zero-retention period. [Privacy policy](https://typesafe.ai/legal/privacy-policy).

The DPA, dated 24 April 2026, describes customer-controller/TypeSafe-processor roles, processing under documented instructions, subprocessors and international-transfer terms. Its schedule bases retention on processing purpose and applicable law. The sensitive-data schedule says “N/A”; that should not be read as a blanket approval for regulated workloads. Actual contractual applicability must be established for the intended relationship. [Data Processing Addendum](https://typesafe.ai/legal/data-processing).

TypeSafe’s legal documentation offers **enterprise zero data retention** through a separate discussion. That does not establish ZDR on a default direct account. The web refresh adds a separate supported route: Vercel explicitly documents a gateway ZDR request option (§9). This corrects the earlier incomplete gateway coverage; account settings and applicable terms remain unverified. [Legal reference](https://docs.typesafe.ai/legal), [Vercel gateway announcement](https://vercel.com/changelog/typesafe-ai-jev-now-available-on-ai-gateway).

### Implications for a data-security product

Jev evaluation is itself another data transfer when hosted externally. Any application using it must account for that processing boundary. Proposed integration safeguards:

- Require a customer-authorized TypeSafe route before sending content.
- Prefer relevant, minimized text; retain raw archives under customer control.
- Record which fields were sent and which transformations removed or obscured data.
- Avoid forwarding API keys, unrelated content or other tenants’ data.
- Distinguish customer-local evidence, application metadata and TypeSafe evaluation input.
- Recheck gateway terms separately if a gateway is used.
- Make retention, deletion, access and regional constraints explicit configuration and contract requirements.

Local masking can also remove context needed for judgment. Test that tradeoff. If the authorized data route cannot support a check, show an unavailable or limited assessment rather than silently changing providers or treating the check as passed.

**Not established here:** a specific account’s retention settings, a signed enterprise agreement, SOC/ISO attestations, an approved subprocessor inventory, customer-hosted Jev availability or regulatory suitability. Public documentation alone cannot fill those gaps.

## 20. Example use case: su-lekha

su-lekha illustrates how Jev could support an AI data-use monitoring and review application. This section preserves an example design, not an implemented product, a required architecture or the primary purpose of this reference. Other use cases in §15 use the same bounded-evaluation pattern. Historical architecture and implementation-plan links are listed in §25 for context.

### Where Jev could fit

In this example, su-lekha needs repeated, bounded judgments about AI data use: sensitive context, policy relevance, evidence sufficiency and review priority. Jev could serve as its semantic evaluator, subject to customer-authorized processing and successful validation. These are candidate applications of its primitives, not independently verified detection capabilities.

The example separates semantic judgments from exact parsing, identity, permissions, counting, evidence integrity, redaction, enforcement and rating arithmetic, which belong in code. A selected evaluator can still fail a deployment gate; the application must expose that failure accurately.

### Example architecture with shared evaluation

```text
Supported personal/developer tools ──> Device Agent ────────┐
                                                          │
RAG chatbots and backend AI routes ──> Application Gateway ─┤
                                                          v
                                     Shared event and policy contract
                                          │                 │
                                Exact local checks    Approved semantic input
                                          │                 │
                                          │          TypeSafe / Jev
                                          │                 │
                                          └──────┬──────────┘
                                                 v
                                  Findings + evidence + verified controls
                                                 │
                                                 v
                                  Shared Core, ratings and customer view
```

This is a **logical responsibility diagram**, not a claim that all raw traffic goes to a central server. Enforcement stays at a connection boundary capable of enforcing. Raw evidence remains customer-controlled by default. Shared Core receives the metadata and references permitted by policy.

Adapters connect different environments to the same contract. They are reusable integration components, not bespoke products for each company. Unsupported closed applications remain uncovered until a tested integration exists. A common semantic evaluator does not remove differences in application access.

### MCP and plugin scope

MCP defines host/client/server relationships and callable tools; the host controls shared context. A server is not automatically given the complete conversation, and exposing an assessment tool does not guarantee every outbound prompt calls it. [MCP architecture](https://modelcontextprotocol.io/specification/2026-07-28/architecture), [MCP tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools).

MCP or a plugin may expose su-lekha assessments and reports. Reliable capture and mandatory prevention still require a supported observation/enforcement point. Product scalability comes from shared contracts, policies and infrastructure—not pretending one extension has access to every application.

### Candidate checks

| Proposed check | Jev contribution | Deterministic/evidence contribution |
|---|---|---|
| Confidential business content | Assess meaning against a defined policy | Source fields, destination identity and exact payload |
| Personal-data context | Evaluate whether content concerns identifiable people | Known identifiers, candidate spans and masking |
| Instruction attack indicators | Flag context suggesting instruction manipulation | Trusted instruction boundaries and permission enforcement |
| Response disclosure | Assess whether response reveals restricted context | Comparison with supplied sources and release policy |
| Evidence relevance | Classify supplied evidence against a control criterion | Authenticity, freshness, scope and actual test results |
| Review priority | Apply a defined urgency rubric | Incident impact, business owner and escalation deadline |

All six are hypotheses requiring evaluation. High model confidence cannot grant permissions, prove provenance or close a failed control.

### Simple customer experience

Keep the default screen focused on **Compliance rating, Security rating, coverage and priority fix**. A finding should answer: what happened, which tool/provider was involved, what evidence supports it, whether anything was blocked/redacted, and what to do next.

Jev probabilities and rubric versions belong in drill-down evidence. Customers should not need to understand model internals to act. Two headline ratings can stay simple while the underlying evidence remains inspectable.

**Rating proposal:** compute ratings from verified applicable controls, not prompt-level confidence. The current illustrative method is passed controls divided by applicable controls, multiplied by 100; unknown/stale controls receive no pass credit, and critical failures override the headline status. This is a product-defined measure, not an industry-issued score or certification. Standards mapping requires a separate reviewed control catalogue.

### Continuous evaluation and reports

Checks run on relevant events; findings update continuously. Monthly or on-demand reports summarize evidence, changes and unresolved issues. A new classification does not automatically change a company’s control rating. Closure requires a verified passing retest.

For one user, departments can stay hidden. Larger organizations add tenant and department scope, access control, queues, budgets and reporting views around the same event contract. Traffic volume and policy complexity drive capacity needs more directly than employee count.

### Unavailable checks

In observation mode, an unavailable evaluation creates a visible coverage gap. In a prevention workflow requiring that check, the configured policy holds or blocks the action. Never label an unperformed check as passed or silently send data to an unauthorized fallback provider.

A possible pilot for this example is **one supported personal/developer tool plus one custom RAG chatbot**, using the same evaluator, seeded risks, evidence shape and screen. Observation could precede scoped prevention after relevant tests pass. This is an illustrative validation path, not a commitment to build su-lekha.

## 21. Validation and production readiness

The following is a proposed validation plan, not a report of completed tests.

### Build a representative evaluation set

Use authorized, synthetic or appropriately de-identified records spanning departments, supported languages, normal requests, genuine violations and ambiguous examples. Include quoted malicious instructions, mixed policies, long context, missing evidence, split streaming data, encoded fields and transformed attachments. Label difficult cases with domain reviewers and preserve disagreements.

Separate development examples from held-out evaluation data. Test explicit rules and existing deterministic detectors as baselines. Add suitable specialist or generative evaluators only where the comparison answers a real design question.

### Measure the whole product

| Dimension | Measurement | Decision it informs |
|---|---|---|
| Capture coverage | Known test events captured versus generated | Which integrations can be claimed supported |
| Classification quality | Precision/recall by risk and department | Which semantic checks are useful |
| Missed harm | Severe false negatives and their causes | Whether prevention is acceptable |
| Review burden | False alerts, unresolved cases and reviewer time | Whether automation saves work |
| Calibration | Observed accuracy within probability bands | Whether probability-based policy is justified |
| Abstention | Quality versus fraction routed to review | How much work can safely be automated |
| Latency | End-to-end percentiles by region and payload | Whether inline checks fit user experience |
| Reliability | Errors, retries, timeouts and queue growth | Outage handling and capacity |
| Cost | Actual usage plus infrastructure/review cost | Unit economics |
| Exact enforcement | Verified sent payload and release timing | Whether block/redaction claims are true |
| Reproducibility | Model/rubric/policy/source versions retained | Whether incidents can be reconstructed |

Do not set a universal 90% or 95% automation threshold before these measurements. Agree acceptance criteria for each check and consequence. Report sample sizes and uncertainty; a handful of successful demos is insufficient evidence for rare failure rates.

### Rollout sequence

1. Validate API shape using synthetic material and an authorized account.
2. Compare semantic outcomes on a labeled held-out set.
3. Run a shadow or observation workflow against the intended integrations; for the su-lekha example, these are the two connection types in §20.
4. Review false alerts, misses and capture gaps with users.
5. Enable narrowly scoped prevention only where capture and decision evidence meet agreed gates.
6. Re-evaluate after model, rubric, policy or integration changes.

Maintain tenant isolation, deadlines, queue fairness, version rollback and explicit outage status. A successful model benchmark does not replace security testing of the product that handles customer evidence.

## 22. Commercial lessons

**Transcript-derived opportunity:** low-cost semantic decisions may improve workflows where a business repeatedly classifies, routes or reviews information. T2’s examples—support triage, lead qualification and service matching—are attractive because outcomes can be measured in time saved, faster response and less missed work. [T2, 15:46–22:54.]

**Analysis:** access to Jev alone is not a defensible product. Other builders can use the same service. Potential differentiation comes from dependable integrations, measurable workflow outcomes and customer trust. In the su-lekha example, evidence provenance, understandable findings and tested controls would also matter.

The practical alternatives to evaluate are existing rules, narrow classifiers, manual review, generative evaluators and customers’ current monitoring/security products. The historical su-lekha research history (local-only evidence) is separate application-specific context, not a general Jev competitor assessment.

Money-making potential remains a hypothesis. Test whether customers will pay for a concrete outcome: explaining an actual data transfer, detecting a real policy issue or producing evidence that saves review time. Measure acquisition, onboarding, support and remediation costs alongside model cost. “Cheap model” and “profitable security product” are separate propositions.

The described capabilities motivate bounded experiments in suitable workflows. Their results, rather than the examples alone, must determine product fit, revenue assumptions and integration scope.

## 23. Open questions and update triggers

| Question | Current status / next evidence needed |
|---|---|
| Can this account access direct Jev? | Not tested; verify authorized account access |
| What happens after Vercel’s promotion? | Recheck account-specific rate and terms after 25 September 2026 |
| What latency will Indian customers experience? | Measure intended regions and payload distributions |
| Are probabilities calibrated on the intended workload? | Held-out, domain-labeled evaluation required |
| How robust is prompt-injection detection? | Adversarial testing required; no guarantee adopted |
| Can multilingual, mixed-script and encoded content be handled? | Workload-specific tests required |
| How do outputs vary across repeated calls and versions? | Repeated evaluation and controlled upgrades required |
| Is enterprise ZDR available on acceptable terms? | Obtain applicable written terms and verify configuration |
| What subprocessors and locations apply? | Review current inventory and customer contract |
| Are private deployment or open weights available? | Not established by reviewed sources |
| What service guarantees and stable quotas apply? | Commercial confirmation required |
| What are the exact confidence computation and SDK guarantees? | Direct confidence formula remains unspecified on the reviewed page; adapter representations differ (§9) |
| Do structured question shapes agree across docs and clients? | Advanced docs and HTTP field types differ; validate the pinned SDK and live endpoint (§5) |
| Can the intended integrations meet their capture/action claims? | End-to-end fixtures required; the su-lekha example also needs seeded-risk and prevention tests |
| Will customers pay and renew? | Paid pilots and retention evidence required |
| Where are original demo URLs and code? | Not supplied; request or discover independently before citing as reproduced evidence |

Update this reference when model aliases move, rate limits/pricing change, modality support expands, contracts change, original video/code links become available or project experiments produce evidence. Preserve dated observations rather than silently rewriting their historical meaning.

## 24. Glossary

| Term | Meaning in this document |
|---|---|
| Jev | TypeSafe’s named decision/evaluation model |
| System One | TypeSafe’s model category for fast structured judgments |
| State | Supplied information the model evaluates |
| Question | Explicit instruction plus answer type and applicable criteria |
| Answer space | Allowed choices or rubric levels |
| Choice | One selection with a distribution across alternatives |
| Score | Expected index across ordered rubric levels |
| Noul | Estimated probability of yes to one proposition |
| Calibration | Agreement between predicted probabilities and observed frequencies |
| Schema/type safety | Output conforms to the expected structure and types |
| Semantic correctness | Output meaning matches the facts and intended criterion |
| RLCD | Reinforcement Learning for Calibrated Decisions |
| RLHF | Reinforcement Learning with Human Feedback |
| RLVR | Reinforcement Learning with Verifiable Rewards |
| DPA | Data Processing Addendum/Agreement governing relevant processing |
| ZDR | Zero data retention, subject to an applicable service agreement |
| Observation | Inspect/report without necessarily stopping an action |
| Prevention | Enforce before a prohibited action or release completes |
| Evidence | Traceable source or test result supporting a finding |
| Coverage | Scope actually observed or assessed, including known gaps |
| Attestation | A scoped statement supported by specified evidence; not automatically certification |

## 25. Source directory

### User-provided primary material

- **T1:** What is Jev? — supplied transcript (local-only evidence). Twelve chapters; final timestamp 12:43.
- **T2:** Intro — supplied transcript (local-only evidence). Eleven chapters; final timestamp 28:17.
- **T3:** Introduction to Jev — supplied transcript (local-only evidence). Seven chapters; final timestamp 12:17.
- Source manifest with integrity hashes (local-only evidence).

### Official technical and product references

All web references reviewed for this research on 19 September 2026. Live pages may change. Provider-authored documentation supports descriptions of the provider’s interface and claims; it is not independent performance validation.

| Source | What it supports |
|---|---|
| [TypeSafe introduction](https://docs.typesafe.ai/introduction) | Shared state and typed evaluation |
| [System One concepts](https://docs.typesafe.ai/concepts/system-one) | Intended task class and calibration framing |
| [AI / machine-learning primer](https://docs.typesafe.ai/introduction/machine-learning-primer) | Vendor explanation of RLHF, RLVR and RLCD |
| [State](https://docs.typesafe.ai/concepts/state) | Input structure and context preparation |
| [Primitives overview](https://docs.typesafe.ai/primitives) | Question design and type selection |
| [Choice](https://docs.typesafe.ai/primitives/choice) | Named alternatives and output distribution |
| [Score](https://docs.typesafe.ai/primitives/score) | Ordered levels and expected score |
| [Noul](https://docs.typesafe.ai/primitives/noul) | Boolean probability and absence of separate confidence |
| [Confidence](https://docs.typesafe.ai/confidence) | Probability-derived certainty and threshold guidance |
| [API reference](https://docs.typesafe.ai/api) | Endpoint, schemas, usage and error handling |
| [Models](https://docs.typesafe.ai/models) | Version, pricing, input modality, budgets and quotas |
| [Agent skill](https://docs.typesafe.ai/agent-skill) | Coding-agent integration guidance |
| [Jev 1.13 jaggedness](https://docs.typesafe.ai/model-jaggedness/jev-1.13) | Provider-acknowledged limitations |
| [Pre-parsed value extraction](https://docs.typesafe.ai/cookbooks/pre_parsed_value_extraction_cookbook) | Candidate extraction in code with semantic selection |
| [Introducing System One Models & Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev) | Launch, terminology, performance claims and benchmark caveats |
| [Vercel Jev model listing](https://vercel.com/ai-gateway/models/jev) | Gateway identifier, example interface and temporary promotion |

### Additional sources checked for revision 3

- [Official documentation index](https://docs.typesafe.ai/llms.txt): discovery of patterns and cookbooks; individual sources are linked in §§5, 9, 10 and 15.
- [Pydantic AI TypeSafe integration](https://pydantic.dev/docs/ai/models/typesafe/): framework mappings and execution boundaries.
- [Vercel launch announcement](https://vercel.com/changelog/typesafe-ai-jev-now-available-on-ai-gateway): SDK version, confidence metadata and gateway options.
- Rechecked [model specification](https://docs.typesafe.ai/models), [API](https://docs.typesafe.ai/api), [primitives](https://docs.typesafe.ai/primitives), [confidence](https://docs.typesafe.ai/confidence), [limitations](https://docs.typesafe.ai/model-jaggedness/jev-1.13) and [gateway listing](https://vercel.com/ai-gateway/models/jev).

### Data handling and integration boundaries

| Source | What it supports |
|---|---|
| [TypeSafe privacy policy](https://typesafe.ai/legal/privacy-policy) | Input use, retention language and US hosting |
| [TypeSafe DPA](https://typesafe.ai/legal/data-processing) | Processing roles, contractual structure and retention schedule |
| [TypeSafe legal reference](https://docs.typesafe.ai/legal) | Agreement directory and enterprise ZDR offering |
| [MCP architecture](https://modelcontextprotocol.io/specification/2026-07-28/architecture) | Host-controlled context and client/server boundaries |
| [MCP tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools) | Tool exposure and invocation model |

### Historical context for the su-lekha example

These links were retained from the original research context. Their targets are not included in this workspace; they are not required to understand Jev.

- Product document index (local-only evidence).
- Architecture, revision 2 (local-only evidence).
- Jev implementation plan, revision 2 (local-only evidence).
- Product brief, revision 5 (local-only evidence).
- Research and decision history (local-only evidence).

**Editorial scope:** all 30 transcript chapters are covered. Repeated promotion, greetings and subscription requests are omitted; sponsorship, access offers and unverifiable claims remain recorded where they affect interpretation. The original research reports that the transcripts were preserved in full; those archives are not included in this workspace.


## Local knowledge-base pipeline: live Jev use

On 19 September 2026 this project used the direct API to triage 3,358 captured Discord message IDs, with 420 successful calls for the final prompt version. Choice routes contribution types and Jev relationships; Noul flags evidence dimensions independently. The local experiment found two relationship errors in a 13-message development sample, so predictions do not automatically approve or discard evidence. This is a local implementation result, not a reproduction of community performance claims. [Implementation and limits](local-triage-experiment.md) · [Community findings](community-evidence-findings.md) · [Completion status](completion-status.md).
