---
doc-role: architecture-decision-record
authority: decision
lifecycle: accepted
---
# ADR-0003: Adopt a small visual-analytics stack

**Status:** Accepted
**Date:** 2026-08 — decided before this repository had an ADR surface
**Recorded here:** 2026-09-05

## Decision

**Adopt a deliberately small stack.** Panel/HoloViews passed; the fallback survey is stopped.

## Consequences

### Positive
- One stack, chosen once, rather than a renderer per experiment.

### Negative
- Panel/HoloViews sit behind an optional extra, which is how the suite became uncollectable on a clean checkout (failure log F4).

## Research Basis

| Source | Relevance |
|--------|-----------|
| [`plans/x03_visual_analytics_decision.md`](../plans/x03_visual_analytics_decision.md) | **The decision record itself**, and a registered artifact of experiment `X03` in `roadmap/experiments.json`. It stays in `plans/` for that reason; this ADR points at it. |

## Related

- Experiment `X03` in [the experiment register](../../../roadmap/experiments.md).
- [ADR index](README.md) for the rest.

---

> **This record does not carry its source's text.** Every decision indexed here
> is a **registered experiment artifact** that stays where the experiment
> register expects it. This ADR exists so the decision is findable from a
> decision index rather than only from an experiment record — *"did we already
> evaluate Mesa?"* is a question asked by someone who does not know the file
> exists. Nothing was moved, archived or rewritten.
