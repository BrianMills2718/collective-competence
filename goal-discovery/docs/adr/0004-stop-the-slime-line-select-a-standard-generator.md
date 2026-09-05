---
doc-role: architecture-decision-record
authority: decision
lifecycle: accepted
---
# ADR-0004: Stop the Slime line; select a standard generator

**Status:** Accepted
**Date:** 2026-08 — decided before this repository had an ADR surface
**Recorded here:** 2026-09-05

## Decision

**Stop the current Slime line after P3-006.** Select the installed, standard generator instead of continuing a bespoke one.

## Consequences

### Positive
- Ends an line that was not producing decision-changing evidence.

### Negative
- The Slime results stand but the route is closed; reopening needs a stated condition.

## Research Basis

| Source | Relevance |
|--------|-----------|
| [`plans/p4_generator_selection.md`](../plans/p4_generator_selection.md) | **The decision record itself**, and a registered artifact of experiment `P4-generator-selection` in `roadmap/experiments.json`. It stays in `plans/` for that reason; this ADR points at it. |
| [`plans/p3_generator_reuse_survey.md`](../plans/p3_generator_reuse_survey.md) | The investigation preceding this decision. |

## Related

- Experiment `P4-generator-selection` in [the experiment register](../../../roadmap/experiments.md).
- [ADR index](README.md) for the rest.

---

> **This record does not carry its source's text.** Every decision indexed here
> is a **registered experiment artifact** that stays where the experiment
> register expects it. This ADR exists so the decision is findable from a
> decision index rather than only from an experiment record — *"did we already
> evaluate Mesa?"* is a question asked by someone who does not know the file
> exists. Nothing was moved, archived or rewritten.
