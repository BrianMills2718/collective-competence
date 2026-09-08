---
doc-role: working-findings-synthesis
authority: derived
lifecycle: active
sources:
  - ../experiments/01-self-sorting/README.md
  - ../experiments/02-regulation/README.md
  - ../experiments/06-structural-regeneration/README.md
  - ../experiments/03-redundant-transport/README.md
  - ../experiments/04-route-learning/README.md
  - ../experiments/05-pattern-repair/README.md
  - ../experiments/morphogenesis-scaling/README.md
  - scoreboard.md
  - ../roadmap/research.md
---
# Findings

[Wiki home](index.md) · [Questions](questions.md) · [Current work](current.md) · [Reference](reference/README.md)

This page is organized by **finding**, not by experiment. Exact protocols, data, caveats, and corrections remain with the native experiment records; those sources win if this summary drifts.

## Simple worked example: self-sorting

Sorting is the programme's simplest worked example, not its subject matter. A Levin-style sorting phenomenon was already available to reproduce, and ten locally acting agents make the mechanism and failures unusually easy to inspect.

### A global competency can arise without a represented global target

Agents see only themselves and one adjacent neighbour and can only attempt a local exchange. Sorted order exists in the experimenter's measurement, not as an internal target object held by an agent. Yet the local rules reliably produce sorted order while a locality-matched random control essentially does not.

**Scope:** one one-dimensional sorting family. It demonstrates a useful collective competency without an explicit internal representation of the global target; it does not establish a general theory.

### Reaching a criterion is not the same as continuing to steer toward it

A controller that halts after detecting sorted order and controllers that remain active look alike immediately after success. Delayed perturbation separates them: after halting, the first no longer restores the state while continuously active controllers do.

### Feedback matters more than centralization in this specimen

Under severe local action failure, decentralized, central closed-loop, and central watchdog controllers still attain sorted order reliably while an open-loop central plan degrades sharply. This is a result about the tested sorting controllers, not a theorem about decentralization.

### Robustness has structural boundaries

Unreliable or frozen members can often be routed around. An immobile blocking member partitions the line and sharply reduces recovery. One opposing-rule agent damages maintenance before two largely destroy reachability; across tested population sizes the transition tracks opposing-agent **headcount** more closely than proportion.

Why the contrarian boundary sits where it does remains mechanistically unresolved.

### Repeated recovery does not automatically imply adaptation

Repeated transient swap or teleport disturbances produce roughly stationary recovery cost for continuously acting controllers, substantially consistent with a displacement-based passive-attractor account. An apparent watchdog history effect was traced to scan-cursor state rather than adaptation.

**Evidence for this section:** [`experiments/01-self-sorting/README.md`](../experiments/01-self-sorting/README.md).

## Retained reference: morphogenesis has non-trivial scaling limits

A separate reaction-diffusion study asks how accurately cells can classify position from two opposing morphogen fields once finite sensor noise and equilibration time are made explicit. It reports two bounded findings: the largest reliably classifiable tissue size is **non-monotonic in morphogen decay length**, and the equilibration-time curve has a genuine **interior maximum** rather than improving indefinitely with more settling time.

A boundary probe in the same work found that adding mere sensing apparatus to the focal system left the classification unchanged, while including baseline access to the information source shifted the classification smoothly rather than producing a pathological jump.

**Limits:** retrospective/imported work, only three usable decay-length points in the reported scaling curve, and no independent reproduction. Treat it as a retained reference result, not benchmark-grade evidence or a registered rung of the current sequence.

**Evidence:** [`experiments/morphogenesis-scaling/README.md`](../experiments/morphogenesis-scaling/README.md).

## Passive convergence and regulation can be distinguished without the semantic answer

A passive relaxer and an authored feedback regulator can occupy the same desirable region in the unchallenged case. Matched displacements expose a large recovery difference, persistent loads expose lower late error under feedback, and blocking sensing or disabling actuation removes that advantage.

