---
doc-role: architecture-decision-record
authority: decision
lifecycle: accepted
---
# ADR-0007: No candidate qualifies; do not install CompuCell3D

**Status:** Accepted
**Date:** 2026-08 — decided before this repository had an ADR surface
**Recorded here:** 2026-09-05

## Decision

**No candidate qualifies.** Do not install CompuCell3D, do not run M9147, and do not download either full result archive. The missing product is a compact run-level evidence package, not another simulator integration.

## Consequences

### Positive
- Stops a large integration whose output would not have been the thing needed.
- Names what is actually missing, so the next attempt targets it.

### Negative
- The evidence package it names has still not been obtained.

## Research Basis

| Source | Relevance |
|--------|-----------|
| [`plans/p6_002_archive_first_benchmark_contract.md`](../plans/p6_002_archive_first_benchmark_contract.md) | **The decision record itself**, and a registered artifact of experiment `P6-002` in `roadmap/experiments.json`. It stays in `plans/` for that reason; this ADR points at it. |

## Related

- Experiment `P6-002` in [the experiment register](../../../roadmap/experiments.md).
- [ADR index](README.md) for the rest.

---

> **This record does not carry its source's text.** Every decision indexed here
> is a **registered experiment artifact** that stays where the experiment
> register expects it. This ADR exists so the decision is findable from a
> decision index rather than only from an experiment record — *"did we already
> evaluate Mesa?"* is a question asked by someone who does not know the file
> exists. Nothing was moved, archived or rewritten.
