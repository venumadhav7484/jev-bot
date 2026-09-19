---
id: noisegate
title: "JevNoiseGate: Android notification and SMS filtering"
category: content
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# JevNoiseGate: Android notification and SMS filtering

## What

An Android app classifies distracting notifications and SMS advertisements.

## How Jev fits

The inspected README describes a shared decision pipeline: local OTP bypass, local sender rules, then model classification using message, channel history and user preferences. Uncertain decisions and network failures allow the notification.

## Why and impact

The reusable pattern combines deterministic exceptions with semantic filtering. No independently measured accuracy or productivity gain is available.

## Limits and reuse

Early, single-device project. Notifications appear before cancellation; SMS messages remain in the inbox. README discloses plaintext credentials in private app storage. Privacy and blocking behavior were not tested.

## Sources

- Discord source — private provenance retained locally.
- [https://github.com/ufec/jev-block-android-ad](https://github.com/ufec/jev-block-android-ad) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