The more important follow-up withheld the authored setpoint, semantic field name, arm meanings and implementation from the existing P15 scalar proposer. Without any regulation-specific analyzer, it passed its fixed gate on all four load units and inferred candidate references **99.16, 98.81, 99.45 and 98.55** (mean **98.99**) against the hidden authored value 100. It did not promote a goal or competence claim. A separate zero-context reader given only the opaque trajectories independently identified regulation-like behavior and a reference near 100 while retaining passive damping, alternate targets/feedforward and hidden dynamics as rivals.

**Scope:** this is a bounded positive Goal Discovery result on one simple deterministic control family. It supports discovery of a useful reference/regulation interpretation from behavior and intervention; it does **not** establish a unique true goal, internal goal representation, agency, adaptation, or general goal discovery.

**Evidence:** [`experiments/02-regulation/README.md`](../experiments/02-regulation/README.md) and its blind-analysis result files.

## Compensation is recognizable as bounded route substitution

A topology-different discrete transport specimen gives two physically distinct channels the same task. With identical hardware and spare capacity, an authored rerouting policy preserves zero backlog after either single channel is disabled by shifting the full flow to the survivor; a fixed-assignment control accumulates backlog instead. When input rises to the surviving channel's capacity limit, rerouting can no longer preserve the criterion.

A zero-context reader given only anonymous trajectories, known input, and anonymous channel-disable operations independently identified the substitution pattern and the capacity boundary, while refusing to infer learning, a unique goal, or a hidden mechanism.

**Scope:** the white-box outcome is mostly entailed by the authored routing rules, so it is calibration rather than a surprising constructive discovery. The useful result is that bounded compensation/substitution is behaviorally recognizable in a structurally different system from scalar regulation.

**Evidence:** [`experiments/03-redundant-transport/README.md`](../experiments/03-redundant-transport/README.md).


## Retained experience produces behaviorally recognizable adaptation

A repeated route-allocation specimen isolates one persistent preference variable. There is no within-episode feedback: an episode uses a fixed allocation, observes the two route qualities, and only then may the next episode's allocation change. In stationary environments the adaptive arm improves delivered work from **75 → 87.5 → 95**, while frozen and reset-between controls remain at 75. After the environment reverses, retained experience is initially harmful — performance falls from 95 to **55** — and then recovers through **67.5 → 80 → 92.5 → 95** as the allocation changes.

The strongest test holds current inputs and block number fixed while changing only prior history. Under the same current `(0.5, 1.0)` environment at block 4, the adaptive system allocates 90 units to the first channel after one history and 10 after the opposite history. A zero-context reader identified this as evidence that current inputs alone do not determine behavior. Holding the changing component fixed or restoring it before each block removes the history-dependent change.

**Scope:** this supports retained history-dependent adaptation in a behavioral/causal sense. It does not identify a unique learning rule, objective, memory mechanism, or agency; a fixed stateful dynamical controller remains a possible mechanistic description.

**Evidence:** [`experiments/04-route-learning/README.md`](../experiments/04-route-learning/README.md).

## The four calibration signatures are not four exclusive mechanism labels

A one-off mixed zero-context read compared compact opaque evidence from passive attraction, feedback regulation, compensation, and adaptation together. It cleanly separated attraction, bounded substitution, and history dependence. It described the feedback specimen as a stronger regulation-like signature but correctly noted that faster restoration and smaller steady offsets alone do not uniquely distinguish active feedback from a different passive restoring law.

This is a reason to **stop polishing the calibration ladder**, not a reason to weaken the concepts. Intervention choice determines what can be inferred: the regulation experiment's sensor/actuator ablations provide causal evidence that the compressed mixed package omitted. Future work should use these distinctions on new systems rather than optimizing toy classifiers.


## Pattern repair can recover a criterion without recovering the original state

