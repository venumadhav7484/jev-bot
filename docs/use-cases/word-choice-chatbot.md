---
id: word-choice-chatbot
title: "Word-choice chatbot experiment"
category: experiments
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Word-choice chatbot experiment

## What

Produce text by repeatedly selecting from a vocabulary.

## How Jev fits

A community project organizes roughly 30,000 words into meaning groups and chains choices.

## Why and impact

The author reports approximately $0.003 per reply but weak grammar.

## Limits and reuse

This is a workaround, not native generation. For Jev-bot, use a generative model for conversation and Jev for bounded decisions. Source review: Jev can select words through a wrapper but this does not establish useful free-form generation. Stored replies work only when a fitting answer exists. Preprocessing uses other models; reported provider costs and tiny test set do not establish production costs or accuracy.

## Sources

- [https://github.com/finetuningsingh/jev-chatbot](https://github.com/finetuningsingh/jev-chatbot) — access: `fetched`; review: `readme_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
