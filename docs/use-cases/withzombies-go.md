---
id: withzombies-go
title: "Go SDK by withzombies"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Go SDK by withzombies

## What

jev-go is an unofficial standard-library Go client for TypeSafe System One.

## How Jev fits

It returns typed Noul, Choice and Score results, accepts an explicit API key, and exposes response metadata.

## Why and impact

A CLI example recommends approve, request changes or human review from a pull-request diff.

## Limits and reuse

Retries and logging are opt-in. The triage CLI defaults to the first 24,576 bytes, limits recommendations to evaluated input and does not submit reviews.

## Sources

- [https://github.com/withzombies/jev-go](https://github.com/withzombies/jev-go) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
