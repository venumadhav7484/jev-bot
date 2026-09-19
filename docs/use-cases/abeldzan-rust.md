---
id: abeldzan-rust
title: "jev-rs: async-first Rust SDK"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# jev-rs: async-first Rust SDK

## What

The repository documents an async-first TypeSafe Rust client with an optional blocking client.

## How Jev fits

It exposes typed System One questions, reusable question collections, model discovery and configurable retries.

## Why and impact

Structured errors and retained HTTP metadata support integration diagnostics.

## Limits and reuse

The crate is not yet published to crates.io; transient failures retry by default, and the billable live integration test is ignored unless explicitly requested.

## Sources

- [https://github.com/abeldzan/jev-rs](https://github.com/abeldzan/jev-rs) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
