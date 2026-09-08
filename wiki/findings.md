---
doc-role: working-findings-synthesis
authority: derived
lifecycle: active
sources:
  - ../experiments/01-self-sorting/README.md
  - ../experiments/02-regulation/README.md
  - ../experiments/06-structural-regeneration/README.md
  - ../experiments/07-endogenous-size-control/README.md
  - ../experiments/08-boundary-memory/README.md
  - ../experiments/09-composition-lineage/README.md
  - ../experiments/10-endogenous-composition/README.md
  - ../experiments/11-learned-composition-memory/README.md
  - ../experiments/12-growing-nca/README.md
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

## A tissue-produced signal can restore size without restoring historical position

A contiguous tissue can encode its own size in the inhibitor concentration sensed locally at either edge. With thresholds calibrated around size 24, loss lowers the self-produced signal and opens proliferation; excess raises it and triggers edge removal. Across right-side loss and addition challenges of 1, 2, 4, 8, 12 and 18 cells, **all 24,000 declared trials return to size 24**.

That does not imply return to the same arena interval. Because either edge can act, exact return to the pre-damage interval after an 8-cell one-sided challenge occurs in only **12/2000** trials; at widths 12 and 18 it occurs in **0/2000**, despite perfect size recovery. Clamping the pre-damage signal prevents regrowth after loss, while removing inhibitor secretion removes the stopping condition and produces continued growth.

The self-generated size cue also has a signal-range boundary. With additive sensing noise sigma 0.02 and thresholds re-tuned to the same target size, the fraction of scored steps at size 24 rises from **0.190** at decay length 4 to **0.834** at 8, **0.999** at 12 and **1.000** at 18 as adjacent tissue sizes become more distinguishable at the edge.

**Scope:** this is an engineered steady-state exponential signaling model with an authored target threshold, not a biological mechanism. Its useful result is a decomposition: endogenous collective information can support size homeostasis while leaving historical translation underdetermined.

**Evidence:** [`experiments/07-endogenous-size-control/README.md`](../experiments/07-endogenous-size-control/README.md).

## Size and boundary-state information compose; bilateral runs expose a criterion ambiguity

Adding one local sealed/unsealed state to each tissue edge composes cleanly with the endogenous size signal. After unilateral amputations on either side at widths 1, 4, 8, 12 and 18, the combined controller restores the exact pre-damage interval in **20,000/20,000** declared trials and reseals the repaired edge, supporting repeated opposite-side damage.

The two information channels are experimentally separable. Removing boundary memory while retaining size sensing restores size after an 8-cell cut in **2000/2000** trials but the exact pre-damage interval in only **5/2000**. Holding the size signal at its quiet pre-damage value while retaining wound memory yields no regrowth and leaves size 16. Removing inhibitor secretion while retaining wound memory constrains growth to the wounded side but loses the stop, reaching size **66** after 50 operations.

Under simultaneous bilateral damage, both edges are wounded and total size deficit is known. The authored controller randomly assigns births across the two edges. Size returns in every declared bilateral trial, while return to the historical interval occurs only at the binomial frequency of assigning the same number of births to each side as were removed.

A subsequent interpretation called this a multi-wound anatomical allocation failure. **That interpretation was too strong.** In Experiment 08 the tissue has no internal compartments or pattern: it is simply a homogeneous contiguous interval. Every size-24 outcome is therefore a translation of every other size-24 outcome. Under a translation-invariant morphology criterion, bilateral repair succeeds whenever size returns. The unrecovered property is historical arena position, which matters only if an external landmark or remembered frame is explicitly part of the goal.

**Scope:** the boundary bit remains an authored toy state, and neither the positive composition result nor the correction proves minimality. The important methodological result is that an apparent information deficit can be created by silently privileging one representative of an equivalence class. Future multi-wound work should first introduce non-translation-equivalent morphology or an explicit environmental anchor before adding an allocation mechanism.