A three-colour ring provides a many-state spatial goal: adjacent cells must differ, but no exact global coloring is privileged. A conflict-aware local rule forms valid patterns rapidly from random states and repairs forced contiguous lesions using only neighbour information. The locality-matched random recoloring control becomes dramatically less effective with size: at 48 cells it reaches a valid pattern in **0/200** trials within 10,000 operations while the conflict-aware rule succeeds **200/200**.

After damage, all 200 trials repair the criterion at every tested lesion width from 1 through 12. But exact microstate restoration rapidly disappears: for width-8 and width-12 lesions, **0/200** runs return to the original pattern even though **200/200** return to some valid pattern. A single permanently frozen conflicting cell can be reorganized around in 200/200 trials; two adjacent frozen same-colour cells make the criterion structurally impossible and repair in 0/200.

A zero-context Goal Discovery pass then withheld the criterion, update rule, category meanings, global score, and whether any exact target existed. The reader independently proposed the cyclic neighbor-inequality relation as the strongest compact candidate criterion, distinguished formation from post-damage restoration, concluded that the diverse repaired endpoints support an equivalence class rather than exact reconstruction, and derived the adjacent-frozen-pair feasibility boundary.

**Scope:** this is a hand-authored self-stabilizing one-dimensional coloring rule, not biological regeneration. The blind result supports relational/many-state candidate-goal inference on this specimen; it does not establish a unique goal, agency, internal target representation, or that every state satisfying the proposed relation is acceptable.

**Evidence:** [`experiments/05-pattern-repair/README.md`](../experiments/05-pattern-repair/README.md).

## Structural regrowth needs information that distinguishes wound from boundary

A one-dimensional tissue with actual vacancies and local proliferation exposes a simple information problem. With occupancy alone, an intact tissue edge and the surviving edge after end amputation present the same radius-1 pattern `(1, 1, 0)`. A translation-invariant radius-1 rule therefore cannot both stop at the normal boundary and grow at the wound boundary without some additional cue.

In the constructive specimen, two external organizer gradients provide a relative positional coordinate. A ratio-based birth gate forms and regenerates the same 24-site tissue under common source amplitudes 0.75, 1.0 and 1.25, and repairs all 27 declared combinations of left/right/middle amputation, width 4/8/12 and common amplitude. An absolute single-gradient gate calibrated to the identical baseline succeeds exactly only in the nine amplitude-1 cases; ungated local proliferation never stops at the target boundary.

The relative code has a clear limit: unequal changes in the two organizer sources shift the recovered morphology, and loss of either source blocks the declared repair. **Scope:** this is an authored positional-information mechanism with external organizers, not autonomous morphogenesis. The useful result is the wound-versus-boundary information requirement and one concrete way of resolving it.

**Evidence:** [`experiments/06-structural-regeneration/README.md`](../experiments/06-structural-regeneration/README.md).

## Measurement choices can hide important differences

Across the work, several attractive headline measures have turned out to read less than their names suggest. In sorting, recovery rate can stay at 1.0 while recovery cost deteriorates; a halted controller can receive a nominal recovery score despite no longer participating; and survivorship can make later episodes appear cheaper. Earlier Goal Discovery work similarly found measures that tracked determinism, unused capacity, or omitted mechanism variables rather than the richer interpretation initially attached to them.

The useful lesson is practical: inspect what a metric is actually conditional on before turning it into a scientific interpretation.

## Other Goal Discovery results remain deliberately narrow

The repository contains results on shared scarcity signals, symmetry breaking, effective information, proposal grammars, and related instrument qualification. Several were narrowed by stronger controls or by showing that an interesting-looking result was partly derivable from specimen construction. They remain useful evidence and negative knowledge, but none currently serves as a general account of competence.

See [the generated scoreboard](scoreboard.md), [research synthesis](../roadmap/research.md), and [reference material](reference/README.md) for the full record.

## What would count as progress from here

Progress now means using these distinctions on **genuinely new phenomena**, not adding more calibration categories. Structural repair and regrowth have now exposed two different questions: recovering a many-state relation and knowing where/when to replace missing components. The current work page owns the next concrete action.
