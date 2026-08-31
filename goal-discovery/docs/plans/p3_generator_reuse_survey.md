---
doc-role: historical-plan-or-decision
authority: historical
lifecycle: retained
---
> Historical record. Its next-step language describes the decision at the time,
> not an active assignment. See the [current plan](current_research_plan.md)
> and [evidence index](plan_completion_ledger.md).


# Phase 3 generator reuse survey

## Capability card

1. **Question:** can an off-the-shelf decentralized system generate a dynamic
   macro-pattern whose perturbation response is not already exhausted by a
   simple reachability invariant?
2. **Input/output:** seeded standard model plus one deterministic branch
   intervention; export a trajectory of observable collective organization.
3. **Useful evidence:** a visible macro-pattern, a measurable disturbance, and
   nontrivial recovery or reorganization without adding a controller.
4. **Stop conditions:** hand-authored goal logic, no reproducible batch path,
   no trajectory boundary, or substantial simulator/frontend construction.
5. **Budget:** 45 minutes to a headless paired trajectory and static evidence;
   no new dashboard.

## Bounded installed candidates

All three candidates ship with the installed NetLogo 7.0.4 Models Library,
open directly in the standard visual interface, run headlessly with
BehaviorSpace, and retain their original CC BY-NC-SA 3.0 attribution. The
current sorting generator is the baseline.

| Candidate | Scientific fit | First result | Boundary / reproducibility | Decision |
| --- | --- | --- | --- | --- |
| Sorting baseline | exact damage reachability now explains nearly every outcome | complete | excellent | retire for this agenda |
| Flocking | leaderless motion; alignment, separation, and cohesion produce dynamic flocks and an endogenous heading | minutes | deterministic after seeded initialization; direct trajectory reporters | **thin spike now** |
| Fireflies | local clocks and flashes synchronize without a coordinator; rich internal state | minutes | seeded stochastic motion; clean clock observations | fallback calibration |
| Slime | field-mediated movement and aggregation; endogenous cluster locations | tens of minutes | seeded randomness plus patch field; cluster metric required | later richer follow-on |

## Adoption decision

Use the standard NetLogo **Flocking** model for the first Phase 3 spike. It is
the smallest change from the retired sorting system that adds continuous
movement, changing neighborhoods, multiple flocks, and a dynamic collective
heading. Its generator code remains unmodified: an external BehaviorSpace file
sets standard parameters, applies a deterministic heading displacement, and
records observable metrics.

Reject a custom boids implementation and a Mesa port because the installed
model already supplies both generator and visualization. Keep Fireflies as the
next independent generator if flocking proves to be only passive alignment.
Keep Slime for the first field-mediated test after the measurement boundary is
settled.

Primary model references:

- <https://ccl.northwestern.edu/netlogo/models/Flocking>
- <https://ccl.northwestern.edu/netlogo/models/Fireflies>
- <https://ccl.northwestern.edu/netlogo/models/Slime>
