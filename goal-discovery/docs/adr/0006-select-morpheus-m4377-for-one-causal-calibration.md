---
doc-role: architecture-decision-record
authority: decision
lifecycle: accepted
---
# ADR-0006: Select Morpheus M4377 for one causal calibration

**Status:** Accepted
**Date:** 2026-08 — decided before this repository had an ADR surface
**Recorded here:** 2026-09-05

## Decision

**Select Morpheus model M4377** (neuromast regeneration in zebrafish) for one bounded causal calibration. **Do not build another generator or visualizer.**

## Consequences

### Positive
- One bounded calibration against a published model, rather than more apparatus.

### Negative
- A fourth external simulator in the dependency surface.

## Research Basis

| Source | Relevance |
|--------|-----------|
| [`plans/p6_000_phenomenon_qualification.md`](../plans/p6_000_phenomenon_qualification.md) | **The decision record itself**, and a registered artifact of experiment `P6-000` in `roadmap/experiments.json`. It stays in `plans/` for that reason; this ADR points at it. |

## Related

- Experiment `P6-000` in [the experiment register](../../../roadmap/experiments.md).
- [ADR index](README.md) for the rest.

---

> **This record does not carry its source's text.** Every decision indexed here
> is a **registered experiment artifact** that stays where the experiment
> register expects it. This ADR exists so the decision is findable from a
> decision index rather than only from an experiment record — *"did we already
> evaluate Mesa?"* is a question asked by someone who does not know the file
> exists. Nothing was moved, archived or rewritten.
