---
id: lootgamebot
title: "Telegram game decisions with confidence fallback"
category: games
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Telegram game decisions with confidence fallback

## What

A Hermes agent delegates repeated game judgments to Jev.

## How Jev fits

Python composes inventory, coins, odds and history. Five Noul dice questions share a call; Choice handles craft/sell/hold. Below 0.70 the harness falls back to its LLM.

## Why and impact

Author logs approximately 700–800 ms decisions versus prior 10–30-second LLM round trips.

## Limits and reuse

Threshold and strategy are specific to this game. This does not establish universal calibration or guaranteed wins.

## Sources

- Discord source — private provenance retained locally.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
