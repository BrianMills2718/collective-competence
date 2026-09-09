# Research landscape — September 2026

[Reference index](README.md) · [Research questions](../questions.md) · [Current work](../current.md) · [Levin software ecosystem survey](levin-software-ecosystem-survey.md)

This is a **warm reference**, not a hot status page. It records the neighboring literatures that constrain novelty claims and help choose richer external specimens. The purpose is to identify what is already established, what this project is combining, and where stronger evidence would have to come from.

## Bottom line

Most individual primitives currently used by the project are **not novel in isolation**. A September 2026 package-by-package audit of the Levin-lab software ecosystem makes this conclusion stronger than the earlier paper-level survey did.

- observability, controllability/reachability, state estimation, and regulation are classical control concepts;
- fault detection/isolation/diagnosability is a mature control and discrete-event-systems field;
- distributed self-stabilization already studies local rules that recover global legitimate states after transient faults;
- inverse optimal control, inverse reinforcement learning, and goal/plan recognition already infer objectives from behavior under stronger assumptions than this project usually wants to make;
- regenerative biology already separates positional information, stem-cell/generative capacity, plasticity, and persistent pattern memory;
- Levin/TAME and multiscale-competency work already frame development and regeneration as collective problem-solving in anatomical state spaces;
- the associated executable ecosystem already contains direct demonstrations of cellular competency, goal scaling, stress-mediated coordination, resource-mediated coordination, regenerative local-controller networks, bioelectric computation, multiscale NCA memory/repair, intervention/reachability maps, and automated inference of regulatory mechanisms from perturbation/phenotype data.

The detailed audit is in [Levin-lab software ecosystem survey](levin-software-ecosystem-survey.md). In particular, **Cellular Competency**, **Scale-free Cognition**, **MinimalDevelopmentalComputation**, **Muse**, **Stress Sharing**, **Cellnition/Regulatory Network Machine**, **BETSE/BioElectricNetwork**, the Lobo planarian inference system, and **Sorting Algorithms as Basal Cognition** substantially narrow what this repository can responsibly present as novel.

The plausible contribution is therefore **not a renamed version of these primitives and not another demonstration that cellular collectives can be competent**. The strongest remaining programme is an intervention-grounded experimental epistemology of competence:

1. treat competence as goal- and challenge-relative rather than a universal scalar;
2. permit relational/equivalence-class candidate goals and explicit underdetermination;
3. declare exactly what observations and interventions an analyst is allowed;
4. distinguish white-box causal/mechanistic analysis from restricted black-box candidate-goal/competence inference on the same external systems;
5. ask what additional intervention would discriminate rival explanations;
6. test whether separable capability constraints make **risky predictions of non-obvious failure-boundary shifts across independently authored systems**.

Those claims are **potentially distinctive, not established as novel**. They now carry a stronger burden: the programme must demonstrate transfer and calibrated inference rather than accumulate bespoke examples.

## 1. Project strategy already anticipated progressive complexity and reuse

The retained Robinson-Crusoe brief says the computational programme should use **one reusable experimental substrate, progressively richer systems, thin slices, and maximum reuse of existing tooling**. The older Dynamical Laboratory specification is even more explicit: the reusable scientific object is the trajectory plus metadata; published executable worlds and existing traces should be ingestible; mature infrastructure should not be reinvented.

The active interpretation is that the reusable object is primarily the **Dynamical Laboratory discipline**, not one universal Python state container. A published NCA, Cellnition model, MinimalDevelopmentalComputation system, BETSE/BioElectricNetwork model, SBML model, Morpheus model, PhysiCell simulation, or other executable world can be a substrate/backend if it supports reproducible trajectories, observations, interventions, and evidence custody.

Internal source: [`goal-discovery/docs/sources/briefs/Addendum_3_Robinson_Crusoe_Dynamical_Laboratory.md`](../../goal-discovery/docs/sources/briefs/Addendum_3_Robinson_Crusoe_Dynamical_Laboratory.md) and the retained coding-agent specification.

