---
doc-role: working-research-questions
authority: working-summary
lifecycle: active
sources:
  - ontology.md
  - goals.md
  - reference/research-landscape.md
  - ../goal-discovery/docs/PROJECT.md
  - ../goal-discovery/docs/plans/current_research_plan.md
---
# Research questions

[Wiki home](index.md) · [Findings](findings.md) · [Current work](current.md) · [Concepts](concepts.md)

## Central question

**How do simple component capabilities and interactions produce robust, goal-relative competencies of a whole, and what can we infer about those competencies and candidate goals from the system's behavior?**

The programme approaches that question from two directions. **Collective Competence** constructs systems and varies their mechanisms. **Goal and Competence Discovery** observes and intervenes on systems and asks what goal criteria and competence claims the behavior supports, contradicts, or leaves underdetermined. The same Dynamical Laboratory supports both.

Neither arm requires a unique scalar notion of "more competent," and Goal Discovery does not require one uniquely identifiable true goal. A result may support several candidate criteria or remain underdetermined. The scientific burden is to state what the evidence actually discriminates.

## Constructive questions

1. **What mechanisms and component capabilities produce a system-level competency?** Begin where mechanisms are inspectable, then test whether the same decomposition survives in richer systems.
2. **Which capabilities and couplings are load-bearing?** Remove, weaken, replace, or vary them and identify what challenge each one actually solves.
3. **What makes successful behavior persist under changed conditions?** Distinguish reaching, maintaining, restoring, compensating, adapting, and learning.
4. **Where are the boundaries of the competency?** Noise, damage, hidden-state corruption, changed initial conditions, resource limits, altered topology, and sensor/actuator faults constrain explanations.
5. **How do simple capabilities compose?** Desired-state information, current-state observation, memory, action repertoire, plasticity, communication, and fault diagnosis should be treated as separable until experiments show how they interact.
6. **Which effects survive increasing complexity?** A relationship demonstrated in a hand-authored toy remains local until it predicts behavior in a richer or externally specified system.

## Discovery questions

1. **Which candidate goal criteria are supported by behavior without supplying the semantic answer to the analyst?** A candidate should earn support through behavior beyond the observations used to propose it.
2. **What distinguishes active goal-directed performance from passive convergence or an attractor?** Interventions are especially useful when ordinary trajectories look alike.
3. **Which aspects of competence can actually be demonstrated?** Attainment, maintenance, reliability, efficiency, robustness, recovery, adaptation, flexibility, and transfer are separate measurements; experiments need only claim what they test.
4. **When is the evidence underdetermined?** Several goal descriptions may remain behaviorally equivalent under the available observation and intervention contract. That is a legitimate result, not a failure to force a label.
5. **What additional observation or intervention would discriminate rival explanations?** This includes ordinary mechanism ambiguity and fault-diagnosis/observability limits.
6. **Can useful goal/competence structure be inferred in systems we did not author for the purpose of being inferred?** This is a stronger test than another bespoke calibration case.

## Current concrete programme

The first phase established a set of small calibration and primitive specimens: self-sorting, passive versus feedback regulation, bounded compensation, retained history-dependent adaptation, many-state pattern repair, structural regrowth, endogenous size/composition signals, generative plasticity, learned setpoint memory, and explicit observation/fault-identifiability limits. These are **building blocks and calibration surfaces**, not a general theory.

The original project strategy was a Robinson-Crusoe-style construction: keep the experimental discipline reusable while moving from simple systems to progressively richer compositions. The current priority is therefore **compositional scaling**, not another sequence of isolated one-purpose toys and not another substrate rewrite.

The intended complexity path is:

1. **Primitive calibrations — substantially complete.** Small systems establish clean distinctions and controls.
2. **Compositional mesoscopic system — current phase.** Use a richer externally specified local system containing many interacting sites, hidden state, development, persistence, and regeneration. The first target is the published **Growing Neural Cellular Automata** system.
3. **Mechanistic multicellular models.** When justified, wrap an established platform or published model such as Morpheus, PhysiCell, or a comparable developmental/regenerative system rather than rebuilding it inside the custom lattice.
4. **Biologically anchored regeneration.** Test the decomposition against published systems with meaningful positional information, plasticity, memory, and perturbation data, with planarian regeneration as a strong candidate domain.
5. **Goal Discovery on richer external systems.** Withhold semantics only after the constructive/white-box behavior is reproduced and understood.

The question for phase 2 is not merely whether a richer system regenerates. It is whether the distinctions learned in the small systems — goal/reference representation, current-state information, memory, reachable action repertoire, reporter integrity, and intervention design — **predict or explain non-obvious behavior and failure boundaries in a system not built to validate those distinctions**.

See [research landscape](reference/research-landscape.md) for the neighboring literatures and current novelty assessment. The existing D1-D6 register in [goals.md](goals.md) remains the detailed source for the discovery arm. Native experiment evidence wins over this summary if they conflict.

## Questions deliberately not required

- A universal scalar ordering of systems by "competence."
- A proof that a system has one and only one true goal.
- A universal internal state container for every possible system.
- A demonstration that every interesting collective effect is emergent in a strong philosophical sense.
- A claim that familiar control, fault-diagnosis, self-stabilization, or regenerative principles are novel merely because they are expressed in this programme's vocabulary.
- More formalism or governance unless a concrete research question needs it.