**Evidence:** [`experiments/08-boundary-memory/README.md`](../experiments/08-boundary-memory/README.md).

## Goal information is not sufficient when the missing state is outside the action repertoire

A two-compartment tissue makes regeneration intrinsically non-translation-equivalent: the criterion is `A^8 B^16` modulo translation. Wrong left/right repair now changes composition rather than merely moving a homogeneous interval.

Experiment 09 deliberately supplies **perfect A/B target counts as an oracle control** to remove uncertainty about what is missing. When both lineages survive, lineage-preserving local proliferation restores all **6/6** declared partial-loss cases. When one compartment is completely removed, the same controller repairs **0/4** declared lineage-extinction cases despite knowing exactly which type is absent. It can only make daughters of surviving types. Adding daughter-fate plasticity repairs **4/4** extinction cases.

If every cell is removed, even the plastic oracle controller cannot regenerate: parent-dependent local growth has no surviving source. The result therefore separates three challenge regimes—information sufficient while the needed lineage survives; additional fate plasticity required after lineage extinction; and complete tissue extinction outside the declared parent-dependent repertoire.

**Scope:** the composition oracle and plasticity rule are authored positive controls, not proposed biological mechanisms, and the random-allocation probabilities for partial bilateral damage are combinatorial consequences of the policy. The useful result is conceptual and causal: knowing a supported goal criterion does not imply having an action capable of reaching it.

**Evidence:** [`experiments/09-composition-lineage/README.md`](../experiments/09-composition-lineage/README.md).

## Tissue-generated composition information is causal but depends on reporter integrity

Experiment 10 replaces the A/B count oracle with type-specific endogenous inhibitors using the same steady-state field contract as the earlier size controller. With both lineages represented, those signals restore the translation-invariant target `A^8 B^16` in **6/6** declared partial-loss challenges. Complete lineage loss still defeats lineage-conserving repair (**0/4**), while daughter-fate plasticity restores **4/4**.

The signal controls show that the information channel is causal rather than decorative. Clamping the A signal at its healthy target value after removing half the A compartment produces **0** births and leaves A=4, B=16. Eliminating A secretion removes the stop: after the same partial loss, A grows to **44** in the fixed 40-operation window. After complete A extinction, the plastic arm normally restores A=8, but with A secretion disabled it instead reaches **A=40, B=16** in 40 operations.

This exposes a new limitation of self-produced measurements: a low signal can mean genuine structural loss, but a broken source can generate the same “deficit” direction and drive pathological compensation. Information about composition therefore has a reliability problem in addition to a capacity problem.

**Scope:** the two inhibitor identities, target thresholds, polarity, plasticity, and instantaneous field equilibration are authored. The result does not show that real tissues use such reporters or that secretion loss is observationally identical to lineage loss under every other cue. It shows that tissue-generated goal information remains contingent on the mechanism that reports it.

**Evidence:** [`experiments/10-endogenous-composition/README.md`](../experiments/10-endogenous-composition/README.md).

## Healthy history can supply a regenerative setpoint, but memory and sensing fail differently

Experiment 11 removes the hard-coded A/B target counts from the repair controller. Before damage, an extracellular trace learns the healthy endogenous A and B signal levels by exponential averaging. The same repair rule is then tested on healthy compositions `A^6 B^18`, `A^8 B^16`, and `A^10 B^14`.

With persistent learned memory and fate plasticity, all **12/12** declared partial and lineage-extinction challenges return to their own learned healthy composition. The memory itself starts at zero and converges to each healthy signal without receiving the target counts. Faster memory decay creates a bounded repair horizon: exact success across those 12 challenges is **12, 12, 11, 8, 4** for per-birth retention `1.0, 0.9995, 0.999, 0.998, 0.995` respectively. Without fate plasticity, complete A/B extinction remains unrepaired in **0/6** declared cases.

