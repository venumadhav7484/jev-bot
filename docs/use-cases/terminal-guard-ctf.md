---
id: terminal-guard-ctf
title: "JevGuard: shell-vetting CTF"
category: security
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# JevGuard: shell-vetting CTF

## What

A challenge app places Jev before commands in an isolated sandbox.

## How Jev fits

Participants can vary the vetter and test whether command decisions can be bypassed.

## Why and impact

Useful adversarial-testing concept for probabilistic guardrails.

## Limits and reuse

The saved challenge screenshot shows a direct flag-read command blocked, followed by an allowed script-write and script-execution sequence that displays the synthetic flag. This is observed demonstration evidence of a multi-step bypass, not an independently repeated attack. Per-command judgments cannot establish secure containment without stateful controls. This project is distinct from the jev-guard harness repository and the Android APK app.

## Sources

- [https://jevguard.vercel.app/](https://jevguard.vercel.app/) — access: `fetched`; review: `source_text_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
