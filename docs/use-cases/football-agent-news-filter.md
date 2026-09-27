---
id: football-agent-news-filter
title: "Fantasy football agent: Jev filters news before Claude reasons"
category: filtering
evidence: author-reported
reviewed_on: 2026-09-27
independently_reproduced: false
---

# Fantasy football agent: Jev filters news before Claude reasons

## What

An AI general manager for fantasy football leagues pulls NFL headlines from six feeds; most name-matched articles are noise.

## How Jev fits

Twenty headlines go out in one request, each with its own Choice (injury, role change, transaction, speculation, team context, noise) carrying its headline so answers cannot cross-map. Only a confident “noise” (0.70 or above) is dropped; timeouts, missing keys and unparseable answers keep the article. Labels are cached as facts about the article, while each manager’s preference for speculation stays in their own strategy document.

## Why and impact

The expensive reasoning model now reads only the headlines that can change a lineup call, and the fail-open rule keeps a missed injury report from being the cheap mistake.

## Limits and reuse

Author-described design; no accuracy or cost comparison published. The public dashboard marks later weeks and outcomes as illustrative. Fail-open filtering trades cost for recall by design.

## Sources

- [AI Fantasy Football GM for Sleeper Leagues | Fantasy Agent](https://footballagent.tech/) — access: `fetched`; review: `landing_page_reviewed`.
- [#ai #aiengineering #typesafeai #python #machinelearning | Niam LeSt...](https://www.linkedin.com/feed/update/urn:li:activity:7508970359300304896/) — access: `fetched`; review: `post_text_reviewed`.
- [static.licdn.com](https://static.licdn.com/aero-v1/sc/h/c45fy346jw096z9pbphyyhdz7) — access: `asset_no_text`; review: `excluded_asset`.
- [Related public project or article](https://www.linkedin.com/feed/update/urn:li:activity:7508970359300304896) — discovered via Discord source (private provenance retained locally); access: `fetched`; review: `post_text_reviewed`.

Access and review are separate. A returned page may contain only metadata. Source register (local-only evidence) · Review notes (local-only evidence).
