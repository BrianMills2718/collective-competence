---
doc-role: external-identifiability-landscape-survey
authority: research-reference
lifecycle: active
surveyed: 2026-09-09
sources:
  - research-landscape.md
  - levin-software-ecosystem-survey.md
  - ../questions.md
---
# Goal/competence identifiability: external landscape beyond the Levin ecosystem

[Reference index](README.md) · [Research landscape](research-landscape.md) · [Levin software survey](levin-software-ecosystem-survey.md) · [Research questions](../questions.md)

## Why this survey exists

The Levin-software audit showed that much of the constructive **collective competence** demonstration space is already occupied. This second audit asks a harder question: **is the proposed remaining niche — identifying candidate goals and competence claims from behavior under a declared observation/intervention contract — already established elsewhere under different names?**

The answer is: **many of its ingredients are already mature research problems, and several are much closer than the earlier research landscape acknowledged.** In particular, underdetermination, equivalence classes, black-box behavioral inference, active selection of discriminating interventions, candidate-goal recognition, and mining behavioral specifications are not novel ideas in isolation.

This does **not** show that the whole programme is redundant. It does change the burden of proof. The project should not claim novelty for an abstract recipe of “observe behavior, preserve ambiguity, intervene to discriminate.” That recipe appears in multiple established fields. Any distinctive contribution must come from the **specific scientific object and combination**: goal-relative *competence* of arbitrary dynamical systems, challenge-relative performance profiles, tests that distinguish active corrective steering from passive property satisfaction, and calibrated inference across independently authored morphogenetic/biological systems without assuming an MDP, planner, known action semantics, or a fixed temporal-logic language.

This is a targeted landscape audit, not a systematic review of every paper in every field. Its purpose is to define the nearest intellectual neighbors, establish stop rules for novelty claims, and specify baselines the project must beat or complement.

## Executive conclusion

The following ideas are **already established somewhere else and must not be advertised as the project's novelty**:

- defining a dynamical system behaviorally as a set of possible trajectories rather than by one privileged internal representation;
- asking whether a system/model is identifiable from a specified set of observations and inputs;
- treating observationally indistinguishable hypotheses as an equivalence class;
- designing inputs/interventions specifically to separate rival hypotheses;
- diagnosing which hidden fault/model generated observed behavior by active probing;
- using interventions to shrink causal equivalence classes;
- inferring candidate objectives/rewards from behavior while explicitly recognizing non-identifiability;
- asking how early or under what observations candidate goals become distinguishable;
- redesigning or actively perturbing an environment so an agent's goal becomes easier to identify;
- mining likely formal behavioral specifications directly from time-series or execution traces;
- actively querying a black-box system to infer a behavioral state machine and checking hypotheses with counterexamples/conformance tests.

The strongest remaining formulation is therefore **not** “goal discovery under an access contract.” A more defensible scientific object is:

> **Given a dynamical system, a declared observation/intervention contract, a family of candidate goal criteria, and a family of challenges, which candidate criteria and competence dimensions are identifiable from behavior, which remain equivalent, and which interventions maximally reduce that equivalence class while distinguishing active corrective competence from passive convergence or mere specification satisfaction?**

Even this should be treated as a **synthesis/benchmark hypothesis**, not a novelty verdict. The project earns distinctiveness only if the combination produces useful predictions, calibrated abstention, or cross-substrate results that the neighboring methods do not already supply.

---

## 1. Behavioral systems theory: the trajectory set is already a first-class system object

Jan C. Willems' behavioral approach defines a dynamical system by its **behavior** — the set of trajectories compatible with the system — rather than beginning with a privileged input/output partition or state-space representation. Later data-driven behavioral work makes explicit that, under suitable excitation/identifiability conditions, collected trajectories can represent the finite-time behavior of a system.

This is very close to the Dynamical Laboratory intuition that the reusable scientific object is a trajectory plus metadata and that black-box/white-box access is an analyst choice.

**Established nearby:**

- system = trajectory behavior rather than one representation;
- manifest versus latent variables;
- equivalence of different representations that generate the same behavior;
- identifiability conditions from data and input richness.