**Operational consequence:** before implementing another dynamical system, first ask whether an externally authored executable model already contains the phenomenon needed for the hypothesis. The default is now **wrap, intervene, and compare**, not build.

## 2. Diverse intelligence and multiscale competency

Michael Levin's TAME framework treats cognition/agency as an empirically investigable continuum across unconventional substrates and explicitly connects development/regeneration to problem-solving in anatomical spaces. McMillen & Levin's 2024 perspective describes biology as a **multiscale competency architecture** in which molecular networks, cells, tissues, organisms, and swarms solve problems in different spaces.

**Established nearby:** multiscale biological competency; morphogenesis as basal cognition/problem-solving; perturbation and alternative means to similar ends.

The software audit adds direct executable neighbors:

- **Cellular Competency** varies local cell problem-solving and measures evolutionary/developmental consequences;
- **Scale-free Cognition** explicitly studies scaling homeostatic goals from cells to anatomy;
- **Muse** evolves multiscale NCA competency and studies morphology loss, communication, persistent information and regenerative restoration;
- **Distributed Agential Chess** studies component-level agency outside biology;
- **Sorting Algorithms as Basal Cognition** directly covers the conceptual territory of our Experiment 01.

**Implication here:** do not claim novelty for the high-level idea that cellular collectives can exhibit goal-directed anatomical competence, that component competence can affect whole behavior, or that goals can scale across levels. The project can contribute only by making narrower claims operational, intervention-based, transferable, and epistemically calibrated.

Sources:
- Levin, 2022, *Technological Approach to Mind Everywhere*, DOI `10.3389/fnsys.2022.768201`.
- McMillen & Levin, 2024, *Collective intelligence: A unifying concept for integrating biology across scales and substrates*, DOI `10.1038/s42003-024-06037-4`.
- Shreesha & Levin, 2023, *Cellular Competency during Development Alters Evolutionary Dynamics...*, DOI `10.3390/e25010131`.
- Pio-Lopez et al., 2023, *The scaling of goals from cellular to anatomical homeostasis*, DOI `10.1098/rsfs.2022.0072`.

## 3. Control theory: observability, controllability, regulation

Classical state-space control already separates:

- **observability** — whether hidden state can be reconstructed from available input/output histories;
- **controllability/reachability** — whether admissible inputs/actions can move the system between relevant states;
- **state estimation**;
- **reference regulation and disturbance rejection**.

Modern work extends these ideas to nonlinear, switched, networked, Boolean, and other discrete systems.

**Established nearby:** several distinctions exposed by Experiments 09–11 are control-theoretic rather than new theoretical primitives.

**Implication here:** use established terms where they fit, and ask what changes when observation/action channels are themselves biological collective products rather than engineered external interfaces.

Reference review: Zhang, 2023, *A survey on observability of Boolean control networks*, DOI `10.1007/s11768-022-00122-x`.

## 4. Regulatory Network Machine / Cellnition: a particularly close reachability neighbor

The 2025 **Regulatory Network Machine (RNM)** framework is important enough to name separately rather than subsume under generic control theory. RNM treats a regulatory network as a dissipative dynamical system with applied inputs and meaningful output equilibria. Network Finite State Machines map input-driven state transitions and expose path dependencies, irreversible transitions, cycles and unreachable equilibria; pathway analysis then finds interventions that reach desired output states.

**Established nearby:** much of what we might call intervention maps, action/reachability, stable history dependence, multi-stage cycles, or persuasive routes to a target state is already explicit in RNM and its Python implementation **Cellnition**.

**Crucial difference from Goal Discovery:** RNM assumes output states with relevance to biomedical/technical objectives already identified. Our discovery question remains distinct only if semantic answers are genuinely withheld and the analyst is asked which candidate goal criteria and competence claims are *identifiable* under a declared access contract, including cases where multiple criteria remain behaviorally equivalent.

This yields a direct benchmark: compare an RNM-style white-box/control analysis with a blinded Goal Discovery analysis of the same network. If the latter does not add a distinct epistemic problem, the discovery claim should be reduced rather than cosmetically renamed.

