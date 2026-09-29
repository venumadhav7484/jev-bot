# Bharat test: plan and pre-registration

Started 29 September 2026. Private working folder; not a git repository. Uses open data and the Jev API only.

## 1. Question

Can Jev, with no training in any Indian language, understand text in Indian languages? The benchmark is SIB-200, where the same 204 professionally translated sentences are labelled with one of 7 topics.

## 2. Data (user approved the download, 2.52 MB)

- **SIB-200** (Adelani et al., EACL 2024), from `huggingface.co/datasets/Davlan/sib200`, CC BY-SA 4.0. We use the `test.tsv` split (204 sentences per language) and `dev.tsv` (99 sentences, smoke tests only).
- **English plus 24 Indian-language sets:** asm_Beng, awa_Deva, ben_Beng, bho_Deva, guj_Gujr, hin_Deva, hne_Deva, kan_Knda, kas_Arab, kas_Deva, mag_Deva, mai_Deva, mal_Mlym, mar_Deva, mni_Beng, npi_Deva, ory_Orya, pan_Guru, san_Deva, sat_Olck, snd_Arab, tam_Taml, tel_Telu, urd_Arab.
- **Topics:** science/technology, travel, politics, sports, health, entertainment, geography.

## 3. Method (fixed before any test run)

- One Jev request per sentence. The state is `{"text": <sentence>}`, with one Choice question over the 7 topics in the order of `labels.txt`.
- The instructions say the text may be in any language or script. The same short topic descriptions are used in every language.
- No examples, no translation step and no tuning on test data. The dev set is used only to check that requests and parsing work.
- A failed request counts as wrong.

## 4. Score to beat

GPT-4 (`gpt-4-0613`) zero-shot accuracy per language, from SIB-200 Table 11. These scores are stored in `published.json`, along with GPT-3.5 zero-shot and supervised XLM-R for context. Models trained on 701 labelled sentences per language score 85–91%; that isn't our comparison.

## 5. Pass lines (stage 1; stop at the first miss)

| # | Check | Pass line |
|---|---|---|
| P1 | Jev accuracy is strictly above GPT-4's published zero-shot accuracy | In ≥ 14 of the 21 Indian-language sets where GPT-4 scored ≥ 40% |
| P2 | Mean accuracy over the 10 most-spoken (hin, ben, mar, tel, tam, guj, urd, kan, ory, mal) | ≥ 72.0% (GPT-4 averages 71.8%) |

- The sets excluded from P1 are sat_Olck (GPT-4 0%), mni_Beng (6.9%) and kas_Deva (21.7%), so that near-zero GPT-4 scores don't give Jev free wins.
- All 24 sets are still run and reported; none are hidden.
- English is reported for context only.

## 6. Stage 2: a separate experiment, only if stage 1 passes (download approved, 40.3 MB)

- **Data:** Amazon MASSIVE v1.1 (CC BY 4.0), full test sets for en-US and 7 languages spoken in India (hi-IN, te-IN, ta-IN, kn-IN, ml-IN, bn-BD, ur-PK). That's 2,974 utterances per language and 60 intents.
- **Method:** one Choice over 60 intents per utterance. Intent descriptions are written from the intent names and the English training split, then frozen before any test run.
- **Rival:** XLM-R base trained on English only (MASSIVE Table 8, zero-shot): hi 74.8, ml 70.1, te 68.2, ta 68.1, bn 66.0, ur 65.6, kn 63.5.
- **Pass line:** Jev beats XLM-R zero-shot in ≥ 5 of the 7 languages.
- Stage 2 is reported to the user either way. Only a pass may appear in a post, and it's labelled as its own test.

## 7. After a pass: showcase