**Implication for this project:** do not claim that substrate-neutral, trajectory-first system description or “access contracts” are conceptually new. The distinctive question must concern *which goal/competence predicates on behavior are scientifically warranted*, not merely the behavioral view itself.

Key sources:

- J. C. Willems, *The Behavioural Approach to Systems and Control*, European Journal of Control 2(4), 1996.
- J. C. Willems, *The Behavioral Approach to Systems Theory*, 2005.
- I. Markovsky & F. Dörfler, *Behavioral systems theory in data-driven analysis, signal processing, and control*, Annual Reviews in Control 52 (2021), DOI `10.1016/j.arcontrol.2021.09.005`.
- J. W. Polderman & J. C. Willems, *Introduction to Mathematical Systems Theory: A Behavioral Approach*.

**Novelty pressure:** **high** on any claim that “behavior under an observation contract” is a new mathematical viewpoint.

---

## 2. Structural/practical identifiability and optimal model discrimination

System identification and mathematical biology have a large literature on whether unknown model parameters or competing model structures can be distinguished from available input-output data. When rival dynamical models fit existing observations equally well, **optimal experimental design** chooses new initial conditions, measurement times, structural changes, or external inputs that maximize predicted disagreement between the models.

This is almost exactly the generic form of “what intervention would discriminate rival explanations?”

**Established nearby:**

- structural and practical identifiability;
- observational equivalence of rival dynamical models;
- model invalidation/model discrimination;
- selecting perturbations that maximize divergence between candidate predictions;
- optimizing experiments for both parameter identifiability and model discrimination.

A particularly direct systems-biology formulation is Mélykúti et al. (2010): alternative network models fit existing data; the next experiment is chosen to maximally separate their outputs. The 2026 work of Liu, Maini & Baker explicitly combines practical parameter identifiability and model discrimination through optimal experiment design.

Key sources:

- B. Mélykúti et al., *Discriminating between rival biochemical network models: three approaches to optimal experiment design*, BMC Systems Biology 4:38 (2010), DOI `10.1186/1752-0509-4-38`.
- D. Skanda & D. Lebiedz, *An optimal experimental design approach to model discrimination in dynamic biochemical systems*, Bioinformatics 26(7), 2010, DOI `10.1093/bioinformatics/btq074`.
- L. Banga et al., *Optimally Designed Model Selection for Synthetic Biology*, ACS Synthetic Biology 9(11), 2020, DOI `10.1021/acssynbio.0c00393`.
- Y. Liu, P. K. Maini & R. E. Baker, *Optimal experiment design for practical parameter identifiability and model discrimination*, Mathematical Biosciences 399 (2026), DOI `10.1016/j.mbs.2026.109710`.

**Implication:** the project should treat “select the next intervention to discriminate hypotheses” as borrowed experimental-design machinery. Its contribution can be choosing a different hypothesis object — candidate goal criteria and competence claims — and proving that this object is meaningful across substrates.

**Novelty pressure:** **very high** on active hypothesis discrimination in general.

---

## 3. Active fault diagnosis: diagnosability by deliberate probing

Active fault diagnosis (AFD) exists precisely because nominal trajectories may contain insufficient information to distinguish hidden faults. AFD injects test inputs designed to make rival fault models produce separable output distributions or sets. Diagnosability is the corresponding question of whether the hidden status can be determined under the available observations and interventions.

This is one of the closest mature analogues to the project's Experiment 11 reporter/fault-identifiability logic.

**Established nearby:**

- passive versus active diagnosis;
- diagnosability as a property of an access/input-output regime;
- model sets whose predictions overlap under ordinary behavior;
- auxiliary inputs designed to remove that overlap;
- robust/probabilistic/set-based discrimination under uncertainty.

Key sources:

- T. A. N. Heirung & A. Mesbah, *Input design for active fault diagnosis*, Annual Reviews in Control 47 (2019), DOI `10.1016/j.arcontrol.2019.03.002`.
- S. Šimandl et al., *A Survey of Active Fault Diagnosis Methods*, IFAC-PapersOnLine 51(24), 2018, DOI `10.1016/j.ifacol.2018.09.726`.
- M. A. Sheikhi et al., *Fault Diagnosis in Dynamical Systems: Geometric Interpretation and Tractable Algorithms*, Annual Review of Control, Robotics, and Autonomous Systems (2026), DOI `10.1146/annurev-control-030123-015422`.