Sources:
- Pietak & Levin, 2025, *Harnessing the analog computing power of regulatory networks with the Regulatory Network Machine*, DOI `10.1016/j.isci.2025.112536`.
- Cellnition: `https://github.com/betsee/cellnition`.

## 5. Fault diagnosis and active diagnosis

Fault diagnosis studies whether changes in behavior can be attributed to specific faults and how inputs/interventions can increase fault detectability. The field includes passive and **active** diagnosis, where diagnostic inputs are deliberately chosen to separate otherwise overlapping behavioral sets.

This is very close to the Experiment 11 "diagnostic birth" argument: an intervention can distinguish reporter health, while amount remains unidentifiable once the reporter is broken.

**Established nearby:** fault detection, isolation, estimation, diagnosability, analytical redundancy, active input design.

**Implication here:** reporter-failure work should connect to fault-diagnosis theory instead of inventing a parallel vocabulary. The potentially interesting biological twist is that the reporter can be produced by the same lineage whose abundance it reports.

Reference review: Sheikhi et al., 2026, *Fault Diagnosis in Dynamical Systems: Geometric Interpretation and Tractable Algorithms*, DOI `10.1146/annurev-control-030123-015422`.

## 6. Self-stabilizing distributed systems and sorting

Dijkstra-style self-stabilization asks whether a distributed system can recover to a legitimate global state from arbitrary/transiently corrupted states using local rules. Graph coloring is an established self-stabilizing problem family.

The Levin-lab sorting work separately treats classical sorting algorithms as distributed morphogenetic/basal-cognition systems, tests unreliable elements, robustness, defect navigation and mixed policies.

**Established nearby:** Experiment 05's constructive coloring mechanism is not a novel distributed algorithmic phenomenon, and Experiment 01's distributed sorting phenomenon is direct prior-art territory.

**What remains useful here:** both provide transparent calibration specimens where we can test relational criteria, maintenance versus one-time attainment, blindness/access contracts and failure to over-infer semantics.

Sources:
- Guellati & Kheddouci, 2010, self-stabilization survey, DOI `10.1016/j.jpdc.2009.11.006`.
- Zhang, Goldstein & Levin, sorting as morphogenesis, DOI `10.1177/10597123241269740`.

## 7. Inverse objective inference: IOC, IRL, goal recognition

Inverse optimal control (IOC), inverse reinforcement learning (IRL), goal recognition, plan recognition, Bayesian inverse planning and adjacent fields infer objectives or intentions from observed behavior. A central problem is **ill-posedness/non-uniqueness**: many objectives can explain the same finite behavior.

**Established nearby:** objective inference from behavior and the fact that the inverse problem is often non-unique.

**Potentially distinctive question here:** can useful candidate goals/competence profiles be inferred for arbitrary dynamical systems **without assuming an agent, known action semantics, an MDP, optimality, or a unique reward function**, while explicitly permitting relational criteria and abstention/underdetermination?

This remains the area where novelty is least resolved and deserves a deeper dedicated survey outside the Levin ecosystem before any claim.

Reference: Arora & Doshi, 2021 (published online 2020), *From inverse optimal control to inverse reinforcement learning: A historical review*, DOI `10.1016/j.arcontrol.2020.06.001`.

## 8. Other inverse-problem neighbors: mechanism and dynamics inference

Two software families sharpen the boundary around Goal Discovery.

### Lobo/Levin planarian regulatory-network inference

The 2015 system takes formalized surgical/genetic/pharmacological perturbation and morphology outcomes, searches regulatory networks, simulates the interventions and recovers mechanistic networks explaining the observed phenotype corpus.

**Established nearby:** automated inverse inference from morphological perturbation data is not new.

**Difference:** this system infers **mechanism** from semantically identified phenotypes. Goal Discovery is only distinct when it asks what *high-level goal/competence interpretations* are licensed without being handed the authored semantic criterion.

Reference: Lobo & Levin, 2015, DOI `10.1371/journal.pcbi.1004295`.

### Equilibrium Flow

