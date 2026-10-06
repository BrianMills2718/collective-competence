---
doc-role: working-research-questions
authority: derived
lifecycle: active
sources:
  - ontology.md
  - goals.md
  - reference/research-landscape.md
  - reference/levin-software-ecosystem-survey.md
  - reference/goal-competence-identifiability-landscape.md
  - ../goal-discovery/docs/PROJECT.md
  - current.md
---
# Research questions

This is a derived working synthesis of the programme's live questions. Accepted plans authorize bounded future work; native experiment records/evidence determine what has been answered.

[Wiki home](index.md) · [Findings](findings.md) · [Current work](current.md) · [Concepts](concepts.md)

## Central question

> **Given a dynamical system, a family of candidate goal criteria, a family of challenges, and a declared observation/intervention contract, which equivalence class of criteria and competence profiles is identifiable from behavior, and which experimentally separable constraints predict the system's competence and failure boundaries?**

The programme approaches that question from two directions. **Collective Competence** maps causal constraints on competence through intervention and mechanism analysis. **Goal and Competence Discovery** restricts analyst access and asks which goal criteria and competence claims the resulting behavior actually discriminates. The same Dynamical Laboratory supports both.

Neither arm requires a unique scalar notion of "more competent," and discovery does not require one uniquely identifiable true goal. A result may support several candidate criteria or remain underdetermined. The scientific burden is to state what the evidence discriminates, what challenge was used to test competence, and what would falsify the proposed explanation.

The project's earlier umbrella question — how component capabilities and interactions produce goal-relative competencies of a whole, and what can be inferred about them from behavior — remains historical motivation. It is no longer precise enough to serve as the test standard because broad local-to-global competence and many generic inference ingredients are already well occupied by prior work.

### Novelty guardrail

The September 2026 [research landscape](reference/research-landscape.md), [Levin-lab software ecosystem survey](reference/levin-software-ecosystem-survey.md), and broader [goal/competence identifiability landscape](reference/goal-competence-identifiability-landscape.md) materially narrow the novelty claims available to this programme.

Many broad constructive formulations are already well occupied: local-to-global morphogenetic competence, component-competency effects, scaling of homeostatic goals, bioelectric coordination, distributed pattern information/memory, reachability/path-dependence maps, and mechanism inference from perturbation/phenotype data all have substantial prior art and in several cases executable software.

The broader identifiability audit also shows that several ideas previously treated as candidate distinctive methodology are **established in neighboring fields**: trajectory-first behavioral descriptions, observational/interventional equivalence classes, partial identifiability, active experiment design to discriminate rival hypotheses, candidate-goal recognition, Goal Recognition Design, specification mining from traces, and black-box active automata learning. In particular, “preserve ambiguity and choose the next intervention that separates surviving candidate goals” is not new in the abstract.

Accordingly, **the programme does not claim novelty for the existence of those phenomena, for the generic identifiability recipe, or for renaming established control/inference concepts**. The stronger current burden is narrower: determine whether a challenge-relative *competence* layer adds information beyond ordinary property/specification or goal inference, make intervention-grounded predictions that transfer to independently authored systems, and state exactly which claims remain identifiable under a declared contract.

The central question is therefore a **synthesis/benchmark hypothesis, not an established novelty claim**. It earns distinctiveness only through results that established neighboring methods do not already provide.

## Constructive questions

1. **Which mechanisms and component capabilities are causally load-bearing for a system-level competency?** Begin where mechanisms are inspectable, then test whether the same intervention distinction survives in richer external systems.
2. **Which capabilities and couplings solve which challenge?** Remove, weaken, replace, or vary them under matched controls rather than assigning semantics from architecture alone.
3. **What makes successful behavior persist under changed conditions?** Distinguish reaching, maintaining, restoring, compensating, adapting, and learning.
4. **Where are the boundaries of the competency?** Noise, damage, hidden-state corruption, changed initial conditions, resource limits, altered topology, and sensor/actuator faults constrain explanations.
5. **Which hypothesized capability distinctions transfer?** Desired-state information, current-state observation, memory, action repertoire, plasticity, communication, and fault diagnosis are working intervention axes, not assumed universal natural kinds.
6. **Which effects survive increasing complexity and substrate change?** A relationship demonstrated in a hand-authored toy remains local until it prospectively predicts behavior in a richer or independently specified system.

For phase 2+, a constructive result is strongest when it makes a **risky prediction before the intervention**: intervention X should shift a recovery/failure boundary relative to Y for a stated causal reason, and an alternative outcome would count against that explanation.

## Discovery questions

