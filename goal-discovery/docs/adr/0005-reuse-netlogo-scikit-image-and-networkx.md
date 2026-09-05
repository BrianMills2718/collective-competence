---
doc-role: architecture-decision-record
authority: decision
lifecycle: accepted
---
# ADR-0005: Reuse NetLogo, scikit-image and NetworkX

**Status:** Accepted
**Date:** 2026-08 — decided before this repository had an ADR surface
**Recorded here:** 2026-09-05

## Decision

**Reuse the standard NetLogo model, scikit-image and NetworkX** rather than building equivalents here.

## Consequences

### Positive
- No bespoke model, morphology or graph code to maintain or validate.
- The model stays comparable with its published form.

### Negative
- Adds three external dependencies to the analysis path.

## Research Basis

| Source | Relevance |
|--------|-----------|
| [`plans/p5_001_reuse_survey.md`](../plans/p5_001_reuse_survey.md) | **The decision record itself**, and a registered artifact of experiment `P5-001` in `roadmap/experiments.json`. It stays in `plans/` for that reason; this ADR points at it. |

## Related

- Experiment `P5-001` in [the experiment register](../../../roadmap/experiments.md).
- [ADR index](README.md) for the rest.

---

> **This record does not carry its source's text.** Every decision indexed here
> is a **registered experiment artifact** that stays where the experiment
> register expects it. This ADR exists so the decision is findable from a
> decision index rather than only from an experiment record — *"did we already
> evaluate Mesa?"* is a question asked by someone who does not know the file
> exists. Nothing was moved, archived or rewritten.
