---
id: tic-tac-toe
title: "Elixir agents playing Tic Tac Toe"
category: games
evidence: author-reported
reviewed_on: 2026-09-20
independently_reproduced: false
---

# Elixir agents playing Tic Tac Toe

## What

An Elixir demo uses Jido and ReqLLM.

## How Jev fits

Each game agent queries Jev for its next move.

## Why and impact

Simple example of actor-based game orchestration with typed choices.

## Limits and reuse

Recorded self-play contains decisive wins for both sides, so perfect play is not established. No controlled move-optimality or win-rate evaluation; human pacing and fast mode differ.

## Sources

- Discord source — private provenance retained locally.
- [https://x.com/mikehostetler/status/2100946109308748079](https://x.com/mikehostetler/status/2100946109308748079) — access: `fetched`; review: `demo_trace_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