- **Video:** a 12–14 s before/after. A stream of messages in 24 scripts goes first into an English-only pipeline (it can't read them), then into Jev (topics appear). A scoreboard against GPT-4 follows, using language tiles rather than a map.
- **Post:** a first-person story, using measured numbers only.
- **Credit:** SIB-200 / FLORES-200, CC BY-SA 4.0.

## 8. Verification

- `src/verify.py` recomputes every number independently from the raw logs.
- Check the published table values against the paper text.
- Scan outputs for keys.
- Check the video frames.
- Check that every number in the post appears in `results.json`.

## 9. Status log

- 29 Sep: plan written. Downloads approved (stage 1 now; stage 2 only on a stage-1 pass).
- 29 Sep: data downloaded (2,515,733 bytes, 25 × test/dev/labels) and 4 unit tests pass. Dev smoke test on 20 sentences, 5 each in English, Hindi, Telugu and Santali: all 20 requests succeeded, 0.34–0.46 s, 524–853 input tokens. Method frozen unchanged; test run started.
- 29 Sep, **stage 1 (5,100 test sentences): PASSED.** 5,100 requests succeeded with 0 failures; p50 0.39 s, p95 0.62 s; 3.15M tokens, $0.13.
  - **P1:** Jev beat GPT-4's published zero-shot score in 21 of 21 counted sets (all 24 overall).
  - **P2:** 89.85% mean over the 10 most-spoken languages, vs 71.78% for GPT-4.
  - English 89.2% (GPT-4 76.6%). Across all 24 Indian sets, 85.4% vs 59.7%.
  - Worst: Santali 19.1% (≈ chance; GPT-4 0%) and Meitei 70.1% (GPT-4 6.9%).
  - Indian scripts cost 1.11–1.20× English tokens (Santali 1.63×).
  - `verify.py` confirms all 25 accuracies, all 25 published values against the paper text and both pass lines. No key in any file.
  - **Caveats to state:** different prompts from the paper's GPT-4 setup; GPT-4 is the June 2023 version; the benchmark is public, so overlap with Jev's training data can't be ruled out.
- 29 Sep, stage 2 setup: MASSIVE downloaded (40,251,390 bytes). Intent descriptions were frozen in `src/intents.json` (from names and English train examples only). Dev smoke test: 24 utterances in en-US, hi-IN and te-IN; 23 correct; ~1,600 input tokens and 0.34–0.95 s per request. Estimated full run: 23,792 requests, ≈ $1.60.
- 29 Sep, video: `video/bharat_test.mp4` (14.0 s, 1080×1350, H.264, 1.0 MB). It's rendered from `frame.html` by one headless Chrome over the DevTools protocol (`capture.py`), because Pillow here can't shape Indian scripts. All on-screen numbers come from `data.js`, which is built from `runs/results.json` by `build_data.py`. Example cards are real test sentences that Jev answered correctly (cherry-picked examples, labelled as real answers; the aggregates cover all 5,100). Thumbnail: `video/poster.png`.
- 29 Sep, post: `post/POST.md`, a first-person story using stage 1 numbers only; stage 2 is not mentioned unless it passes.
- 29 Sep, **stage 2 (MASSIVE, 23,792 utterances): PASSED.**
  - All 23,792 requests succeeded; p50 0.38 s; 38.7M tokens, $1.62.
  - **P3:** Jev beat XLM-R trained on English only in 7 of 7 Indian locales. Mean 80.1% vs 68.0% (hi 81.6/74.8, te 81.0/68.2, ta 78.7/68.1, kn 79.5/63.5, ml 81.5/70.1, bn 79.0/66.0, ur 79.2/65.6). English: 85.0%.
  - Still below XLM-R trained on each language's own data (mean 84.3%).
  - `verify2.py` confirms all 8 accuracies and every published value against the paper's Table 8.
  - **Total spend for the project:** ≈ $1.76.
- 30 Sep, video updated at the user's request: a new 4.5 s scene for stage 2 (voice requests), now 19.0 s long and 1.35 MB. It shows two real Telugu requests Jev routed correctly (MASSIVE ids 4313 and 12121, English glosses marked "translation"), then all 7 languages: Jev bars against the English-only XLM-R bars, with a white line for XLM-R trained on each language (the honest gap). The summary gained a voice line and MASSIVE credit. All numbers come from `runs/results_stage2.json` through `build_data.py`.

## 10. Version 2 (30 Sep, user request)

- **Video:** slower (~60 s), 8 scenes: problem → objective → solution/setup → examples → vs GPT-4 (published) → voice → vs today's models → conclusion. Original background music composed in code (no third-party audio).
- **Fact fix:** India has 22 *scheduled* languages (Eighth Schedule); the Union's official languages are Hindi and English. Our 24 test sets cover 23 languages (Kashmiri in two scripts). That's 19 of the 22 scheduled languages (SIB-200 has no Bodo, Dogri or Konkani) plus Awadhi, Bhojpuri, Chhattisgarhi and Magahi.
- **Stage 3, a comparison with current models:** the latest OpenAI GPT, the latest Gemini and GLM 5.3, on the same 5,100 SIB-200 sentences with the same instructions and topic list, zero-shot. Measure accuracy, cost per 1,000 sentences and latency.
- **No pass line (user's choice):** "facts are facts". Results are reported as measured, and the conclusion is written from them.
- 30 Sep, stage 3 setup: Gemini skipped (user). Rivals are gpt-6-astra (OpenAI flagship; Responses API, reasoning effort low; key from a local .env) and glm-5.3 (reasoning_effort low). Prompt: the same instructions and 7 topic descriptions Jev gets, plus "answer with exactly one topic name". Dev probe on 20 sentences: both 20/20. gpt-6-astra ~216 input and 7 output tokens, $2.51 per 1,000, 2.2 s; GLM 314 input and 13 output tokens, $0.50 per 1,000, 2.6 s. User approved all 25 test sets (5,100 sentences each), ≈ $15.40.
- 30 Sep, video v2 edits (user): every scene holds 4 s after its last animation before fading out (total ≈ 86 s with scenes 7–8). Telugu and Hindi are highlighted in both scoreboards. English is added as an unhighlighted reference row on the GPT-4 scoreboard (Jev 89.2 vs GPT-4 76.6). The callout reads "Telugu +23.8 · Hindi +10.4 points".
- 30 Sep, **stage 3 done** (all 5,100 requests per model succeeded; GLM needed 29 retries after rate limits; `verify3.py` passes).
  - Mean accuracy on the 10 most-spoken languages: Jev 89.85, gpt-6-astra 88.56, glm-5.3 87.51.
  - All 24 Indian sets: gpt-6-astra 88.31, glm-5.3 85.85, Jev 85.37.
  - English: 89.2, 88.2, 85.3.
  - Cost per 1,000 requests: $0.026, $3.28 (127×), $0.54 (21×).
  - p50 latency: 0.39 s, 2.10 s (5.4×), 1.97 s (5.1×).
  - Rare scripts favour the flagship: Santali 19.1 vs 87.7, Meitei 70.1 vs 86.3, Kashmiri (Devanagari) 80.4 vs 89.2.
  - Spend: gpt $16.75, glm $2.78.
- 30 Sep, an independent editor review (Sonnet) of the article draft; fixes applied:
  - "never taught" instead of "never trained".
  - Latency given as a median, and "requests" rather than "sentences".
  - The hand-picked example labelled as such.
  - XLM-R base named.
  - English row added to the voice chart.
  - Author's feelings moved into ✍ slots.
  - Fewer chart rows for mobile.
  - The per-request token wording fixed.
