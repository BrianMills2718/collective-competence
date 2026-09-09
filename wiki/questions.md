---
doc-role: working-research-questions
authority: working-summary
lifecycle: active
sources:
  - ontology.md
  - goals.md
  - reference/research-landscape.md
  - reference/levin-software-ecosystem-survey.md
  - ../goal-discovery/docs/PROJECT.md
  - current.md
---
# Research questions

[Wiki home](index.md) · [Findings](findings.md) · [Current work](current.md) · [Concepts](concepts.md)

## Central question

**How do simple component capabilities and interactions produce robust, goal-relative competencies of a whole, and what can we infer about those competencies and candidate goals from the system's behavior?**

The programme approaches that question from two directions. **Collective Competence** constructs systems and varies their mechanisms. **Goal and Competence Discovery** observes and intervenes on systems and asks what goal criteria and competence claims the behavior supports, contradicts, or leaves underdetermined. The same Dynamical Laboratory supports both.

Neither arm requires a unique scalar notion of "more competent," and Goal Discovery does not require one uniquely identifiable true goal. A result may support several candidate criteria or remain underdetermined. The scientific burden is to state what the evidence actually discriminates.

### Novelty guardrail

The September 2026 [research landscape](reference/research-landscape.md) and [Levin-lab software ecosystem survey](reference/levin-software-ecosystem-survey.md) show that many broad constructive formulations are already well occupied: local-to-global morphogenetic competence, component-competency effects, scaling of homeostatic goals, bioelectric coordination, distributed pattern information/memory, reachability/path-dependence maps, and mechanism inference from perturbation/phenotype data all have substantial prior art and in several cases executable software.

Accordingly, **the programme does not claim novelty for the existence of those phenomena or for renaming established control/regeneration concepts**. The stronger current burden is narrower: make intervention-grounded predictions that transfer to independently authored systems, and state exactly which goal/competence claims are identifiable or underdetermined under a declared observation/intervention contract.

A useful sharper operational formulation is:

> **What experimentally separable constraints determine the goal-relative competencies and failure boundaries of dynamical systems, and under a declared observation/intervention contract which of those competencies and candidate goals are behaviorally identifiable?**

The original central question remains the umbrella; this sharper version is the current test standard.

## Constructive questions

1. **What mechanisms and component capabilities produce a system-level competency?** Begin where mechanisms are inspectable, then test whether the same decomposition survives in richer systems.
2. **Which capabilities and couplings are load-bearing?** Remove, weaken, replace, or vary them and identify what challenge each one actually solves.
3. **What makes successful behavior persist under changed conditions?** Distinguish reaching, maintaining, restoring, compensating, adapting, and learning.
4. **Where are the boundaries of the competency?** Noise, damage, hidden-state corruption, changed initial conditions, resource limits, altered topology, and sensor/actuator faults constrain explanations.
5. **How do simple capabilities compose?** Desired-state information, current-state observation, memory, action repertoire, plasticity, communication, and fault diagnosis should be treated as separable until experiments show how they interact.
6. **Which effects survive increasing complexity?** A relationship demonstrated in a hand-authored toy remains local until it predicts behavior in a richer or externally specified system.

For phase 2+, a constructive result is strongest when it makes a **risky prediction before the intervention**: intervention X should shift a recovery/failure boundary relative to Y for a stated causal reason, and an alternative outcome would count against that explanation.

## Discovery questions

1. **Which candidate goal criteria are supported by behavior without supplying the semantic answer to the analyst?** A candidate should earn support through behavior beyond the observations used to propose it.
2. **What distinguishes active goal-directed performance from passive convergence or an attractor?** Interventions are especially useful when ordinary trajectories look alike.
3. **Which aspects of competence can actually be demonstrated?** Attainment, maintenance, reliability, efficiency, robustness, recovery, adaptation, flexibility, and transfer are separate measurements; experiments need only claim what they test.
4. **When is the evidence underdetermined?** Several goal descriptions may remain behaviorally equivalent under the available observation and intervention contract. That is a legitimate result, not a failure to force a label.
5. **What additional observation or intervention would discriminate rival explanations?** This includes ordinary mechanism ambiguity and fault-diagnosis/observability limits.
6. **Can useful goal/competence structure be inferred in systems we did not author for the purpose of being inferred?** This is a stronger test than another bespoke calibration case.

A discovery result is not strongest when it merely guesses the author's target label. It is strongest when the analyst is **calibrated**: it recovers a criterion at the resolution actually supported by the evidence, preserves equivalence classes where rivals survive, abstains from stronger semantic claims, and identifies the intervention that would separate those rivals.

## Current concrete programme

The first phase established a set of small calibration and primitive specimens: self-sorting, passive versus feedback regulation, bounded compensation, retained history-dependent adaptation, many-state pattern repair, structural regrowth, endogenous size/composition signals, generative plasticity, learned setpoint memory, and explicit observation/fault-identifiability limits. These are **building blocks and calibration surfaces**, not a general theory and not novelty claims for the underlying phenomena.

The original project strategy was a Robinson-Crusoe-style construction: keep the experimental discipline reusable while moving from simple systems to progressively richer compositions. The current priority is therefore **compositional scaling and external interrogation**, not another sequence of isolated one-purpose toys and not another substrate rewrite.

The intended complexity path is:

1. **Primitive calibrations — substantially complete.** Small systems establish clean distinctions and controls.
2. **Compositional mesoscopic system — current phase.** Use a richer externally specified local system containing many interacting sites, hidden state, development, persistence, and regeneration. The first target is the published **Growing Neural Cellular Automata** system.
3. **Close external comparators and developmental systems.** Prefer existing systems selected for a concrete prediction: e.g. Cellnition/RNM for reachability/control comparison, MinimalDevelopmentalComputation for regenerative local-controller transfer, LENIA Umwelt for blinded sensory/goal inference, or BioElectricNetwork/NeuralPlatePatterning/BETSE when a bioelectric hypothesis is required.
4. **Mechanistic biological models and real corpora.** Wrap established models/platforms or SBML systems rather than rebuilding them; planarian/Lobo/PLIMBO, Morpheus, PhysiCell, BioModels via SBMLtoODEjax, Planform and Limbform are candidate routes depending on the question.
5. **Goal Discovery on richer external systems.** Withhold semantics only after the constructive/white-box behavior is reproduced and understood, and compare the blind analyst against explicit rival criteria rather than only the authored label.

The question for phase 2 is not merely whether a richer system regenerates. It is whether the distinctions learned in the small systems — goal/reference representation, current-state information, memory, reachable action repertoire, reporter integrity, and intervention design — **predict or explain non-obvious behavior and failure boundaries in a system not built to validate those distinctions**.

The stronger combined benchmark is to use the **same independently authored system** in two roles: first map causal constraints white-box, then deliberately restrict the analyst and ask which goal/competence structure remains identifiable. See [research landscape](reference/research-landscape.md) and the [Levin software survey](reference/levin-software-ecosystem-survey.md) for comparators and substrate candidates. The existing D1-D6 register in [goals.md](goals.md) remains the detailed source for the discovery arm. Native experiment evidence wins over this summary if they conflict.

## Questions deliberately not required

- A universal scalar ordering of systems by "competence."
- A proof that a system has one and only one true goal.
- A universal internal state container for every possible system.
- A demonstration that every interesting collective effect is emergent in a strong philosophical sense.
- A claim that familiar control, fault-diagnosis, self-stabilization, regenerative, bioelectric, goal-scaling, or multiscale-competency principles are novel merely because they are expressed in this programme's vocabulary.
- More formalism or governance unless a concrete research question needs it.
