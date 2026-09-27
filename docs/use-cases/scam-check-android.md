---
id: scam-check-android
title: "Scam Check: phone-side gate, then Jev on risky texts"
category: security
evidence: author-reported
reviewed_on: 2026-09-27
independently_reproduced: false
---

# Scam Check: phone-side gate, then Jev on risky texts

## What

An Android app and paste-in tool warn when a text message or email looks like a scam.

## How Jev fits

Phone-side code checks links, numbers and pay-now wording first; only risky-looking messages go to Jev, with links, numbers and emails hidden. Jev answers six plain questions (asking you to act, after your codes, rushing you, offering money, personal opener, impersonating a bank or courier) and code maps them to likely scam, be careful or looks ordinary with reasons.

## Why and impact

In a pre-registered live run, it caught 83.2% of modern scams against 54.4% for a classifier trained on older SMS, while warning on 9.0% of ordinary messages (limit 10%).

## Limits and reuse

On modern scams Jev did only a little better than keyword rules answering the same six questions; ordinary messages drew more warnings than baselines. One recorded run on public data.

## Sources

- [Release v0.1.3 · jonny5isalive5/jev-scam-triage](https://github.com/jonny5isalive5/jev-scam-triage/releases/latest) — access: `fetched`; review: `not_reviewed`.
- [GitHub - jonny5isalive5/jev-scam-triage: jev-scam-blocker](https://github.com/jonny5isalive5/jev-scam-triage) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