**Implication:** reporter failure, hidden-state faults, and intervention selection should use diagnosability/AFD vocabulary when applicable. The potentially interesting extension is that the rival hypotheses are not only faults or mechanisms but *semantic/functional criteria and competence profiles*.

**Novelty pressure:** **very high** on “active probing makes hidden explanations identifiable.”

---

## 4. Causal discovery: observational and interventional equivalence classes

Causal discovery provides another mature template. Observational data may identify a causal structure only up to a Markov equivalence class. Interventions shrink the compatible set to an interventional equivalence class, and active strategies choose intervention targets to maximize causal identifiability.

**Established nearby:**

- explicit equivalence classes as the correct output when evidence underdetermines structure;
- intervention-dependent identifiability;
- designing interventions to orient otherwise ambiguous relationships;
- formal statements of the minimal or optimal intervention set for identification under assumptions.

Key sources:

- A. Hauser & P. Bühlmann, *Two optimal strategies for active learning of causal models from interventional data*, International Journal of Approximate Reasoning 55(4), 2014, DOI `10.1016/j.ijar.2013.11.007`.
- K. Yang, A. Katcoff & C. Uhler, *Characterizing and Learning Equivalence Classes of Causal DAGs under Interventions*, ICML 2018, PMLR 80:5541-5550.
- M. J. Vowels, N. C. Camgoz & R. Bowden, *D'ya Like DAGs? A Survey on Structure Learning and Causal Discovery*, ACM Computing Surveys 55(4), DOI `10.1145/3527154`.

**Implication:** “return an equivalence class rather than force a unique answer” is excellent scientific practice but not itself novel. The project needs a principled **goal/competence equivalence relation**, ideally defined by the allowed intervention-induced trace distributions rather than by prose similarity.

**Novelty pressure:** **very high** on equivalence classes and intervention-driven identifiability in the abstract.

---

## 5. Inverse reinforcement learning: reward ambiguity is already formalized as partial identifiability

Inverse reinforcement learning (IRL) and inverse optimal control infer reward/objective information from observed behavior. Non-uniqueness is not a side issue: many reward functions can generate the same optimal or stochastic policy. Recent work explicitly formalizes **reward identifiability up to equivalence relations** and **partial identifiability**.

This is a direct prior-art warning for any claim that allowing multiple candidate goals or admitting underdetermination is new.

Important results include:

- reward functions can be identifiable only up to behavior-preserving transformations/equivalence classes;
- an observed policy can fundamentally underdetermine the reward;
- changes in environment, discount factor, prior structure, or behavioral assumptions can improve identifiability;
- model misspecification can make reward inference unsound even when an algorithm returns a precise answer.

Key sources:

- S. Kim et al., *Reward Identification in Inverse Reinforcement Learning*, ICML 2021, PMLR 139.
- H. Cao, S. Cohen & Ł. Szpruch, *Identifiability in inverse reinforcement learning*, NeurIPS 2021.
- M. L. Shehab et al., *Learning true objectives: Linear algebraic characterizations of identifiability in inverse reinforcement learning*, L4DC 2024, PMLR 242:1266-1277.
- J. Skalse & A. Abate, *Partial Identifiability and Misspecification in Inverse Reinforcement Learning*, arXiv:2411.15951 (2024).

**Difference that may still matter:** standard IRL usually assumes an agent, an MDP or related decision-process semantics, known/meaningful actions, and a behavioral model connecting reward to policy. This project intentionally wants to ask similar questions of arbitrary executable dynamical systems where “actions” and “agent” may not be supplied.

That difference is substantial **only if the method genuinely works without smuggling those assumptions back in through the candidate-goal language or analyzer**.

**Novelty pressure:** **extreme** on objective non-identifiability and reward equivalence; **moderate** on substrate-neutral extension beyond agent/MDP semantics.

---

## 6. Goal recognition and Goal Recognition Design: the nearest neighbor to active goal disambiguation

