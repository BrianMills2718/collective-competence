---
doc-role: architecture-decision-record
authority: decision
lifecycle: accepted
---
# ADR-0001: Mesa as an optional backend, not the default

**Status:** Accepted
**Date:** 2026-08 — decided before this repository had an ADR surface
**Recorded here:** 2026-09-05

## Decision

**Mixed.** Keep Mesa as an optional backend for naturally agent-based systems. Do not make it the default architecture, and do not migrate completed experiments to it.

## Consequences

### Positive
- Mesa's activation and live controls remove real plumbing where a system is genuinely agent-based.
- Exact tick-for-tick parity against the reference backend was demonstrated before adopting it at all.

### Negative
- A second simulation backend to keep working.
- Parity must be re-established for any experiment that adopts it.

## Research Basis

| Source | Relevance |
|--------|-----------|
| [`plans/x01_mesa_decision.md`](../plans/x01_mesa_decision.md) | **The decision record itself**, and a registered artifact of experiment `X01` in `roadmap/experiments.json`. It stays in `plans/` for that reason; this ADR points at it. |
| [`plans/x01_mesa_spike.md`](../plans/x01_mesa_spike.md) | The investigation preceding this decision. |

## Related

- Experiment `X01` in [the experiment register](../../../roadmap/experiments.md).
- [ADR index](README.md) for the rest.

---

> **This record does not carry its source's text.** Every decision indexed here
> is a **registered experiment artifact** that stays where the experiment
> register expects it. This ADR exists so the decision is findable from a
> decision index rather than only from an experiment record — *"did we already
> evaluate Mesa?"* is a question asked by someone who does not know the file
> exists. Nothing was moved, archived or rewritten.
