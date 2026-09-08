# Research landscape — September 2026

[Reference index](README.md) · [Research questions](../questions.md) · [Current work](../current.md)

This is a **warm reference**, not a hot status page. It records the neighboring literatures that constrain novelty claims and help choose richer external specimens. The purpose is to identify what is already established, what this project is combining, and where stronger evidence would have to come from.

## Bottom line

Most individual primitives currently used by the project are **not novel in isolation**. That is expected and useful.

- observability, controllability/reachability, state estimation, and regulation are classical control concepts;
- fault detection/isolation/diagnosability is a mature control and discrete-event-systems field;
- distributed self-stabilization already studies local rules that recover global legitimate states after transient faults;
- inverse optimal control, inverse reinforcement learning, and goal/plan recognition already infer objectives from behavior under stronger assumptions than this project usually wants to make;
- regenerative biology already separates positional information, stem-cell/generative capacity, plasticity, and persistent pattern memory;
- Levin/TAME and multiscale-competency work already frame development and regeneration as collective problem-solving in anatomical state spaces.

The plausible contribution is therefore **not a renamed version of these primitives**. It is an integrated experimental programme that:

1. treats competence as goal- and challenge-relative rather than a universal scalar;
2. permits relational/equivalence-class candidate goals and explicit underdetermination;
3. uses the same executable systems for white-box mechanism analysis and restricted black-box goal/competence inference;
4. separates desired-state information, current-state evidence, memory, action repertoire/reachability, plasticity, and fault diagnosability;
5. tests whether those distinctions predict behavior across increasingly rich and externally specified substrates.

That integrated contribution is plausible but **not yet established as novel**.

## 1. Project strategy already anticipated progressive complexity

The retained Robinson-Crusoe brief says the computational programme should use **one reusable experimental substrate, progressively richer systems, thin slices, and maximum reuse of existing tooling**. It explicitly describes a path from simple local rules through stateful/adaptive components and coupled systems.

The active interpretation is that the reusable object is primarily the **Dynamical Laboratory discipline**, not one universal Python state container. A published NCA, Morpheus model, PhysiCell simulation, or other executable world can be a substrate/backend if it supports reproducible trajectories, observations, interventions, and evidence custody.

Internal source: [`goal-discovery/docs/sources/briefs/Addendum_3_Robinson_Crusoe_Dynamical_Laboratory.md`](../../goal-discovery/docs/sources/briefs/Addendum_3_Robinson_Crusoe_Dynamical_Laboratory.md).

## 2. Diverse intelligence and multiscale competency

Michael Levin's TAME framework treats cognition/agency as an empirically investigable continuum across unconventional substrates and explicitly connects development/regeneration to problem-solving in anatomical spaces. McMillen & Levin's 2024 perspective describes biology as a **multiscale competency architecture** in which molecular networks, cells, tissues, organisms, and swarms solve problems in different spaces.

**Established nearby:** multiscale biological competency; morphogenesis as basal cognition/problem-solving; perturbation and alternative means to similar ends.

**Implication here:** do not claim novelty for the high-level idea that cellular collectives can exhibit goal-directed anatomical competence. The project can contribute by making the claims operational, intervention-based, and comparable across artificial systems.

Sources:
- Levin, 2022, *Technological Approach to Mind Everywhere*, DOI `10.3389/fnsys.2022.768201`.
- McMillen & Levin, 2024, *Collective intelligence: A unifying concept for integrating biology across scales and substrates*, DOI `10.1038/s42003-024-06037-4`.

## 3. Control theory: observability, controllability, regulation

Classical state-space control already separates:

- **observability** — whether hidden state can be reconstructed from available input/output histories;
- **controllability/reachability** — whether admissible inputs/actions can move the system between relevant states;
- **state estimation**;
- **reference regulation and disturbance rejection**.

Modern work extends these ideas to nonlinear, switched, networked, Boolean, and other discrete systems.

**Established nearby:** several distinctions exposed by Experiments 09–11 are control-theoretic rather than new theoretical primitives.

**Implication here:** use the established terms where they fit, and ask what changes when observation/action channels are themselves biological collective products rather than engineered external interfaces.