Zhang & Levin's 2025 Equilibrium Flow asks how a static pattern distribution constrains possible underlying dynamics and explicitly finds a solution space shaped by data and inductive bias; it also inverse-designs dynamics that preserve target pattern distributions.

**Implication:** non-uniqueness should be treated as a default property of inverse dynamical inference, not as a special nuisance of our discovery machinery.

Reference: arXiv `2509.17990`.

## 9. Regenerative biology: positional information, generative capacity, memory

Planarian regeneration is an especially relevant biological anchor. Current reviews emphasize that correct regeneration requires both:

- a generative cell repertoire (notably neoblast stem cells and lineage potential);
- positional information that tells the system what structure is missing and where it belongs.

Regeneration research also includes persistent bioelectric/anatomical memories and long-lived positional memory. These are direct biological neighbors of the project's distinctions among desired-state information, current-state evidence, memory and plasticity.

The software ecosystem adds **PLIMBO**, Planform, Limbform, a reverse-engineered planarian regulatory model, **NeuralPlatePatterning**, **BETSE**, **BioElectricNetwork**, and **ElectricMorphogenesis** as concrete executable/data resources.

**Established nearby:** information and generative capacity are jointly required; long-lived pattern/positional memories can influence future regeneration; bioelectric networks can process pattern information; biologically grounded intervention models already exist.

**Implication here:** Experiments 09–11 are transparent calibrations of known themes, not biological novelty claims. Their value is in giving exact controls and preparing predictions for richer systems.

Reference review: *Stem cells (neoblasts) and positional information jointly dominate regeneration in planarians*, Heliyon 2025, DOI `10.1016/j.heliyon.2025.e41833`.

## 10. Existing developmental-computation systems close to our constructive arm

### MinimalDevelopmentalComputation

Manicka & Levin's hierarchical regenerative network uses local intracellular controllers within a tissue network and demonstrates pattern maintenance/regeneration, rescaling/canalization and distributed causal information.

**Implication:** this is a stronger next external benchmark than constructing another local-controller tissue toy. It can test whether our decomposition predicts non-obvious outcomes in a system not authored by us.

Reference: DOI `10.3390/e24010107`; repository `https://github.com/santamanicka/MinimalDevelopmentalComputation`.

### Stress Sharing and CompetitionAsCoordination

Stress sharing models an error-like variable communicated across a collective; finite resource reservoirs provide another emergent coordination medium. Both show that multiple low-level mechanisms can support global morphological coordination.

Most importantly for discovery, the stress-sharing paper reports that anatomical goal states were not recoverable merely from observed stress states.

**Implication:** do not infer a semantic goal from an internal error-like variable. Access and intervention determine what is identifiable.

References: DOI `10.1016/j.bbrc.2024.150396`; DOI `10.1016/j.biosystems.2022.104762`.

### Muse

The Muse hybrid-NCA framework studies multiscale developmental competency; associated aging work manipulates communication, competency, damage and regenerative information and reports persistent spatial information after organ loss.

**Implication:** memory/communication/repair/goal-directedness combinations are already directly represented in contemporary adjacent work. Our contribution must be predictive transfer or calibrated inference, not the vocabulary alone.

Repository: `https://github.com/bhartl/muse`.

## 11. Neural Cellular Automata — first active external rung

Mordvintsev et al.'s **Growing Neural Cellular Automata (NCA)** remains an unusually good bridge between transparent primitives and richer biological models.

The canonical system has a 2-D grid, vector-valued hidden cell state, a shared learned local update rule, stochastic/asynchronous updates, growth from a seed, persistence training and regeneration training.

Experiment 12 is therefore still well chosen. The audit changes the **claim**, not the specimen: regeneration itself is established. The valuable question is whether our intervention distinctions predict non-obvious recovery boundaries, latent-consistency effects and action/reachability failures in the fixed external model.

Sources:
- Mordvintsev et al., 2020, *Growing Neural Cellular Automata*, DOI `10.23915/distill.00023`.
- source repository: `https://github.com/distillpub/post--growing-ca`.
- Hartl, Levin & Pio-Lopez, 2026, NCA review, DOI `10.1016/j.plrev.2025.11.010`.

