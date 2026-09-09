---
doc-role: working-findings-synthesis
authority: derived
lifecycle: active
sources:
  - ../experiments/README.md
  - reference/research-landscape.md
  - reference/levin-software-ecosystem-survey.md
  - reference/goal-competence-identifiability-landscape.md
  - ../roadmap/research.md
---
# Findings

[Wiki home](index.md) · [Questions](questions.md) · [Current work](current.md) · [Experiments](../experiments/README.md) · [Reference](reference/README.md)

This page records **cross-cutting findings**, not one section per run. Native experiment READMEs, code, and result packages remain authoritative for exact protocols, numbers, and caveats. The first-phase systems are calibration surfaces; the neighboring phenomena they instantiate are generally not novelty claims.

## 1. Useful collective competence can arise without an explicit global target representation

The founding self-sorting system uses only local adjacent comparisons/exchanges while sorted order exists in the experimenter's measurement, not as a global object inside the agents. The locality-matched random control essentially does not sort, so locality alone is not the explanation.

Sorting also established two durable distinctions. First, **reaching a criterion is not the same as continuing to steer toward it**: a closed-loop controller that halts after success can look identical at the target yet fail a delayed perturbation that continuously active controllers repair. Second, the strongest tested robustness divider is feedback versus open loop, not centralized versus decentralized control.

Robustness is nevertheless structural rather than unlimited: unreliable/frozen members can often be routed around, while an immobile blocker partitions the line; small numbers of opposing-rule agents can destroy maintenance before they destroy one-time attainment.

**Evidence:** [Experiment 01](../experiments/01-self-sorting/README.md). **Novelty qualification:** distributed sorting as basal competence and self-stabilizing local-to-global order have direct prior art; this specimen's current value is calibration of maintenance, perturbation, and inference distinctions.

## 2. A supported goal criterion can be a relation or equivalence class, not one target microstate

The three-colour ring forms and repairs configurations satisfying the relation "adjacent colours differ." After large forced lesions, all tested runs recover the criterion while none recover the original microstate. A blind reader, given trajectories/interventions but not the authored criterion, independently proposes the same relational family and recognizes the permanent adjacent-frozen-pair impossibility boundary.

This lesson corrected a later interpretation error in homogeneous tissue repair: returning to a different translated interval is not an anatomical failure unless external position is actually part of the criterion. **Do not silently privilege one representative of an equivalence class.**

Equivalence classes themselves are not novel: they are standard in inverse problems, causal identification, IRL/reward ambiguity, formal methods, and behavioral systems. The project-specific burden is to show that preserving the right equivalence class materially improves competence interpretation or prediction on external systems.

**Evidence:** [Experiment 05](../experiments/05-pattern-repair/README.md) and the correction in [Experiment 08](../experiments/08-boundary-memory/README.md).

## 3. Regulation, compensation, and adaptation are operationally distinct, but behavioral signatures do not uniquely name mechanisms

A passive relaxer and feedback regulator separate under matched displacement, persistent load, and sensor/actuator ablation. With the semantic setpoint hidden, the existing scalar proposal machinery infers a reference near the authored value 100 without promoting a goal/competence claim.

A topology-different transport system shows **bounded compensation**: rerouting substitutes for either failed route while surviving capacity is sufficient, and fails when it is not. A repeated route-allocation system shows **retained history-dependent adaptation**: under the same current environment, later allocation differs because of prior experience; frozen/reset controls remove the history effect.

A mixed blind comparison correctly separates attraction, substitution, and history dependence but also shows the limit: stronger restoration alone does not prove a feedback mechanism. Intervention design determines what mechanism claims are identifiable.

These distinctions are useful operationally, but regulation, observability, reachability, fault diagnosis, adaptation, and active model discrimination are established neighboring fields. Their use here must be connected to standard terminology and baselines where the assumptions fit.

**Evidence:** [02 regulation](../experiments/02-regulation/README.md), [03 compensation](../experiments/03-redundant-transport/README.md), [04 adaptation](../experiments/04-route-learning/README.md).

## 4. Regenerative competence separates desired-state information, current-state evidence, memory, and reachable action repertoire

Experiments 06–11 progressively isolate these roles rather than treating "regeneration" as one property:

| Distinction | What the constructed systems show |
|---|---|
| **Wound vs normal boundary** | Occupancy alone can present the same local pattern at a healthy edge and an amputation edge; extra positional/boundary information is required for different actions. |
| **Amount vs position** | A tissue-produced inhibitor can restore size while leaving historical translation underdetermined. |
| **Information channels compose** | Endogenous size information plus boundary state solves repeated unilateral repair; removing either channel produces a different failure. |
| **Goal information vs action repertoire** | Perfect knowledge of missing A/B composition does not repair complete lineage extinction if surviving cells cannot generate the missing type; daughter-fate plasticity changes the reachable state space. |
| **Current-state sensing vs reporter integrity** | Endogenous composition signals are causal, but false-healthy clamps block needed repair and secretion failure can drive overgrowth. |
| **Desired-state memory vs current sensing** | Learned healthy signal levels can replace hard-coded target counts across several baseline compositions, but decaying memory creates a repair horizon and does not authenticate a failed current-state reporter. |

The accompanying identifiability argument makes the last point formal: once a self-produced reporter is known to be broken, different hidden abundances can generate the same observation history while requiring different remaining repair actions. Exact repair therefore needs some additional information about current amount/lost amount; more control logic cannot manufacture an unobserved distinction.

The Levin-software and broader landscape audits show that the ingredients themselves — positional information, plasticity, pattern memory, cellular competency, reachability, reporter/diagnostic limitations, regenerative local controllers — have extensive prior art. The surviving scientific use of this decomposition is as a **set of falsifiable intervention hypotheses** to be tested across independently authored systems, not as a claim to have discovered the natural universal parts of competence.

**Evidence:** [06](../experiments/06-structural-regeneration/README.md), [07](../experiments/07-endogenous-size-control/README.md), [08](../experiments/08-boundary-memory/README.md), [09](../experiments/09-composition-lineage/README.md), [10](../experiments/10-endogenous-composition/README.md), [11](../experiments/11-learned-composition-memory/README.md).

## 5. Selected capability distinctions survive the first richer external test—and expose non-obvious geometry and hidden-state behavior

Experiment 12 is the first phase-2 specimen whose learned local rule was not authored by this project. A pinned CPU reproduction of the published Growing NCA lizard models recovers the intended hierarchy: a growth-trained model forms but does not maintain/repair the severe lesion, a persistence-trained model maintains an intact form but does not repair it, and the regeneration-trained model repairs it.

The fixed regenerating model has a **finite lesion-response basin** on the tested central-circle family. Radius 16 enters a low-error repaired regime, radius 18 stalls at much higher error, and radius 20 eventually diverges over a 512-update horizon while the matched undamaged model remains close to target.

A preregistered fixed-area geometry test shows that **lesion area alone is not sufficient**. A radius-16 circle and a 4:1 PC1-aligned ellipse each remove 793 grid cells and have closely matched immediate target error/live-cell removal, but the ellipse falls into a high-error regime across 4/4 confirmation streams (mean 96-step target MSE `0.01933` versus `0.00316` for the circle). This contradicts the simple prediction that more exposed intact boundary per removed cell should make elongated damage easier to repair. The orthogonal PC2 ellipse recovers better but is substantially less severe at the moment of damage, so the current evidence does **not** isolate a pure orientation/anatomy effect. The warranted result is that geometry/orientation can shift the recovery boundary beyond what lesion pixel count predicts.

The hidden-state result is stronger than simple latent-state importance. At radius 16, erasing only the 12 hidden channels while leaving visible RGBA intact is **more damaging than deleting the full local 16-channel state**. The ordering holds across 4/4 independently seeded future update streams (mean 96-step target MSE `0.00875` hidden-only versus `0.00316` full deletion). At radius 8, hidden-only corruption is largely absorbed.

