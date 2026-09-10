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

## 4. Regenerative competence separates desired-state information, current-state evidence, latent/developmental state, and reachable action repertoire

Experiments 06–11 progressively isolated several roles rather than treating "regeneration" as one property:

| Distinction | What the constructed systems show |
|---|---|
| **Wound vs normal boundary** | Occupancy alone can present the same local pattern at a healthy edge and an amputation edge; extra positional/boundary information is required for different actions. |
| **Amount vs position** | A tissue-produced inhibitor can restore size while leaving historical translation underdetermined. |
| **Information channels compose** | Endogenous size information plus boundary state solves repeated unilateral repair; removing either channel produces a different failure. |
| **Goal information vs action repertoire** | Perfect knowledge of missing A/B composition does not repair complete lineage extinction if surviving cells cannot generate the missing type; daughter-fate plasticity changes the reachable state space. |
| **Current-state sensing vs reporter integrity** | Endogenous composition signals are causal, but false-healthy clamps block needed repair and secretion failure can drive overgrowth. |
| **Desired-state memory vs current sensing** | Learned healthy signal levels can replace hard-coded target counts across several baseline compositions, but decaying memory creates a repair horizon and does not authenticate a failed current-state reporter. |

The accompanying identifiability argument makes the last point formal: once a self-produced reporter is known to be broken, different hidden abundances can generate the same observation history while requiring different remaining repair actions. Exact repair therefore needs some additional information about current/lost amount; more control logic cannot manufacture an unobserved distinction.

The Levin-software and broader landscape audits show that the ingredients themselves—positional information, plasticity, pattern memory, cellular competency, reachability, reporter/diagnostic limitations, regenerative local controllers—have extensive prior art. The surviving scientific use of this decomposition is as a **set of falsifiable intervention hypotheses** to test across independently authored systems, not a claim to have discovered universal natural parts of competence.

**Evidence:** [06](../experiments/06-structural-regeneration/README.md), [07](../experiments/07-endogenous-size-control/README.md), [08](../experiments/08-boundary-memory/README.md), [09](../experiments/09-composition-lineage/README.md), [10](../experiments/10-endogenous-composition/README.md), [11](../experiments/11-learned-composition-memory/README.md).

## 5. The first richer external system has a multidimensional recovery boundary, and simple scalar explanations repeatedly fail

Experiment 12 is the first phase-2 specimen whose learned local rule was not authored by this project. A pinned CPU reproduction of the published Growing NCA lizard models recovers the intended growth/persistence/regeneration hierarchy before project-specific interventions are applied.

The fixed regenerating model has a **finite tested lesion-response basin**. Radius 16 enters a low-error repaired regime, radius 18 stalls, and radius 20 later diverges over 512 updates while the matched undamaged model remains close to target. This establishes a bounded response family, not a universal lesion-size threshold.

A preregistered fixed-area geometry test shows that **lesion area alone is insufficient**. A radius-16 circle and 4:1 PC1-aligned ellipse each remove 793 grid cells and have closely matched immediate error/live-cell removal, but the ellipse falls into a high-error regime in 4/4 future streams (mean target MSE `0.01933` versus `0.00316`). This contradicts the simple prediction that more exposed intact boundary should make elongated damage easier. The orthogonal ellipse was milder immediately, so the evidence does not isolate a pure orientation/anatomy law.

A target-derived location test matched candidate lesions by immediate target error. The lowest-annulus-support location (`0.1043`) recovers worse than the highest-support centroid (`0.3052`) in 4/4 future streams (`0.00477` versus `0.00299` mean target MSE). This supports location dependence and one successful local-support prediction, not a universal support law because the matching procedure required different lesion radii/areas.

A developmental-timing test used the same radius-8 geometry at steps 48, 72, and 96 while removing about one quarter of live cells. Step 48 leaves greater residual divergence from its matched undamaged branch than step 96 in 4/4 streams (`0.000646` versus `0.000413` mean RGB MSE); step 72 is mixed (`0.000432`). Developmental state matters, but the preregistered “earlier is more correctable” rule does not hold monotonically.

The latent-state evidence is stronger than generic hidden-state importance. At radius 16, hidden-only zeroing while leaving visible RGBA intact is worse than full local deletion (`0.00875` versus `0.00316` mean target MSE). H2 then preserves visible RGBA **and the full multiset of 12-channel hidden vectors** but spatially permutes those vectors. The result is much worse than full deletion in 4/4 streams (`0.06216` mean target MSE). The warranted conclusion is that **visible/latent spatial compatibility is causally load-bearing**. This does not identify memory, a semantic goal, or an explicit target map.