## 12. Bioelectric and multicellular platforms: do not build another engine

### BETSE and bioelectric systems

BETSE already supplies a 2-D multiphysics tissue engine for electrodiffusion, channels, gap junctions, GRNs and biochemical networks. BioElectricNetwork supplies a smaller computational bioelectric system; ElectricMorphogenesis and NeuralPlatePatterning provide more targeted models.

**Implication:** if the next hypothesis needs bioelectric tissue physics, wrap one of these systems. Do not evolve our custom lattice into a general bioelectric simulator.

### Morpheus and PhysiCell

Morpheus integrates cell-based models with ODEs, stochastic/delay equations, reaction-diffusion systems, motility, adhesion and Cellular Potts models in 2-D/3-D. PhysiCell is an open-source off-lattice 3-D multicellular simulator coupled to diffusing biochemical fields, with mechanics and phenotype behaviors.

These remain useful candidates when a specific published model on those platforms tests a prediction better than a Levin-lab system.

### SBMLtoODEjax and published biological models

SBMLtoODEjax can turn many existing SBML ODE models into JAX-compatible Python systems. It is an important **reuse-first import path**: before writing a new regulatory/biochemical ODE model, search BioModels/SBML for an existing system. Its documented coverage is incomplete, so compatibility must be checked per model.

Sources:
- BETSE: Pietak & Levin, 2016, Frontiers in Bioengineering and Biotechnology 4:55; current repository `https://github.com/betsee/betse`.
- BioElectricNetwork: DOI `10.1038/s41598-019-54859-8`.
- NeuralPlatePatterning: DOI `10.1016/j.isci.2023.108398`.
- Starruß et al., 2014, Morpheus, DOI `10.1093/bioinformatics/btt772`.
- Ghaffarizadeh et al., 2018, PhysiCell, DOI `10.1371/journal.pcbi.1005991`.
- SBMLtoODEjax: arXiv `2307.08452`.

## 13. Real intervention corpora: Planform and Limbform

Planform formalizes planarian surgery/perturbation/morphology experiments and its current site reports more than 1,500 entries. Limbform similarly formalizes more than 800 limb-regeneration experiments across multiple organisms.

**Implication:** these are better eventual tests of a mature discovery system than endlessly generated synthetic trajectories. They are heterogeneous and semantically richer, so they should come only after access-contract and equivalence-class behavior is reliable on executable systems.

Sources:
- `https://lobolab.umbc.edu/planform/`
- `https://lobolab.umbc.edu/limbform/`

## 14. Information measures and causal scale tools are methods, not competence semantics

Inform/PyInform, CAIM and causal-emergence tools already implement many information-theoretic and macro-scale analyses that might be useful. The original lab brief also anticipated Hoel-style comparison of representations/scales.

**Implication:** reuse mature measures where mathematically warranted. Do not turn active information storage, transfer entropy, effective information or a predictive coarse-graining into a semantic claim about "memory," "goal," or "agency" without an intervention or argument that supports that interpretation.

## 15. A particularly useful future Goal Discovery benchmark: LENIA Umwelt

The 2026 Lenia Umwelt work introduces regions from which agents receive no sensory information and reports avoidance behavior interpreted in relation to information occlusion and preservation of morphology.

This is attractive because it supplies:

- an independently authored non-developmental dynamical agent;
- a clean information-access perturbation;
- rival plausible higher-level interpretations;
- behavior rich enough that semantic withholding is meaningful.

A blinded analysis could ask whether morphology preservation, obstacle/region avoidance, information avoidance or a weaker equivalence class is actually supported by the interventions supplied.

Source: Cool et al., 2026, *Agnosiophobia in a virtual agent: behavioral and dynamical architecture in Lenia*, arXiv `2605.30708`.

## 16. Current novelty assessment after the software audit