1. **Which candidate goal criteria are supported by behavior without supplying the semantic answer to the analyst?** A candidate should earn support through behavior beyond the observations used to propose it.
2. **What distinguishes a descriptive regularity from active goal-relative competence?** A mined specification, passive attractor, hard constraint, and active controller may fit the same nominal trajectories; perturbations must separate mere satisfaction from maintenance, restoration, compensation or adaptation.
3. **Which aspects of competence can actually be demonstrated?** Attainment, maintenance, reliability, efficiency, robustness, recovery, adaptation, flexibility, and transfer are separate measurements; experiments need only claim what they test.
4. **When is the evidence underdetermined?** Several goal descriptions may remain behaviorally equivalent under the available observation and intervention contract. That is a legitimate result, not a failure to force a label.
5. **What additional observation or intervention would discriminate rival explanations?** Reuse optimal experiment design, active diagnosis, Goal Recognition Design or related machinery when their assumptions fit instead of treating this question as a new generic algorithmic problem.
6. **Can useful goal/competence structure be inferred in systems we did not author for the purpose of being inferred?** This is a stronger test than another bespoke calibration case.
7. **Does the competence layer add information beyond established baselines?** When a benchmark can be expressed as LTL/STL specification mining, goal recognition, IRL, active diagnosis, causal discovery or finite-state active learning, compare against the native method and identify the incremental claim precisely.

A discovery result is not strongest when it merely guesses the author's target label. It is strongest when the analyst is **calibrated**: it recovers a criterion at the resolution actually supported by the evidence, preserves equivalence classes where rivals survive, abstains from stronger semantic claims, identifies the intervention that would separate those rivals, and demonstrates competence information that a descriptive property learner would miss.

### Discovery stop rule

If an established method already answers the benchmark under its native assumptions and the competence layer adds no independently validated information, classify the work as an **application/comparison**, not a new discovery framework. Specialized methods should normally beat a substrate-neutral wrapper on their home domain.

## Current concrete programme

The first phase established a set of small calibration and primitive specimens: self-sorting, passive versus feedback regulation, bounded compensation, retained history-dependent adaptation, many-state pattern repair, structural regrowth, endogenous size/composition signals, generative plasticity, learned setpoint memory, and explicit observation/fault-identifiability limits. These are **building blocks and calibration surfaces**, not a general theory and not novelty claims for the underlying phenomena.

The original project strategy was a Robinson-Crusoe-style construction: keep the experimental discipline reusable while moving from simple systems to progressively richer compositions. The current priority is therefore **compositional scaling and external interrogation**, not another sequence of isolated one-purpose toys and not another substrate rewrite.

The intended complexity path is:

1. **Primitive calibrations — substantially complete.** Small systems establish clean distinctions and controls.
2. **Compositional mesoscopic system — current phase.** Use a richer externally specified local system containing many interacting sites, hidden state, development, persistence, and regeneration. The first target is the published **Growing Neural Cellular Automata** system.
3. **Close external comparators and developmental systems.** Prefer existing systems selected for a concrete prediction: e.g. Cellnition/RNM for reachability/control comparison, MinimalDevelopmentalComputation for regenerative local-controller transfer, LENIA Umwelt for blinded sensory/goal inference, or BioElectricNetwork/NeuralPlatePatterning/BETSE when a bioelectric hypothesis is required.
4. **Mechanistic biological models and real corpora.** Wrap established models/platforms or SBML systems rather than rebuilding them; planarian/Lobo/PLIMBO, Morpheus, PhysiCell, BioModels via SBMLtoODEjax, Planform and Limbform are candidate routes depending on the question.
5. **Goal/competence identification on richer external systems.** Withhold semantics only after the constructive/white-box behavior is reproduced and understood; compare the blind analyst against explicit rival criteria and against the appropriate specification-mining/goal-recognition/identification baseline.

The question for phase 2 is not merely whether a richer system regenerates. It is whether the distinctions learned in the small systems — goal/reference representation, current-state information, memory, reachable action repertoire, reporter integrity, and intervention design — **predict or explain non-obvious behavior and failure boundaries in a system not built to validate those distinctions**.

The stronger combined benchmark is to use the **same independently authored system** in two roles: first map causal constraints white-box, then deliberately restrict the analyst and ask which goal/competence structure remains identifiable. A particularly important control is to compare criterion inference against ordinary trace/specification inference and ask whether challenge-based intervention evidence supports a stronger claim of active maintenance, recovery, compensation or adaptation.

See [research landscape](reference/research-landscape.md), the [Levin software survey](reference/levin-software-ecosystem-survey.md), and the [goal/competence identifiability landscape](reference/goal-competence-identifiability-landscape.md) for comparators, prior art and baseline requirements. The existing D1-D6 register in [goals.md](goals.md) remains the detailed source for the discovery arm. Native experiment evidence wins over this summary if they conflict.

## Questions deliberately not required

- A universal scalar ordering of systems by "competence."
- A proof that a system has one and only one true goal.
- A universal internal state container for every possible system.
- A demonstration that every interesting collective effect is emergent in a strong philosophical sense.
- A claim that familiar control, fault-diagnosis, identifiability, active-discrimination, specification-mining, goal-recognition, self-stabilization, regenerative, bioelectric, goal-scaling, or multiscale-competency principles are novel merely because they are expressed in this programme's vocabulary.
- More formalism or governance unless a concrete research question needs it.
