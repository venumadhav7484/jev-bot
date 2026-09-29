# Bharat test: can a half-second judgment model read Indian languages?

An experiment with **Jev** (TypeSafe's decision model, `jev-1.13.0`), run zero-shot: no fine-tuning, no examples, no translation step. Pass lines were written into [PLAN.md](PLAN.md) before the first test request, and every headline number is recomputed from the raw logs by separate verification scripts.

## Results

**1. Topic tagging, SIB-200** (204 sentences × 24 Indian-language test sets, 19 of India's 22 scheduled languages)
- Above GPT-4's published zero-shot score (gpt-4-0613, SIB-200 paper) in all 21 test sets that counted, and in 24 of 24 overall.
- 10 most-spoken languages: 89.9% vs 71.8% for GPT-4. Telugu 92.2%, Hindi 89.7%, English 89.2%.

**2. Voice-assistant intents, MASSIVE** (2,974 requests per language, 60 intents, 7 languages spoken in India)
- Jev averaged 80.1%. Published XLM-R base trained on English only scored 68.0%; trained on each language, 84.3%.

**3. Against today's models** (the same 5,100 SIB-200 requests and instructions, 30 Sep 2026)

| | Jev | gpt-6-astra | GLM 5.3 |
|---|---|---|---|
| Accuracy, 10 most-spoken languages | 89.9% | 88.6% | 87.5% |
| Accuracy, all 24 Indian sets | 85.4% | 88.3% | 85.9% |
| Cost per 1,000 requests | $0.026 | $3.28 | $0.54 |
| Median time per request | 0.39 s | 2.10 s | 1.97 s |

The flagship wins clearly on rare scripts, for example Santali 87.7% vs 19.1%.

**Limits.** These are narrow tasks (topic tagging and intent routing). GPT-4's numbers are published results that used different prompts. The benchmarks are public, so training-data overlap can't be ruled out. Latency figures are medians over public APIs from one location.

## Layout

| Path | What it holds |
|---|---|
| `PLAN.md` | Pre-registration, pass lines and the dated status log |
| `src/` | Runners (`run_stage1.py`, `run_stage2.py`, `rivals.py`), reports, independent verifiers, frozen specs (`published.json`, `intents.json`), `fetch_data.py` |
| `runs/` | Results (`results*.json`) and raw decision logs (`*_raw.jsonl`, `rival_*.jsonl`) |
| `video/` | The 86 s video, its thumbnail, and the renderer (`frame_v2.html` + `capture.py`, headless Chrome; `music.py` composes the original soundtrack) |
| `tests/` | Unit tests |

## Reproduce

```bash
cd src
python fetch_data.py                                 # SIB-200 + MASSIVE (not stored in this repo)
python run_stage1.py && python report.py && python verify.py
python run_stage2.py && python report2.py && python verify2.py
python rivals.py openai --langs <all 25> && python rivals.py glm --langs <all 25>
python report3.py && python verify3.py
```

Keys are read from environment variables, or from a git-ignored `.env` in this folder: `JEV_API_KEY`, `OPENAI_API_KEY`, `glm_key`. The verifiers also accept an optional path to the paper's extracted text to re-check the published numbers.

## Data and credits

- SIB-200 (Adelani et al., EACL 2024), data under CC BY-SA 4.0 from FLORES-200.
- MASSIVE (FitzGerald et al., ACL 2023), CC BY 4.0.
- Published comparison numbers are cited from those papers. The datasets are downloaded by `fetch_data.py` and aren't redistributed here.