H2 then preserves the hidden content but breaks its spatial assignment: complete 12-channel hidden vectors are shuffled inside the radius-16 mask while visible RGBA and the hidden-vector multiset remain unchanged. This is worse than full deletion in 4/4 streams, with mean 96-step target MSE `0.06216` (`0.00875` hidden-zero, `0.00316` full deletion, `0.000679` undamaged). The conservative conclusion is now that **visible/latent spatial compatibility is causally load-bearing**, not merely that hidden channels matter. The shuffle includes both visibly occupied and empty cells, so it does not yet isolate fine-grained live-cell latent identity. It also does not establish a semantic goal, memory map, or explicit target representation. Nor does one NCA result establish a substrate-independent decomposition; transfer requires successful prospective predictions on additional external systems.

**Evidence:** [Experiment 12](../experiments/12-growing-nca/README.md), which owns the lesion-basin and hidden-state result-file links.

## 6. Morphogenesis reference work already shows non-trivial information/scaling limits

The retained reaction-diffusion study reports a non-monotonic maximum reliably classifiable tissue size as morphogen decay length changes and an interior optimum in equilibration time. It is scientifically relevant to the current positional-information questions, but it is retrospective, based on only three usable decay-length points in the reported scaling curve, and has not been independently reproduced.

**Evidence:** [morphogenesis scaling](../experiments/morphogenesis-scaling/README.md).

## 7. Measurement and apparent history effects require aggressive interpretation checks

Several attractive metrics have proven narrower than their names. In sorting, binary recovery can remain perfect while recovery cost worsens; survivorship can make later episodes look cheaper; and an apparent watchdog history effect was a scan-cursor initial-condition effect. Repeated transient recovery also did not establish adaptation beyond a passive-attractor account.

Earlier Goal Discovery work similarly found statistics that partly tracked determinism, unused capacity, or omitted variables rather than the richer interpretation initially attached to them. The durable rule is simple: **inspect what a measurement is conditional on before converting it into a competence or mechanism claim.**

The external identifiability audit adds a second rule: recovering a stable trace property or likely specification is not by itself evidence of active competence. A passive attractor, invariant, one-shot controller, and active regulator can satisfy the same nominal criterion on ordinary trajectories; challenge/intervention data are needed to distinguish them.

## 8. The prior-art audits narrow the contribution from phenomenon-building to predictive and inferential discipline

Two September 2026 audits changed the strategic interpretation of the programme:

- the [Levin software ecosystem survey](reference/levin-software-ecosystem-survey.md) shows that many of the developmental/morphogenetic systems and conceptual primitives we might otherwise build already exist as executable prior work;
- the [goal/competence identifiability survey](reference/goal-competence-identifiability-landscape.md) shows that underdetermination, behavioral equivalence, active discrimination, goal recognition, reward ambiguity, specification mining, and black-box model inference are also established ideas in adjacent fields.

Therefore, **"observe behavior, retain ambiguity, then intervene" is not itself a novelty claim.** The programme is only distinctive if the competence framing adds validated value: for example, predicting failure-boundary changes, separating specification satisfaction from active correction, producing calibrated abstention on an external system, or transferring an intervention decomposition across substrates where a simpler established baseline does not already answer the question.

This is a research-landscape conclusion rather than a native experimental result, but it now constrains how all experimental findings should be interpreted and presented.

## Evidence map

For a one-line map of every native specimen, use [`experiments/README.md`](../experiments/README.md). For exact evidence, follow its links to the experiment README/code/results. Novelty constraints and reusable external systems live in the [reference index](reference/README.md). Older instrument-qualification work, audits, conjectures, and corrections remain searchable there and through the generated [scoreboard](scoreboard.md).

## What would count as progress now

The next progress criterion is **prospective prediction plus calibrated inference in external systems**, not another isolated demonstration of a primitive already understood.

On the fixed external NCA:

1. state predictions before testing whether recovery boundaries depend on lesion amount, geometry, region, developmental timing, latent-state consistency, or available update actions;
2. use matched causal comparisons and preserve negative/falsifying outcomes;
3. after the white-box map is understood, define rival candidate criteria and competence dimensions before withholding semantics;
4. compare against a nearest-method baseline where its assumptions fit, including a passive-convergence/specification-satisfaction alternative;
5. promote Goal Discovery only if it recovers the supported resolution, preserves surviving equivalence classes, and adds something that the baseline does not.

A stronger later result would reproduce this pattern on another independently authored system selected for a different mechanism or substrate, rather than tuning the framework to the NCA alone.
