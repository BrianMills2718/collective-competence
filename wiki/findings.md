---
doc-role: working-findings-synthesis
authority: derived
lifecycle: active
sources:
  - ../experiments/01-self-sorting/README.md
  - ../experiments/02-regulation/README.md
  - scoreboard.md
  - ../roadmap/research.md
---
# Findings

[Wiki home](index.md) · [Questions](questions.md) · [Current work](current.md) · [Reference](reference/README.md)

This page is organized by **finding**, not by experiment. It is the shortest route to what the programme currently thinks it has learned. Exact protocols, data, caveats, and corrections remain with the native experiment records; those sources win if this summary ever drifts.

## Sorting can arise without a represented global target

In the founding self-sorting system, agents see only themselves and one adjacent neighbour and can only attempt a local exchange. The global criterion — sorted order — exists in the experimenter's measurement, not as an internal target object held by any agent. Yet decentralized local rules reliably produce the sorted global state while a locality-matched random control essentially does not.

**Scope:** one one-dimensional sorting family. This shows a useful collective competency without an explicit internal representation of the global target; it does not establish a general theory of collective competence.

**Evidence:** [`experiments/01-self-sorting/README.md`](../experiments/01-self-sorting/README.md).

## Reaching a criterion is not the same as continuing to steer toward it

A controller that halts after detecting a sorted state and controllers that continue acting can look equally successful immediately after reaching the goal. Delayed perturbation separates them: once the halting controller has stopped, it no longer restores the state, while continuously active controllers do.

The important distinction is therefore not just **being at** a desirable state, but whether the system still has an active organization that **steers toward or maintains** it.

**Evidence:** self-sorting delayed-perturbation results.

## Feedback matters more than centralization in the sorting specimen

Under severe local action failure, decentralized, central closed-loop, and central watchdog controllers still reach sorted order reliably. The open-loop central plan degrades sharply. In this specimen, the important contrast is therefore feedback versus open-loop execution rather than central versus decentralized organization.

**Scope:** this is a property of the tested sorting controllers, not a general theorem about decentralization.

## Robustness has structural boundaries

An unreliable or frozen member can often be routed around with little effect on eventual success. A dead immobile member partitions the line and sharply reduces recovery for all controllers. The failure mode therefore depends on what capability is lost, not simply on whether a component is defective.

This is useful because the negative case constrains mechanistic explanations of the competency.

## Contrarian disruption scales with headcount more strongly than proportion

Across several population sizes, one opposing-rule agent is often survivable while two largely destroy reachability. The transition tracks the number of opposing agents much more closely than their fraction of the population.

A single opposing agent also affects **maintenance** before it destroys **attainment**: the system may still occasionally reach sorted order while no longer holding it as a stable condition.

**Open question:** why the boundary sits where it does has not yet been established mechanistically.

## Repeated transient recovery does not, by itself, show something richer than passive attraction

When transient swap or teleport disturbances are repeated, recovery cost remains roughly stationary for continuously acting sorting controllers. A simple displacement-based passive-attractor account explains much of the behavior. The experiment therefore weakens any attempt to infer richer adaptation merely from repeated recovery.

An apparent history effect in the watchdog controller was traced to its scan cursor's initial correlation with the just-sorted array rather than adaptation.

This is a useful negative finding: the programme should not treat robustness or repeated recovery as automatic evidence of adaptation or agency.

## Passive convergence and negative-feedback regulation now coexist on the shared lattice

The first non-sorting control pair has been ported onto the shared lattice. Both a passive relaxer and an authored feedback regulator can occupy the same desirable region in the unchallenged case. Under matched state displacements, feedback returns to the criterion in 2 steps while passive relaxation takes 8–11. Under persistent loads, feedback roughly halves or better the late error across the tested range. Blocking sensing or disabling actuation removes that advantage exactly.

**Scope:** this is a deterministic calibration/port of an already-known thermostat contrast, not a new discovery of agency, adaptation, or collective competence. Its value is that a second qualitative phenomenon now lives on the same substrate as sorting, with a clean passive rival and causal ablations.

**Evidence:** [`experiments/02-regulation/README.md`](../experiments/02-regulation/README.md) and its committed characterization result.

## Measurement choices can hide important differences

Several sorting follow-ups exposed cases where a headline measure was insufficient. Recovery rate can remain at 1.0 while recovery cost deteriorates; a controller that has halted can produce a nominal recovery score even though it is no longer participating in the test; survivorship can make later episodes look cheaper.

The general lesson is practical rather than bureaucratic: inspect what a metric is actually conditional on before turning it into a scientific interpretation.

## Findings that remain narrow

The repository also contains results on shared scarcity signals, symmetry breaking, effective information, and other Goal Discovery calibration work. Several were later narrowed by stronger controls or by showing that the interesting-looking result was partly derivable from the specimen's construction. They remain useful evidence, but they should not currently outrank the sorting line as the programme's conceptual front door.

See [the generated scoreboard](scoreboard.md), [research synthesis](../roadmap/research.md), and [reference material](reference/README.md) for the full record.

## What would count as progress from here

The programme still needs more **different phenomena**, not merely more measurements of sorting. Regulation is now present as the second qualitative control family. The next useful test is whether Goal Discovery can distinguish it from passive convergence without privileged implementation knowledge; after that, move to compensation/repair and eventually adaptation.
