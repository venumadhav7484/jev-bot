---
id: typesafe-chess
title: "Chess with three-move lookahead"
category: games
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Chess with three-move lookahead

## What

An experiment plays chess against Stockfish using Jev.

## How Jev fits

Author provides up to three moves of foresight and experiments with the information placed in context.

## Why and impact

Author estimates roughly 1600 Elo for that setup; useful hypothesis about external lookahead improving candidate decisions.

## Limits and reuse

No independent rating calculation, game count or engine-strength calibration verified. Do not attribute the estimate to Jev alone or compare directly to standard Elo ratings. Browser source review: Full FINDINGS.md reports strong input-representation effects: assisted suite cp loss90–106 vs279–294 raw, with code providing rules facts. Initial setups won2/44 rated-opponent games; project-calibrated Elo is not FIDE/lichess. Choice favors last-list moves15–18%; Noul still has repeat variability. Followup best-capture facts help, but additional mate/fork flags add no measurable average improvement;58games give overlapping Elo intervals and ladder-induced position confounds. Depth16 grader recheck not run. Source: https://github.com/Dimesio/typesafe-chess/blob/main/FINDINGS.md . Author report, not reproduced; PDF/rawlogs not inspected.

## Sources

- [https://github.com/Dimesio/typesafe-chess](https://github.com/Dimesio/typesafe-chess) — access: `browser_readable`; review: `implementation_report_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
