# Cached-source grounding pilot

The pipeline separates evidence capture, Jev judgments, assistant drafting, citation validation and editorial review. It uses the existing frozen archive; it does not collect new Discord source messages or change the capture checkpoint.

## Measured run — 19 September 2026

| Measure | Result |
|---|---|
| Sample | 30 distinct cached texts; 33 registered URL aliases |
| Jev triage | 30 successful requests in 12.46 seconds |
| Jev claim/caveat checks | 30 successful requests in 10.61 seconds |
| Drafts | 30 provisional write-ups; 130 attributed claims, inferences and explicit unknowns |
| Total API usage | 206,033 input tokens; 8,600 output tokens |
| Estimated Jev cost | $0.008653386, excluding Codex usage, tax and other infrastructure |
| Editorial result | Complete cached text read for all 30; 19 existing cases updated |
| Independent implementation verification | None |

Cost uses the published $0.042 per million input tokens, with output free, checked on the run date. This is a usage-based estimate, not an invoice. [TypeSafe models](https://docs.typesafe.ai/models).

The sample was a deterministic stratified selection from unreviewed cached texts of 1,000–20,000 characters. It excludes blocked sources, binary media and long or truncated captures. It is not representative of the full backlog.

## What worked and what did not

Code verifies source hashes, contiguous passage offsets, required fields and exact quotation matches. This prevents fabricated passage references; it does not establish that a quote entails a claim. Jev evaluates each claim and flags caveats. The same Codex session drafted and reviewed the narratives; that is not independent validation.

The initial review rules sent **all 30 sources** to deep review. Every source triggered the broad missing-detail question. Consequently, this pilot has **not demonstrated a reduction in review workload**. Review thresholds are experimental, not calibrated. Keep Jev checks advisory while testing narrower questions on a separately labeled sample. No historical manual timing baseline was available, so no end-to-end speedup is claimed. API timing excludes drafting, reading and editorial work; it is not total task duration.

Source review produced useful corrections: comparison-only Jev integrations must not become enforcement claims; fixture demos must not become live model tests; development-set benchmarks must retain tuning and sample-size caveats. Follow-up source inspection resolved a robotics conflict: its Jev path receives scripted text hints and image length, selects preset angles, and declares completion after four steps. The README does not establish raw-image Jev perception. [Inspected code](https://github.com/opaielsheikh/zero-shot-vision-robotics/blob/main/vision_robotics/agent.py). [State documentation](https://docs.typesafe.ai/concepts/state).

## Run on an authorized private archive

```sh
python3 scripts/source_pilot.py prepare --count 30
python3 scripts/source_pilot.py triage --max-requests 30 --max-input-bytes 1500000 --workers 3
python3 scripts/source_pilot.py packet
# Have an authorized drafting assistant read the packet and write the JSON drafts.
python3 scripts/source_pilot.py import-drafts /absolute/path/to/drafts.json
python3 scripts/source_pilot.py check --max-requests 30 --max-input-bytes 1500000 --workers 3
python3 scripts/source_pilot.py report
```

Use a new `--work` directory for a new pilot. Existing manifests are immutable. Successful request hashes are cached; changed source or draft content invalidates the relevant checks. Failed or uncertain calls are recorded and never retried automatically. Request and byte ceilings bound each run. Bytes are a conservative transport bound, not a token estimate.

Drafts require `what`, `how`, `why_impact` and `limits`. Claims carry source-version-specific passage citations and explicit `source_claim`, `editorial_inference` or `unknown` labels. Reports produce provisional Markdown and a review queue under the ignored private research directory. Editorial decisions remain separate from machine suggestions and cannot be created by these commands.

This version uses Codex-session drafting with no separate generative API. It is not an unattended narrative-generation service. The user-facing bot remains the existing local template-and-evidence assistant, optionally routed by Jev. Media still requires visual inspection, OCR or transcription before text-based Jev assessment.
