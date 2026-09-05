---
doc-role: architecture-decision-record
authority: decision
lifecycle: accepted
---
# ADR-0008: Stop the internal simulator search

**Status:** Accepted
**Date:** 2026-08 — decided before this repository had an ADR surface
**Recorded here:** 2026-09-05

## Decision

**No selection.** Stop internal simulator search and trajectory generation. The near-term dependency is an external run-level evidence bundle.

## Consequences

### Positive
- Ends a search that had run through several candidates without qualifying one.

### Negative
- Leaves the programme dependent on an external bundle it does not control.

## Research Basis

| Source | Relevance |
|--------|-----------|
| [`plans/p6_003_compact_evidence_package_acquisition.md`](../plans/p6_003_compact_evidence_package_acquisition.md) | **The decision record itself**, and a registered artifact of experiment `P6-003` in `roadmap/experiments.json`. It stays in `plans/` for that reason; this ADR points at it. |

## Related

- Experiment `P6-003` in [the experiment register](../../../roadmap/experiments.md).
- [ADR index](README.md) for the rest.

---

> **This record does not carry its source's text.** Every decision indexed here
> is a **registered experiment artifact** that stays where the experiment
> register expects it. This ADR exists so the decision is findable from a
> decision index rather than only from an experiment record — *"did we already
> evaluate Mesa?"* is a question asked by someone who does not know the file
> exists. Nothing was moved, archived or rewritten.