Goal recognition infers an agent's objective from observed behavior. **Goal Recognition Design (GRD)** goes further: given a domain and a set of candidate goals, it asks how much behavior can occur before the goal becomes distinguishable and how the environment can be modified so that the goal is revealed sooner.

This is uncomfortably close to the project's question “what additional observation or intervention would discriminate rival candidate goals?”

GRD work already includes:

- a set of candidate goals;
- measures of goal distinctiveness/ambiguity;
- non-optimal agents;
- partial observability and unobservable actions;
- stochastic domains;
- environment modifications designed to improve recognition;
- **active** online Goal Recognition Design, where observer interventions are interleaved with subject behavior.

Key sources:

- S. Keren, A. Gal & E. Karpas, *Goal Recognition Design*, ICAPS 2014, DOI `10.1609/icaps.v24i1.13617`.
- S. Keren, A. Gal & E. Karpas, *Goal Recognition Design for Non-Optimal Agents*, AAAI 2015, DOI `10.1609/aaai.v29i1.9645`.
- S. Keren, A. Gal & E. Karpas, *Goal Recognition Design — Survey*, IJCAI 2020, DOI `10.24963/ijcai.2020/675`.
- C. Wayllace et al., *Accounting for Observer's Partial Observability in Stochastic Goal Recognition Design*, ECAI 2020, DOI `10.3233/FAIA200370`.
- K. C. Gall, W. Ruml & S. Keren, *Active Goal Recognition Design*, IJCAI 2021, DOI `10.24963/ijcai.2021/559`.

**Implication:** the project must no longer describe “identify candidate goals, preserve ambiguity, and choose the intervention that separates them” as an untouched problem. It is already a core goal-recognition-design pattern.

**Potential distinction:** GRD normally starts with an **agent/domain theory, action semantics, and explicit candidate goals**. Our proposed setting may instead begin with an arbitrary dynamical substrate and observational variables, where the scientific task includes deciding whether a pattern criterion merits interpretation as a *goal at all*, and separately measuring the system's competence with respect to it under perturbation.

That distinction should be tested, not merely asserted.

**Novelty pressure:** **extreme** on active candidate-goal disambiguation; **moderate** on extending it to non-agent dynamical systems plus competence evidence.

---

## 7. Specification mining: probably the closest neighbor to “infer goal criteria from behavior”

This field materially changes the novelty assessment.

**Specification mining** learns likely formal system properties directly from observed executions or time series. Signal Temporal Logic (STL) and Linear Temporal Logic (LTL) mining can infer temporal properties from positive/negative traces, demonstrations, cyber-physical-system behavior, and interactions with the environment. The literature already spans:

- passive and active learning;
- model-based and model-free methods;
- supervised and unsupervised methods;
- template-based and template-free search;
- discrete traces and continuous time series;
- learning task specifications from demonstrations.

The 2022 STL survey defines specification mining as learning likely system properties from observation of system behavior and interaction with the environment. A 2025 systematic LTL review surveys thousands of papers and many methods for automatically generating temporal specifications. Work on task learning from demonstrations explicitly infers Boolean non-Markovian rewards/logical trace properties from behavior.

Key sources:

- E. Bartocci, C. Mateis, E. Nesterini & D. Nickovic, *Survey on mining signal temporal logic specifications*, Information and Computation 289 (2022), 104957, DOI `10.1016/j.ic.2022.104957`.
- D. Neider & R. Roy, *What Is Formal Verification Without Specifications? A Survey on Mining LTL Specifications*, 2025.
- S. Germiniani, D. Nicoletti & G. Pravadelli, *A Systematic Literature Review on Mining LTL Specifications*, IEEE Access (2025), DOI `10.1109/ACCESS.2025.3551607`.
- M. Vazquez-Chanlatte et al., *Learning Task Specifications from Demonstrations*, NeurIPS 2018.
- M. Baert, S. Leroux & P. Simoens, *Learning temporal task specifications from demonstrations*, EXTRAAMAS 2024.

