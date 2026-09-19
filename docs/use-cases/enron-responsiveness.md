---
id: enron-responsiveness
title: "Enron documents: confidence-gated legal discovery"
category: Additional reviewed applications
evidence: author-reported
reviewed_on: 2026-09-19
independently_reproduced: false
---

# Enron documents: confidence-gated legal discovery

## What

Author reports classifying 9,840 Enron documents as responsive or nonresponsive.

## How Jev fits

Binary responsiveness decision and confidence-based acceptance. Author reports 82.9% accuracy and 80.6% precision, recall and F1 across the run.

## Why and impact

Reported throughput 44.6 documents/second and cost $1.05. Accepted confidence>=95 subset reportedly reaches 93.7% accuracy, 87.5% precision, 95.5% recall within that subset and 91.3% F1.

## Limits and reuse

Signed-in Discord image inspected: chart covers 78 human-labeled documents reviewed in one window. It shows 8/14 wrong below 0.80, 0/1 wrong from 0.80 to below 0.95, and 4/63 wrong at 0.95+. Thus chart acceptance coverage is 63/78, while claimed throughput covers 9,840 processed documents. The relationship between this 78-document window and text-reported aggregate accuracy is unspecified. Do not imply all 9,840 have independently verified labels. Small selection-biased sample; subset recall is not end-to-end recall.

## Sources


Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