The wound state disambiguates one reporter fault but not all of them. If A secretion fails in an otherwise intact `A^8 B^16` tissue, no wound is present and the controller performs **0** births. If A secretion fails simultaneously with an A wound, however, the current A signal never approaches the remembered healthy setpoint: the fixed 40-birth window ends at **A=44, B=16** after partial A loss and **A=40, B=16** after complete A extinction.

**Scope:** the memory update, persistence law, 99% matching tolerance, wound bits, signal identities, and fate plasticity are authored. The retention sweep is a deterministic memory-capacity illustration, not a biological lifetime estimate. The useful distinction is that desired-state memory can survive structural loss while current-state measurement remains a separate, fallible information problem.

**Evidence:** [`experiments/11-learned-composition-memory/README.md`](../experiments/11-learned-composition-memory/README.md).


## External NCA shows a finite regeneration basin and load-bearing latent state

The published Growing Neural Cellular Automata lizard models provide the first phase-2 specimen whose learned local rule was not authored by this project. A pinned NumPy reproduction recovers the published qualitative hierarchy: growth, persistence of an intact morphology, and regeneration after a severe lesion are distinct capabilities.

On the fixed regeneration-trained model, a matched central-lesion sweep exposes a bounded recovery regime. After 96 recovery updates, radius-8 and radius-16 lesions return to target MSE **0.000482** and **0.003410**, while radius-18 and radius-20 lesions remain at **0.014094** and **0.016404**. Longer observation does not turn the latter into simple slow recovery: radius 18 stalls near 0.015 and radius 20 later diverges to **0.03543** by +512 updates, while the undamaged branch remains near the target.

Selective channel interventions show that latent state is causally load-bearing. At radius 16, erasing only the 12 hidden channels while leaving visible RGBA present is more damaging than deleting the entire local state. Across four independently seeded future update streams from the same formed state, hidden-only corruption is worse than full deletion in **4/4** comparisons (mean target MSE **0.00875** versus **0.00316**). A smaller radius-8 hidden-state corruption is largely absorbed.

**Scope:** this supports a role for hidden-state magnitude/consistency in one externally specified learned NCA. It does not establish that hidden channels encode a literal goal, target map, or semantic memory. The current basin is also limited to one target and central circular lesions; geometry, location, developmental timing, and action restrictions remain to be tested.

**Evidence:** [`experiments/12-growing-nca/README.md`](../experiments/12-growing-nca/README.md), [`lesion_basin.json`](../experiments/12-growing-nca/results/lesion_basin.json), and [`hidden_state_probe.json`](../experiments/12-growing-nca/results/hidden_state_probe.json).

## Measurement choices can hide important differences

Across the work, several attractive headline measures have turned out to read less than their names suggest. In sorting, recovery rate can stay at 1.0 while recovery cost deteriorates; a halted controller can receive a nominal recovery score despite no longer participating; and survivorship can make later episodes appear cheaper. Earlier Goal Discovery work similarly found measures that tracked determinism, unused capacity, or omitted mechanism variables rather than the richer interpretation initially attached to them.

The useful lesson is practical: inspect what a metric is actually conditional on before turning it into a scientific interpretation.

## Other Goal Discovery results remain deliberately narrow

The repository contains results on shared scarcity signals, symmetry breaking, effective information, proposal grammars, and related instrument qualification. Several were narrowed by stronger controls or by showing that an interesting-looking result was partly derivable from specimen construction. They remain useful evidence and negative knowledge, but none currently serves as a general account of competence.

See [the generated scoreboard](scoreboard.md), [research synthesis](../roadmap/research.md), and [reference material](reference/README.md) for the full record.

## What would count as progress from here

Progress now means separating **remembered desired state from trustworthy observation of current state**. Before adding a redundant reporter, state which hidden structural/reporter states are observationally distinguishable under the available wound and intervention channels. The current work page owns the next concrete action.