**Why this matters:** if a “candidate goal” is represented simply as a property of successful traces — eventually reach region X, always maintain variable Y, repeatedly restore condition Z, satisfy relational pattern P — then much of Goal Discovery can collapse into **specification mining plus model selection**.

Therefore the project needs a sharper distinction between:

1. **descriptive regularity/specification:** a property that observed trajectories satisfy; and
2. **goal-relative competence:** evidence that the system *actively steers, maintains, restores, compensates, or adapts toward* a criterion under specified challenges.

A passive attractor, a hard physical constraint, and an actively regulated target may generate the same nominal specification. The project's strongest niche is therefore not merely learning the criterion but experimentally identifying the **mode and limits of competency relative to it**.

**Required baseline:** whenever a discovery experiment can be expressed in LTL/STL or another trace-property language, compare against a specification-mining baseline. If our method only rediscovers the same property less efficiently, call it an application rather than a new inference framework.

**Novelty pressure:** **extreme** on inferring behavioral properties/specifications from traces; **lower** on coupling property inference to perturbation-based competence profiling and active/passive discrimination.

---

## 8. Active automata learning and conformance testing: black-box behavior inference by queries

Active automata learning (AAL) infers state-machine models by interacting with a black-box system. Learners issue input sequences, observe outputs, propose a hypothesis machine, and use equivalence/conformance tests to search for counterexamples. Modern work covers deterministic, nondeterministic, stochastic, register, weighted and other automata, with mature tools such as LearnLib and AALpy.

**Established nearby:**

- black-box behavioral model inference by active experiments;
- explicit reset/query contracts;
- counterexample-driven refinement;
- equivalence/conformance testing;
- sample-complexity concerns when interventions are expensive;
- active learning under noise.

Key sources:

- B. K. Aichernig & M. Tappler, *Efficient Active Automata Learning via Mutation Testing*, Journal of Automated Reasoning 63, 2019, DOI `10.1007/s10817-018-9486-0`.
- E. Muškardin et al., *AALpy: an active automata learning library*, Innovations in Systems and Software Engineering 18, 2022, DOI `10.1007/s11334-022-00449-3`.
- S. Fortz et al., *A research agenda for active automata learning*, International Journal on Software Tools for Technology Transfer (2026), DOI `10.1007/s10009-026-00839-z`.

**Implication:** black-box querying and “ask for a counterexample that refutes my behavioral hypothesis” are established. AAL should become a baseline/tool when a substrate can be finitely abstracted rather than something the project reimplements.

**Novelty pressure:** **very high** on interactive black-box model learning; **low** relevance when continuous/high-dimensional biological systems resist meaningful finite abstraction.

---

## 9. Measuring goal-directedness and agency: even the higher-level predicate has formal neighbors

The programme also sits near work that tries to operationalize **goal-directedness itself**, not just infer a reward.

MacDermott et al. (NeurIPS 2024) define **maximum entropy goal-directedness (MEG)** in causal models and MDPs and allow goal-directedness to be measured relative to a known utility, a hypothesis class of utilities, or selected variables. In biology/philosophy of biology, work by Levin collaborators and others treats goal-directedness as perturbationally revealed competency in dynamical state spaces, emphasizing plasticity, persistence, equifinality, compensation, and part-whole organization. Recent critiques explicitly question whether goal attribution can ever be observer-independent.

Key sources:

- M. MacDermott et al., *Measuring Goal-Directedness*, NeurIPS 2024, DOI `10.52202/079017-0363`.
- J. Jaeger et al., *Agency, Goal-Directed Behavior, and Part-Whole Relationships in Biological Systems*, Biological Theory (2023/2024), DOI `10.1007/s13752-023-00447-z`.
- F. Heylighen, *The meaning and origin of goal-directedness: a dynamical systems perspective*, Biological Journal of the Linnean Society 139(4), 2023.
- N. Rajcic & A. Søgaard, *Goal-Directedness is in the Eye of the Beholder*, 2025 preprint.

**Implication:** “measure goal-directedness from perturbational behavior” is not an empty field. The project needs to be explicit that it is not proposing a universal agency score. Its better contribution is a **claim-auditing protocol**: given a candidate criterion and challenge family, what dimensions of competence are supported and at what resolution?

