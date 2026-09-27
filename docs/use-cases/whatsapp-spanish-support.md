---
id: whatsapp-spanish-support
title: "Mexican-Spanish support chats: scope and repeat detection"
category: business
evidence: author-reported
reviewed_on: 2026-09-27
independently_reproduced: false
---

# Mexican-Spanish support chats: scope and repeat detection

## What

A builder tested Jev on real Mexican-Spanish WhatsApp support conversations for an internet provider and on 1,500 summarized phone screenshots.

## How Jev fits

Scope checks and "is the bot asking the same thing again" run as typed questions; multi-intent messages get one Noul per intent plus a Choice for the main intent in one request. Screenshots are summarized first, and a separate Noul catches unknown topics that "other" misses.

## Why and impact

The author reports above 90% on both support checks with clean separation (≤0.15 vs ≥0.8) and a 155 ms p50; the same 1,500×3 batch took about 60 minutes through a free gateway and 3 minutes on the native API.

## Limits and reuse

Around 60 support cases; only the first post of the public thread was reviewed. Results are the author's.

## Sources

- [Related public project or article](https://x.com/abelardodiaz/status/2101791631590522897) — discovered via Discord source (private provenance retained locally); access: `fetched`; review: `post_text_reviewed_media_pending`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
