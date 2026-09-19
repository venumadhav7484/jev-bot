---
id: java-sdk
title: "Community Java SDK with Spring Boot starter"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Community Java SDK with Spring Boot starter

## What

An independent community Java client supports TypeSafe System One requests; it requires Java 17 or newer and Jackson.

## How Jev fits

The client exposes Noul, Choice and Score, batches questions over shared state, and offers Spring Boot configuration.

## Why and impact

The API intentionally follows official Python and JavaScript SDK conventions to make integrations read similarly.

## Limits and reuse

The project explicitly lacks TypeSafe affiliation or endorsement. Default retries cover connection failures and timeouts; the README describes stub-server tests, not a live reliability benchmark.

## Sources

- [https://github.com/Premo-Cloud/typesafe-sdk-java](https://github.com/Premo-Cloud/typesafe-sdk-java) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