**Novelty pressure:** **high** on generic goal-directedness measurement; **lower** on calibrated multidimensional competence claims for unconventional dynamical substrates.

---

## 10. Synthesis: what is and is not left

### Claims to stop making

The project should **not** claim novelty for any of the following by itself:

| Claim | Established neighboring field |
|---|---|
| A system can be characterized by trajectories rather than one internal model | Behavioral systems theory |
| Some hidden properties are not identifiable from available outputs | System identification / observability / identifiability |
| Multiple hypotheses should survive when behavior cannot distinguish them | Statistical/causal/IRL equivalence classes |
| Interventions can make hidden hypotheses distinguishable | Optimal experiment design / AFD / causal discovery |
| The next experiment can be chosen to maximize discrimination | Model discrimination / AFD / active causal learning |
| Rewards/goals can be non-identifiable from behavior | IRL / goal recognition |
| Candidate goals can be ranked from observed actions | Goal recognition |
| An environment can be modified to reveal goals sooner | Goal Recognition Design |
| Likely temporal/system properties can be inferred from traces | Specification mining |
| Black-box dynamics can be inferred by active queries and counterexamples | Active automata learning |
| Goal-directedness can be operationalized in causal/dynamical models | Goal-directedness/agency literature |

### What may still be a useful contribution

No surveyed field by itself appears to exactly package all of the following as one experimental programme:

1. **arbitrary dynamical substrates**, including developmental, regenerative and biological systems without a presupposed agent/action ontology;
2. **candidate goal criteria that may be relational/equivalence-class properties**, not only reward functions or terminal states;
3. a **challenge-relative competence vector** separating attainment, maintenance, recovery, robustness, efficiency, adaptation, flexibility and transfer rather than one scalar agency score;
4. interventions specifically designed to distinguish **active corrective steering** from passive convergence, physical constraint, or merely satisfying a mined specification;
5. a declared **observation/intervention contract** that is varied experimentally and used to state identifiability limits;
6. output as a **calibrated equivalence class/abstention**, not forced semantic labeling;
7. the **same independently authored system** used first as a white-box causal oracle and then as a deliberately blinded inference benchmark;
8. transfer tests across systems not authored to validate the decomposition.

This combination is **potentially distinctive**, but the survey does not establish novelty. It may be best understood as a *benchmarking and synthesis contribution* rather than a new foundational theory.

---

## 11. A stricter problem definition for the project

To keep the discovery arm scientifically separate from nearby fields, define each benchmark explicitly:

### System

An executable or observed dynamical system producing trajectories over state space. No agent interpretation is required.

### Observation contract `O`

What variables, resolution, sampling times, history, interventions and metadata the analyst may observe.

### Intervention family `I`

Allowed perturbations: state edits, parameter changes, structural lesions, input signals, sensor/action restrictions, environment changes, resets, etc.

### Candidate criterion family `G`

A finite or generative family of possible goal-relative criteria. Criteria may be terminal, relational, temporal, distributional, equivalence-class or maintenance properties.

### Challenge family `C`

Perturbations/environments relative to which competence is evaluated. A claim of competence without a challenge family is underspecified.

### Competence profile `K(g, C)`

A vector of measured dimensions such as attainment, maintenance, recovery, reliability, efficiency, robustness, adaptation, flexibility and transfer. Do not collapse this to one scalar unless a concrete experiment needs one.

### Behavioral equivalence under a contract

Two candidate criteria `g1` and `g2` are equivalent for the current benchmark when the permitted observations/interventions do not produce evidence that discriminates their associated competence predictions at the declared resolution. The exact mathematical relation should be experiment-specific until a general definition earns its keep.

### Active discrimination

Given surviving candidate criteria/competence hypotheses, choose an allowed intervention that is predicted to maximally separate them. This should reuse optimal-design/AFD/GRD machinery where appropriate rather than inventing an inferior bespoke optimizer.

### Output

The analyst should return:

- supported criteria/competence claims;
- contradicted claims;
- the surviving equivalence class;
- confidence/uncertainty at the resolution justified by evidence;
- the next intervention most likely to discriminate surviving rivals;
- explicit refusal to infer semantic mechanism or “true goal” where the evidence does not warrant it.