| Project element | Current novelty assessment |
|---|---|
| Local rules yielding legitimate global states | Established self-stabilization / distributed-systems territory |
| Distributed sorting as basal competence | Direct nearby prior art |
| Component competency affects whole-level morphology/evolution | Direct nearby prior art (Cellular Competency) |
| Cellular homeostatic goals scale into anatomy | Direct nearby prior art (Scale-free Cognition) |
| Feedback, disturbance rejection, observability/reachability | Established control theory |
| Path-dependent reachability/intervention maps | Strong nearby implementation in RNM/Cellnition + control theory |
| Reporter failure and diagnostic interventions | Established fault-diagnosis territory |
| Positional information + generative plasticity/memory | Established regenerative-biology themes |
| Bioelectric computation/pattern control | Established and supported by multiple executable systems |
| Anatomical/morphogenetic collective competence | Active Levin/multiscale-competency programme |
| Mechanism inference from morphological perturbation data | Established nearby (Lobo/Levin) and broader systems biology |
| Reward/objective inference from behavior | Large IOC/IRL/goal-recognition literature |
| Candidate-goal inference for arbitrary dynamical systems without supplied semantics, optimality or agent assumptions | **Potentially distinctive; not yet established** |
| Explicit access-contract identifiability + equivalence classes + abstention | **Promising; requires broader prior-art survey and demonstration** |
| White-box causal map + restricted blind discovery on the same external system | **Potentially distinctive benchmark methodology** |
| One decomposition predicting failure-boundary shifts across independent substrates | **Potentially useful only if it makes successful risky predictions** |

## 17. Strategic ladder from here

The ladder is now **reuse-first** rather than substrate-construction-first.

**Rung 0 — primitive calibrations:** sorting, regulation, compensation, history-dependent adaptation. **Done enough; novelty not claimed.**

**Rung 1 — simple morphogenetic calibrations:** many-state pattern repair, regrowth, size/composition sensing, plasticity, learned memory, fault-identifiability limits. **Done enough; use as controlled calibration surfaces only.**

**Rung 2 — fixed external learned system:** Growing NCA. **Current phase.** Finish intervention predictions about lesion geometry/location/timing, latent consistency and available actions.

**Rung 2b — close comparator:** Cellnition/RNM. Clarify where reachability/control analysis ends and semantic candidate-goal identifiability begins.

**Rung 3 — externally authored developmental/bioelectric systems:** prioritize MinimalDevelopmentalComputation, LENIA Umwelt, BioElectricNetwork or NeuralPlatePatterning according to the hypothesis. BETSE is available when full tissue physics matters.

**Rung 4 — published mechanistic biological models:** use planarian/Lobo/PLIMBO, SBML/BioModels via SBMLtoODEjax, Morpheus/PhysiCell, or another published model chosen for a prediction rather than for platform prestige.

**Rung 5 — real biological intervention corpora:** Planform/Limbform or comparable data where observation semantics, penetrance, experimental heterogeneity and missing variables make identifiability genuinely difficult.

**Rung 6 — strongest discovery test:** semantics withheld on systems and data not authored for this programme, with predeclared access contracts and explicit rival candidate goals.

The sequence can skip rungs when a cleaner external test appears. The purpose is to prevent **serial toy replacement** while retaining the explanatory clarity earned by the calibrations.

## 18. What would count as progress now

A new experiment should preferably satisfy all of the following:

1. **Externality:** the system or phenomenon was not created to validate our decomposition.
2. **Prediction:** before running it, state which intervention outcome/failure-boundary ordering the framework predicts and what result would count against that explanation.
3. **Matched causal comparison:** preserve state/RNG and isolate the intervention variable where possible.
4. **Semantic discipline:** do not equate latent variables, stress, attractors, reward functions or authored targets with an identified goal unless the evidence warrants it.
5. **Identifiability accounting:** report rival candidate criteria still consistent with the observations and the intervention that would separate them.
6. **Reuse:** prefer existing executable models, formalized datasets and mature analysis tools over a new substrate implementation.

The core methodological aspiration can be stated compactly:

> **On the same independently authored system, can white-box interventions reveal causal constraints that predict competence boundaries while a deliberately restricted analyst recovers only the goal/competence structure actually identifiable from behavior?**

That is a stronger and less redundant target than another demonstration of collective competence.
