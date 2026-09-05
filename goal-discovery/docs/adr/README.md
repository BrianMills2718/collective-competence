---
doc-role: adr-index
authority: canonical
lifecycle: active
---
# Architecture Decision Records

Installed 2026-09-05 from enforced-planning's ADR pattern — the ecosystem's
**adopted, owned** mechanism for this (`capability_ownership_registry.yaml`:
`enforced-planning.adr_pattern`, `decision_status: adopted`, *"the most
mechanically portable governance artifact found in this ecosystem"*). This
repository did not invent a decision surface; it installed the existing one.

**These ADRs cite; they do not absorb.** Every decision indexed here is already a
**registered experiment artifact** in `roadmap/experiments.json` and stays where
the experiment register expects it. Nothing was moved, archived or rewritten to
build this index.

**ADRs are immutable.** If a decision changes, write a new one that supersedes it.

| ADR | Decision | Experiment | Status |
|-----|----------|------------|--------|
| [0001](0001-mesa-as-optional-backend-not-default.md) | Mesa as an optional backend, not the default | `X01` | Accepted |
| [0002](0002-adopt-netlogo-for-visual-prototyping.md) | Adopt NetLogo for visual prototyping | `X02` | Accepted |
| [0003](0003-adopt-a-small-visual-analytics-stack.md) | Adopt a small visual-analytics stack | `X03` | Accepted |
| [0004](0004-stop-the-slime-line-select-a-standard-generator.md) | Stop the Slime line; select a standard generator | `P4-generator-selection` | Accepted |
| [0005](0005-reuse-netlogo-scikit-image-and-networkx.md) | Reuse NetLogo, scikit-image and NetworkX | `P5-001` | Accepted |
| [0006](0006-select-morpheus-m4377-for-one-causal-calibration.md) | Select Morpheus M4377 for one causal calibration | `P6-000` | Accepted |
| [0007](0007-no-candidate-qualifies-do-not-install-compucell3d.md) | **No candidate qualifies; do not install CompuCell3D** | `P6-002` | Accepted |
| [0008](0008-stop-internal-simulator-search.md) | **Stop the internal simulator search** | `P6-003` | Accepted |

## Statuses

| Status | Meaning |
|--------|---------|
| Proposed | Under discussion |
| Accepted | Decision made, in effect |
| Deprecated | No longer applies |
| Superseded | Replaced by another ADR |

## Why this index exists at all

Four of the eight are **negative** decisions — *do not install CompuCell3D*,
*stop the internal simulator search*, *stop the Slime line*, *do not make Mesa
the default*. Those are the most valuable entries, because they exist to stop the
same evaluation being run twice.

Their problem was never that they were lost. It was that *"did we already
evaluate Mesa?"* is asked by someone who does not know the file exists, and the
answer sat in `docs/plans/` where a reader looking for plans finds it and a
reader looking for a decision does not.

## What belongs here, and what does not

**Here:** architecture and tooling decisions — what to build on, what to adopt,
what to stop building.

**Not here:** research-direction decisions, which have owners already.

| Decision kind | Owner |
|---|---|
| What the programme is betting on | [conjecture register](../../../wiki/conjectures.md) |
| Scope and scientific boundary | [charter](../PROJECT.md) |
| What stopped and what it still costs | [failure log](../../../wiki/failure-log.md) |
| The next action | [current plan](../plans/current_research_plan.md) |
| A live design argument in progress | [substrate design](../../../wiki/substrate-design.md) |

`p2_research_pivot.md` was a candidate and was **rejected on this rule**: pivoting
away from the thermostat family is research direction, not architecture. It stays
a plan.

The registry records the same boundary from the other side: *"one ADR = one
decision/doc. Does not natively support indexing many fine-grained propositions
raised within a single discussion"* — which is what the substrate design document
does, so that stays as it is.

## Creating a new one

```bash
cp goal-discovery/docs/adr/TEMPLATE.md goal-discovery/docs/adr/0009-my-decision.md
# fill in Context, Decision, Consequences, Research Basis; Status: Proposed
# add a row above; set Accepted when the decision is made
```