---

## 12. The critical distinction: specification satisfaction versus competence

This is the most promising conceptual separator from specification mining.

Suppose all observed trajectories eventually satisfy `x = x*`. That is compatible with at least several explanations:

1. passive physical relaxation to an attractor;
2. active feedback regulation around `x*`;
3. a one-shot controller that reaches `x*` and then stops;
4. a hard constraint that prevents alternative states;
5. a developmental process that reaches `x*` only from a narrow initial-condition basin;
6. an adaptive system that can restore `x*` using alternative actions after perturbation.

A temporal specification such as “eventually `x*`” describes all six. A competence claim should discriminate them using challenge/intervention evidence.

Therefore a discovery benchmark should have **two layers**:

- **criterion inference:** what trace property/goal criterion is compatible with behavior? Use specification-mining/goal-recognition baselines.
- **competence inference:** what evidence shows attainment, active maintenance, recovery, compensation, adaptation, etc. relative to that criterion? Use perturbations, matched controls and failure-boundary mapping.

If the project can make this distinction operational and transferable, it has a clearer contribution than “goal inference” alone.

---

## 13. Required baselines and reuse policy

For every future discovery benchmark, first ask which mature method already fits the access assumptions.

| Benchmark structure | Baseline/reuse candidate |
|---|---|
| Candidate temporal/relational criteria over traces | STL/LTL specification mining |
| Agent + domain model + candidate goals | Goal recognition / Goal Recognition Design |
| MDP + action semantics + reward hypotheses | IRL identifiability methods |
| Rival mechanistic dynamical models | optimal experiment design / model discrimination |
| Fault-mode hypotheses | active fault diagnosis |
| Causal graph hypotheses | interventional causal discovery |
| Finite black-box input/output abstraction | AALpy / LearnLib active automata learning |
| White-box regulatory reachability | Cellnition / RNM / control-theoretic analysis |

**Stop rule:** when an existing method exactly answers the benchmark under its native assumptions, use it and classify our work as an application/comparison unless the competence layer adds demonstrably new information.

---

## 14. Concrete benchmark programme

### Benchmark A — Growing NCA

Keep the current white-box lesion/latent-state/action-reachability work. Add an explicitly blinded inference layer only after the causal map is stronger.

Candidate criterion families should include competing descriptions at different resolutions, for example visible target similarity, persistent morphology class, relational/geometric features, viability-like occupancy criteria, and weaker maintenance properties. The point is not to guess the author's training loss; it is to identify which descriptions are behaviorally warranted under selected interventions.

Compare:

- passive trace/specification inference;
- perturbation-based competence profiling;
- active selection of the next lesion/state/action intervention.

### Benchmark B — Cellnition / Regulatory Network Machine

Use RNM as a strong comparator because white-box reachability, path dependence and target-state control are already formalized. Blind the semantic labels and ask whether Goal/Competence Identification recovers anything scientifically distinct from standard reachability/model-discrimination analysis.

**Failure condition:** if the blind framework simply reconstructs the RNM state graph less efficiently, reduce the discovery claim.

### Benchmark C — MinimalDevelopmentalComputation

This is a high-value external regenerative system with local controllers, dynamic tissue structure and published developmental interpretation. Pre-register candidate competence predictions, then compare white-box mechanism results against a blinded analyst.

### Benchmark D — specification-mining stress test

Construct a benchmark where ordinary trajectories make passive and active systems satisfy the same LTL/STL criterion. Then add delayed or structured perturbations that separate them. This directly tests whether the proposed competence layer adds information beyond mined specification satisfaction.

### Benchmark E — agent-native comparator

On a small planning/MDP system where GRD or IRL applies cleanly, compare our generalized machinery against the native method. We should expect the specialized method to win on efficiency. The purpose is to verify that our outputs reduce to established answers when their assumptions hold.

### Benchmark F — biological intervention corpus

Only after the method survives synthetic/executable comparisons, move to Planform/Limbform or another real perturbation corpus. Here the primary scientific value is calibrated limits: which goal/competence descriptions are actually discriminated by the historical interventions, and what new experiment would be maximally informative?

