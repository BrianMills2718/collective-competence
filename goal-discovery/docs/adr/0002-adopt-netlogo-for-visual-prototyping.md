---
doc-role: architecture-decision-record
authority: decision
lifecycle: accepted
---
# ADR-0002: Adopt NetLogo for visual prototyping

**Status:** Accepted
**Date:** 2026-08 — decided before this repository had an ADR surface
**Recorded here:** 2026-09-05

## Decision

**Adopt NetLogo for Experiment 003's visual prototype.** Keep Python as the analysis and evidence layer.

## Consequences

### Positive
- An off-the-shelf environment supplies model execution and visualisation without bespoke code.

### Negative
- A NetLogo dependency the environment must supply; sixteen tests skip without it.

## Research Basis

| Source | Relevance |
|--------|-----------|
| [`plans/x02_netlogo_decision.md`](../plans/x02_netlogo_decision.md) | **The decision record itself**, and a registered artifact of experiment `X02` in `roadmap/experiments.json`. It stays in `plans/` for that reason; this ADR points at it. |
| [`plans/x02_netlogo_calibration.md`](../plans/x02_netlogo_calibration.md) | The investigation preceding this decision. |

## Related

- Experiment `X02` in [the experiment register](../../../roadmap/experiments.md).
- [ADR index](README.md) for the rest.

---

> **This record does not carry its source's text.** Every decision indexed here
> is a **registered experiment artifact** that stays where the experiment
> register expects it. This ADR exists so the decision is findable from a
> decision index rather than only from an experiment record — *"did we already
> evaluate Mesa?"* is a question asked by someone who does not know the file
> exists. Nothing was moved, archived or rewritten.
