---
doc_role: active_authority
authority: canonical_if_merged
status: accepted
date: 2026-10-05
reversible: true
---
# Decision 0001 — Native authorities with a derived navigational wiki

## Context

Collective Competence accumulated useful experiment records, plans, audits, generated status views, and wiki syntheses. The hot wiki was later compressed to reduce reading cost, but `wiki/current.md` and `wiki/findings.md` still described themselves as owners of mutable project truth.

The canonical Agentic Engineering System uses a stricter separation: native artifacts own decisions, plans, implementation, verification, and evidence; the wiki is progressive-disclosure navigation over those authorities.

## Decision

Adopt that separation here without importing the AES runtime or creating a parallel framework.

- `wiki/` is **derived navigation and synthesis**. It does not authorize implementation or overrule native evidence.
- Current bounded future work is authorized by accepted records under `docs/plans/`.
- Durable repository-level choices live under `docs/decisions/`.
- A native experiment README owns the interpretation/limits of that experiment; its code owns procedure, tests own software/intervention contracts, and committed result artifacts own observations.
- Plan completion does **not** establish a scientific finding or close a scientific gap. Fresh observations and experiment interpretation do.
- Historical `goal-discovery/docs/plans/`, audits, scoreboards, and state snapshots remain provenance. They are not silently rewritten into the new plan system.
- `.agentic/relationships.yaml` records the minimal machine-readable graph among current decisions, plans, experiments, code, tests, evidence, and derived wiki routes.

## Consequences

A reader may start at `wiki/index.md`, but consequential claims must follow links to native owners. New code or experiment work should name the accepted plan that authorizes it, unless the change is ordinary maintenance with no new scientific scope.

The hot wiki should become easier to regenerate/review because it carries less independent state.