---

## 15. Updated novelty assessment

| Proposed project element | Assessment after this audit |
|---|---|
| Trajectory-first, representation-neutral system view | **Established** — behavioral systems theory |
| Declared observation/intervention access contract | **Established in spirit** across identification/testing/diagnosis; project-specific packaging only |
| Explicit underdetermination/equivalence classes | **Established** across causal inference, IRL, identification |
| Active intervention to distinguish rival explanations | **Established** — OED/AFD/causal learning |
| Candidate-goal inference from behavior | **Established** — goal recognition/IRL |
| Active design to reveal candidate goals | **Established** — Goal Recognition Design |
| Mining candidate temporal/system criteria from traces | **Established** — specification mining |
| Black-box active behavioral inference | **Established** — automata learning |
| Universal measure of goal-directedness | **Occupied and philosophically contested** |
| Competence as multidimensional and challenge-relative rather than scalar | **Plausible synthesis; needs sharper comparison** |
| Distinguishing specification satisfaction from active maintenance/recovery across arbitrary substrates | **Potentially distinctive benchmark question** |
| Joint candidate-criterion + competence-profile identifiability for arbitrary dynamical systems without agent/MDP assumptions | **Potentially distinctive; not established as novel** |
| White-box oracle + deliberately blinded analyst on the same independent developmental systems | **Potentially distinctive methodology; must demonstrate added value** |
| Cross-substrate predictive transfer of intervention-defined competence constraints | **Potentially strongest contribution if successful** |

---

## 16. Strategic recommendation

The discovery arm should be framed less as inventing a new inverse-problem concept and more as **integrating and stress-testing established identification ideas on a different scientific target**.

A suitable internal name is still “Goal and Competence Discovery,” but in external scientific writing the safer phrase is **goal/competence identification under interventions** until novelty is demonstrated.

The project should now optimize for three outputs:

1. **Predictive transfer:** a capability distinction predicts a non-obvious boundary shift in an independently authored system.
2. **Incremental inference value:** perturbation-based competence profiling distinguishes systems that specification mining/nominal goal recognition would treat similarly.
3. **Calibration:** the blinded analyst returns the right equivalence class and abstains at the right time, including identifying the intervention needed to refine the claim.

If those three outputs are achieved across several external systems, the project has a coherent contribution even if every mathematical ingredient has prior art. If they are not, the right conclusion is to narrow the programme rather than introduce new vocabulary.

## Primary-source links

- Behavioral systems theory/data-driven behavior: `https://www.sciencedirect.com/science/article/pii/S1367578821000754`
- Active fault diagnosis review: `https://www.sciencedirect.com/science/article/pii/S1367578819300070`
- 2026 fault-diagnosis review: `https://www.annualreviews.org/content/journals/10.1146/annurev-control-030123-015422`
- Causal DAG equivalence under intervention: `https://proceedings.mlr.press/v80/yang18a.html`
- IRL identifiability, NeurIPS 2021: `https://papers.nips.cc/paper/2021/hash/671f0311e2754fcdd37f70a8550379bc-Abstract.html`
- IRL identifiability, L4DC 2024: `https://proceedings.mlr.press/v242/shehab24a.html`
- Goal Recognition Design survey: `https://www.ijcai.org/proceedings/2020/675`
- Active Goal Recognition Design: `https://www.ijcai.org/proceedings/2021/559`
- STL specification-mining survey: `https://www.sciencedirect.com/science/article/pii/S0890540122001122`
- Learning task specifications from demonstrations: `https://papers.neurips.cc/paper_files/paper/2018/hash/74934548253bcab8490ebd74afed7031-Abstract.html`
- 2026 active automata-learning agenda: `https://link.springer.com/article/10.1007/s10009-026-00839-z`
- AALpy: `https://link.springer.com/article/10.1007/s11334-022-00449-3`
- Measuring Goal-Directedness, NeurIPS 2024: `https://proceedings.neurips.cc/paper_files/paper/2024/hash/1551c01d7a3d0bf21e2518331e9f7074-Abstract-Conference.html`