A1 isolates **action availability** without overwriting state. All arms begin from the same radius-16 lesion; updates inside the original lesion footprint are withheld for 0, 16, 32, or 64 recovery steps and then restored. The strict preregistered monotonic dose prediction is mixed—16 and 32 do not consistently order—but every nonzero blackout is worse than the normal damaged branch in every tested future stream, and the 64-step blackout is clearly worst. Mean 96-step target MSE is `0.00316`, `0.00739`, `0.00735`, and `0.01401` for 0/16/32/64 steps respectively.

The action effect is not merely an observation-time delay over the tested horizon. After all actions are restored, mean RGB divergence from the normal damaged branch increases from `0.00487` to `0.00953` for the 32-step arm and from `0.01134` to `0.01396` for the 64-step arm between +96 and +256. Both restricted arms retain higher target error than normal in every seed at +256. Thus **timely corrective action is causally load-bearing and temporary restriction can produce persistent path-dependent consequences**. This is not a proof of formal unreachability.

Taken together, the frozen white-box map supports experimentally separable dependence on **challenge geometry, regional context/support, developmental state, latent-state consistency, and corrective action availability**. The scientific point is not that these ingredients are individually novel; it is that one independently authored system exposes a multidimensional competence/failure boundary that repeatedly defeats one-dimensional proxies.

**Evidence:** [Experiment 12](../experiments/12-growing-nca/README.md), which owns exact result-file links, prospective predictions/refuters, and limits.

## 6. Morphogenesis reference work already shows non-trivial information/scaling limits

The retained reaction-diffusion study reports a non-monotonic maximum reliably classifiable tissue size as morphogen decay length changes and an interior optimum in equilibration time. It is scientifically relevant to positional-information questions, but it is retrospective, based on only three usable decay-length points in the reported scaling curve, and has not been independently reproduced.

**Evidence:** [morphogenesis scaling](../experiments/morphogenesis-scaling/README.md).

## 7. Measurement and apparent history effects require aggressive interpretation checks

Several attractive metrics have proven narrower than their names. In sorting, binary recovery can remain perfect while recovery cost worsens; survivorship can make later episodes look cheaper; and an apparent watchdog history effect was a scan-cursor initial-condition effect. Repeated transient recovery also did not establish adaptation beyond a passive-attractor account.

Earlier Goal Discovery work similarly found statistics that partly tracked determinism, unused capacity, or omitted variables rather than the richer interpretation initially attached to them. The durable rule is: **inspect what a measurement is conditional on before converting it into a competence or mechanism claim.**

The external identifiability audit adds a second rule: recovering a stable trace property or likely specification is not by itself evidence of active competence. Challenge/intervention data are required to distinguish passive satisfaction from active maintenance, recovery, compensation, or adaptation.

## 8. Prior-art audits narrow the contribution from phenomenon-building to predictive and inferential discipline

The September 2026 Levin-software and broader identifiability audits show that developmental/morphogenetic systems and many conceptual/inferential primitives we might otherwise build already exist.

Therefore **"observe behavior, retain ambiguity, then intervene" is not itself a novelty claim**. The programme is only distinctive if its integrated competence framing adds validated value: predicting failure-boundary changes, producing calibrated abstention/equivalence classes, separating active correction from nominal satisfaction, or transferring an intervention decomposition across independently authored substrates where a simpler established method does not already answer the question.

This landscape conclusion now constrains all experimental interpretation and implementation. Default engineering remains **Search → reuse → wrap → intervene → compare.**

## Evidence map

For a one-line map of every native specimen, use [`experiments/README.md`](../experiments/README.md). For exact evidence, follow its links to experiment README/code/results. Novelty constraints and reusable external systems live in the [reference index](reference/README.md).

## What would count as progress now

The NCA white-box map is frozen. The immediate next progress criterion is **making that evidence inspectable without changing its semantics**, via issue #77's saved-evidence workbench and owner review.

After review, progress should come from one of two tightly controlled paths:

1. **predictive transfer** — predeclare selected NCA-derived relations and test them in another independently authored developmental system; or
2. **calibrated blind inference** — freeze a candidate criterion family and observation/intervention contract, then ask which goal/competence equivalence class is identifiable without semantic labels, compared with the nearest established baseline.

The external integration order remains reuse-first: Cellnition/RNM is the nearest reachability/path-dependence comparator if its licensing gate is explicitly passed; MinimalDevelopmentalComputation is the next high-priority independent developmental transfer specimen. A stronger result will survive such external comparison rather than accumulating more bespoke NCA sweeps.