Reference review: Zhang, 2023, *A survey on observability of Boolean control networks*, DOI `10.1007/s11768-022-00122-x`.

## 4. Fault diagnosis and active diagnosis

Fault diagnosis studies whether changes in behavior can be attributed to specific faults and how inputs/interventions can increase fault detectability. The field includes passive and **active** diagnosis, where diagnostic inputs are deliberately chosen to separate otherwise overlapping behavioral sets.

This is very close to the Experiment 11 "diagnostic birth" argument: an intervention can distinguish reporter health, while amount remains unidentifiable once the reporter is broken.

**Established nearby:** fault detection, isolation, estimation, diagnosability, analytical redundancy, active input design.

**Implication here:** reporter-failure work should connect to fault-diagnosis theory instead of inventing a parallel vocabulary. The potentially interesting biological twist is that the reporter can be produced by the same lineage whose abundance it reports.

Reference review: Sheikhi et al., 2026, *Fault Diagnosis in Dynamical Systems: Geometric Interpretation and Tractable Algorithms*, DOI `10.1146/annurev-control-030123-015422`.

## 5. Self-stabilizing distributed systems

Dijkstra-style self-stabilization asks whether a distributed system can recover to a legitimate global state from arbitrary/transiently corrupted states using local rules. Graph coloring is an established self-stabilizing problem family.

**Established nearby:** Experiment 05's constructive coloring mechanism is not a novel distributed algorithmic phenomenon.

**What remains useful here:** it provides a transparent specimen where the **goal criterion is an equivalence class/relation rather than one target state**, and where a blind analyst can be tested on recovering that fact.

Reference: Guellati & Kheddouci, 2010, *A survey on self-stabilizing algorithms for independence, domination, coloring, and matching in graphs*, DOI `10.1016/j.jpdc.2009.11.006`.

## 6. Inverse objective inference: IOC, IRL, goal recognition

Inverse optimal control (IOC), inverse reinforcement learning (IRL), goal recognition, plan recognition, and Bayesian inverse planning infer objectives or intentions from observed behavior. A central problem is **ill-posedness/non-uniqueness**: many objectives can explain the same finite behavior.

**Established nearby:** objective inference from behavior and the fact that the inverse problem is often non-unique.

**Potentially distinctive question here:** can useful candidate goals/competence profiles be inferred for arbitrary dynamical systems **without assuming an agent, known action semantics, an MDP, optimality, or a unique reward function**? The project also explicitly permits relational criteria and abstention/underdetermination.

This is the area where novelty is least resolved and deserves a deeper dedicated survey before any claim.

Reference: Arora & Doshi, 2021 (published online 2020), *From inverse optimal control to inverse reinforcement learning: A historical review*, DOI `10.1016/j.arcontrol.2020.06.001`.

## 7. Regenerative biology: positional information, generative capacity, memory

Planarian regeneration is an especially relevant biological anchor. Current reviews emphasize that correct regeneration requires both:

- a generative cell repertoire (notably neoblast stem cells and lineage potential);
- positional information that tells the system what structure is missing and where it belongs.

Regeneration research also includes persistent bioelectric/anatomical memories and long-lived positional memory. These are direct biological neighbors of the project's distinctions among desired-state information, current-state evidence, memory, and plasticity.

**Established nearby:** information and generative capacity are jointly required; long-lived pattern/positional memories can influence future regeneration.

**Implication here:** Experiments 09–11 should be treated as transparent artificial decompositions of known biological themes, not as biological novelty claims. Their value is in giving exact controls and in preparing predictions for richer systems.

Reference review: *Stem cells (neoblasts) and positional information jointly dominate regeneration in planarians*, Heliyon 2025, DOI `10.1016/j.heliyon.2025.e41833`.

## 8. Neural Cellular Automata — first phase-2 external rung

Mordvintsev et al.'s **Growing Neural Cellular Automata (NCA)** is an unusually good bridge between the project's transparent primitives and richer biological models.

The canonical system has:

- a 2-D grid;
- vector-valued cell state including hidden channels;
- a shared learned local neural update rule;
- stochastic/asynchronous updates;
- growth from a seed;
- persistence training;
- regeneration training and damage recovery;
- fully executable white-box dynamics that are nevertheless too complex to explain by inspection alone.

The 2020 Distill work explicitly provides growing, persistent, and regeneration-trained variants. A 2026 Physics of Life Reviews survey presents NCA as a framework for biological self-organization and multiscale competency while naming **interpretability, scaling, and integration with biological data** as major limitations/open problems.

This makes NCA a good test of whether the project's decomposition can explain behavior in a system **not authored to validate it**.

Sources:
- Mordvintsev, Randazzo, Niklasson & Levin, 2020, *Growing Neural Cellular Automata*, DOI `10.23915/distill.00023`, canonical article: https://distill.pub/2020/growing-ca/
- source repository: https://github.com/distillpub/post--growing-ca (CC-BY-4.0 repository/article materials)
- Hartl, Levin & Pio-Lopez, 2026, *Neural cellular automata: Applications to biology and beyond classical AI*, DOI `10.1016/j.plrev.2025.11.010`.

## 9. Richer multicellular platforms

The next complexity rung does not require building a general tissue simulator.

**Morpheus** integrates cell-based models with ODEs, stochastic/delay equations, reaction-diffusion systems, cell motility, adhesion, and Cellular Potts models in 2-D/3-D. It is designed for multiscale systems biology and has been used for morphogenesis and cell-fate studies.

**PhysiCell** is an open-source off-lattice 3-D multicellular simulator coupled to diffusing biochemical fields, with cell mechanics and phenotype behaviors.

**Implication here:** if the NCA rung succeeds, choose a published model on an established platform and wrap it through the laboratory contract. Do not evolve the custom 1-D lattice into a universal multicellular engine.

Sources:
- Starruß et al., 2014, *Morpheus: a user-friendly modeling environment for multiscale and multicellular systems biology*, DOI `10.1093/bioinformatics/btt772`.
- Ghaffarizadeh et al., 2018, *PhysiCell: An open source physics-based cell simulator for 3-D multicellular systems*, DOI `10.1371/journal.pcbi.1005991`.

## 10. Current novelty assessment

| Project element | Current novelty assessment |
|---|---|
| Local rules yielding legitimate global states | Established self-stabilization territory |
| Feedback, disturbance rejection, observability/reachability | Established control theory |
| Reporter failure and diagnostic interventions | Established fault-diagnosis territory |
| Positional information + generative plasticity/memory | Established regenerative-biology themes |
| Anatomical/morphogenetic collective competence | Active Levin/multiscale-competency programme |
| Reward/objective inference from behavior | Large IOC/IRL/goal-recognition literature |
| Candidate-goal inference for arbitrary dynamical systems without optimality/agent assumptions | **Potentially distinctive; not yet established** |
| White-box construction + restricted black-box discovery on the same known-ground-truth systems | **Potentially distinctive methodology** |
| One experimental decomposition spanning reference, current observation, memory, action repertoire, and fault diagnosis across substrates | **Potentially useful synthesis; must earn generality externally** |

## 11. Strategic ladder from here

**Rung 0 — primitive calibrations:** sorting, regulation, compensation, history-dependent adaptation. **Done enough.**

**Rung 1 — simple morphogenetic primitives:** many-state pattern repair, regrowth, size/composition sensing, plasticity, learned memory, fault-identifiability limits. **Done enough.**

**Rung 2 — compositional mesoscopic system:** externally specified NCA with many local states and nontrivial learned dynamics. **Current phase.**

**Rung 3 — mechanistic multicellular model:** imported/published Morpheus, PhysiCell, reaction-diffusion, Cellular Potts, or comparable model chosen for a specific prediction.

**Rung 4 — biologically anchored regeneration:** planarian or comparable model/data where positional information, plasticity, and memory have direct experimental interpretation.

**Rung 5 — Goal Discovery on systems not authored by this project:** strongest eventual test of the analytic arm.

The ladder is not a required chronology if a better externally specified specimen appears. Its purpose is to prevent **serial toy replacement** while retaining the explanatory clarity earned by small models.
