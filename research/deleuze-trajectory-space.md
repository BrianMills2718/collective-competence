# Constraint-induced trajectory space: theoretical notes from Deleuze, Levin, Hoel, control theory, and the Collective Competence programme

> **Status:** exploratory research note, not a canonical project claim.
>
> **Provenance:** this document records and sharpens a long-form conceptual discussion prompted by a reading of Gilles Deleuze's "Postscript on the Societies of Control." It preserves both the useful connections and the objections that substantially changed the interpretation.
>
> **Evidence rule:** nothing in this file overrides native experiment records, code, result packages, the hot wiki, or the project's novelty audits. Where this note maps philosophical vocabulary onto project concepts, the mapping is heuristic unless a project experiment already operationalizes it.
>
> **Terminology rule:** do not import Deleuzian vocabulary into the project ontology merely because an analogy is suggestive. Where control theory, reachability analysis, causal inference, dynamical-systems language, information theory, or the Levin/TAME literature already supplies a clearer technical term, prefer the established technical term in experiments. Philosophical vocabulary is useful here chiefly as a hypothesis generator and model-construction heuristic.

## 1. Why this discussion is relevant to the repository

The conversation began with a political-philosophical taxonomy—sovereignty, discipline, and control—but moved toward a much more precise question:

> **What causal structures shape the distribution of future trajectories available to a system, at what scale should those structures be represented, and how should interventions on them be evaluated?**

That question is already close to the repository's actual scientific programme.

The repository asks which experimentally separable constraints determine goal-relative competence and failure boundaries, and which goal/competence claims are identifiable under a declared observation/intervention contract. It already treats:

- system boundary and scale as declared modeling choices;
- problem space as representation-dependent coordinates in which a system can attain, maintain, or recover a criterion;
- competence as challenge-relative rather than a single universal scalar;
- reachability, action repertoire, information access, path dependence, recovery, robustness, compensation, adaptation, and identifiability as distinct;
- externally authored systems, prospective predictions, matched interventions, and negative results as preferred evidence;
- coarse-graining and effective information as empirical questions rather than assumptions.

The strongest connection is therefore not "Deleuze explains collective competence." It is:

> **Deleuzian language about territories, striation, modulation, and lines of flight can sometimes be translated into precise questions about constraint-induced topology of trajectory space.**

The repository is unusually well positioned to test whether that translation is scientifically useful because it already contains exact reachability results, opportunity-versus-realization experiments, path-dependent recovery, multiscale boundary metadata, causal-emergence measurements, and a planned Regulatory Network Machine comparator.

---

## 2. Trajectory of the discussion

The conceptual trajectory matters because several initial formulations were rejected or substantially repaired.

### 2.1 Starting point: societies of sovereignty, discipline, and control

The initial source distinguished roughly:

- **sovereignty**: obedience backed by punishment or death;
- **discipline**: enclosure, schedules, surveillance, bodily normalization;
- **control**: data, automation, continuous classification, and access modulation.

The first objection was that these categories looked too loose to be literal partitions. Killing is obviously an extreme form of bodily control. Schools have always classified people. Credit, reputation, and distributed informational judgments predate digital computation. A prison, a grading rule, and a credit algorithm are all "control" in an ordinary causal sense.

The useful repair was to interpret these not as mutually exclusive historical species, but as **idealized modalities of constraint**:

- sovereign mechanisms characteristically seize, forbid, or punish;
- disciplinary mechanisms characteristically impose comparatively stable norms within bounded institutions;
- control mechanisms characteristically update access or constraints as a function of changing signals.

This is still scale- and model-dependent, but it is much less brittle.

### 2.2 "Machine" looked suspiciously universal

The source used "machine" much more broadly than ordinary physical machinery: a machine was described as a process connected to flows, interrupting or transforming them, and producing further flows.

That raised an immediate problem:

> If every process that transforms flows is a machine, what is not a machine?

The productive reconstruction was:

> **A Deleuzian machine can be treated as a selected process-level coarse-graining of a physical system, chosen because it exposes some transformation relevant to the analysis.**

On this reconstruction:

- machine is not ontologically opposed to object;
- the same physical realization can be an object at one descriptive level and a machine/process at another;
- humans can be represented as collections of interacting processes without implying that ordinary object boundaries are unreal;
- there need not be one primitive "machine" substance beneath everything.

For project purposes this suggests a model-selection heuristic rather than a metaphysical commitment:

> Do not assume ordinary object boundaries are the causally useful boundaries.

This fits the repository's existing requirement to declare focal boundary and scale.

### 2.3 Assemblages and the problem of "temporary"

An assemblage was initially glossed as a temporary organization of heterogeneous components. The objection was decisive: everything physical is temporary under a sufficiently long timescale, so "temporary" is meaningless without a reference scale.

The repaired notion is:

> **An assemblage is an organization whose coherence is relative to a specified timescale, representation, and intervention family.**

The useful distinction is not permanent versus temporary. It is whether a pattern is sufficiently invariant or causally coherent at the scale relevant to the question.

This is directly compatible with the repository's insistence that challenge families, boundaries, representations, and transfer limits be declared.

### 2.4 Enclosure became coarse-grained causal organization

The Foucauldian image of enclosure is spatial: prison, hospital, barracks, school.

The discussion generalized this:

> A physically enclosed region is one possible coarse-graining, but a useful macroscopic boundary can also be temporal, informational, relational, or dynamical.

A human, tissue, firm, or collective may be more usefully modeled as a **dynamically enclosed** system than as whatever is inside an instantaneous spatial boundary.

A candidate operational direction is:

> find a boundary such that variables inside it form an unusually effective causal or controller unit relative to variables outside it.

This should not be assumed. It is an empirical/model-selection question.

### 2.5 Agency language weakened once libertarian free will was rejected

The source often framed control as erosion of autonomous individual agency. That formulation is weak if one already rejects libertarian free will.

The better question is not:

> Is Alice metaphysically free?

It is:

> **Which variables have causal leverage over Alice's future trajectories, and how does an institutional or biological architecture change that leverage?**

For a dynamical system this becomes a question about transition rules, reachable sets, intervention effects, and controllability rather than metaphysical authorship.

This maps well onto the repository, which already avoids claiming agency from successful behavior alone.

### 2.6 "Dividual" had to become a spectrum

The source treated modern subjects as "dividuals": persons decomposed into data fragments such as credit scores, risk factors, watch history, and test scores.

The objection was that humans have always been decomposable into attributes. A person could be rich, indebted, ugly, aristocratic, criminal, reputable, or heretical long before databases.

The stronger version is scalar:

> **Dividualization is the degree to which components of a representation can circulate, recombine, and trigger effects independently of the rest of the represented person/system.**

Modern infrastructure changes the speed, portability, automatic actionability, and cross-context recombination of attributes. It does not invent divisibility.

This is potentially relevant to the repository's representation contracts, but it is not currently a central experimental lane.

### 2.7 Mold versus modulation became state-dependent constraint updating

The original "mold versus modulation" language sounded unrelated when defined carelessly.

A better parallel definition is:

- **mold**: a constraint whose parameters remain approximately fixed while cases pass through it;
- **modulation**: a constraint whose parameters update as cases pass through it.

For example:

- mold: pass if score >= 70;
- modulation: pass if score >= previous_score + 5.

Or, more generally:


theta_(t+1) = f(theta_t, x_t, population_state, resource_state)


where the constraint parameter (theta) itself evolves.

The objection remains that "approximately fixed" is scale-dependent. A rule fixed within an exam but changed every semester is a mold at one temporal resolution and modulation at another. Therefore the distinction is model-relative, not ontologically absolute.

For this repository, the corresponding technical vocabulary would usually be fixed versus adaptive/state-dependent control or changing transition structure.

### 2.8 The major turn: trajectory space

The discussion became substantially more useful when "control" was reformulated in terms of **trajectory space**.

Let:

- (s_t) be a system state;
- (A(s_t)) be available actions/interventions;
- (tau=(s_0,s_1,ldots)) be a trajectory;
- (C) be the constraint architecture;
- (P(tau |  C,pi)) be the trajectory distribution under policy/dynamics (pi).

Then a mechanism of control need not choose one future. It can alter:

- which trajectories are reachable;
- their transition costs;
- their probabilities;
- the redundancy of routes to the same goal;
- the sensitivity of outcomes to interventions;
- the robustness of trajectories under perturbation.

This gave a precise form to the earlier intuition that institutions or collective mechanisms create "ruts" in possibility space.

### 2.9 Territorialization, striation, and lines of flight

The discussion then connected the "ruts" intuition to Deleuze and Guattari's vocabulary:

- **territorialization**: stabilization or organization of a pattern of relations;
- **deterritorialization**: loosening or escaping that organization;
- **reterritorialization**: stabilization into a new organization;
- **striated space**: space organized into channels, partitions, metrics, or privileged trajectories;
- **smooth space**: comparatively less pre-channelled organization;
- **line of flight**: a trajectory that escapes or transforms an existing organization.

For scientific use in this repository, "striation" has the cleanest possible translation:

> **Constraint-induced anisotropy of trajectory space**: some state transitions/routes become easier, more probable, more robust, or possible at all, while others become difficult, fragile, improbable, or unreachable.

"Anisotropy" here means direction dependence: movement through state space is easier in some directions than others.

A "line of flight" can then be treated heuristically as a route that becomes newly reachable or realizable after a transformation of the constraint architecture. It should not replace standard reachability or control terminology in experiments.

### 2.10 Liberation was separated from welfare

At one point "liberation" was approximated as widening the distribution of possible trajectories. That immediately produced a problem.

A broader distribution can be worse:

- more catastrophic trajectories may become available;
- probability mass can spread away from good outcomes;
- increased optionality can reduce reliability.

At least three concepts must be distinguished:

1. **support size**: how many trajectories have nonzero probability;
2. **entropy**: how spread out the probability distribution is;
3. **controllability**: how effectively interventions can shift the system among reachable states.

None is intrinsically equivalent to welfare.

This matters because a simple "minimize control" or "maximize lines of flight" norm is indefensible. Biological regulation, traffic control, error correction, and morphogenesis are all forms of constraint/control that may be instrumentally beneficial.

### 2.11 Utilitarianism and the descriptive/normative split

A serious consequentialist analysis already cares about causal structure, uncertainty, path dependence, option value, tail risk, and intervention costs.

The clean division of labor is therefore:

- causal/dynamical analysis describes how architectures shape trajectories;
- normative theory supplies the evaluation criterion.

A simple form is:


maximize over pi: E[U(tau) | pi]


and the realistic version must include uncertainty over the causal model (M):


maximize over pi: E_(M,tau)[U(tau) | pi, M]


Therefore Deleuzian analysis is not a rival objective function. At best it is a descriptive heuristic for identifying causal architecture that a consequentialist would then evaluate.

This repository is appropriately mostly non-normative: it studies reachability, competence, recovery, identifiability, and mechanism rather than supplying (U).

---

## 3. Definitions and working translations

This section records the definitions that survived the dialogue strongly enough to be potentially useful.

### 3.1 Posthumanism

A useful broad definition for this discussion:

> **Posthumanism** comprises approaches that reject the autonomous, self-contained human individual as the uniquely privileged or sufficient unit of explanation.

This is a broad family resemblance, not the only standard definition. Different posthumanisms emphasize different things: technology, embodiment, ecology, distributed cognition, anti-humanism, nonhuman agency, or critiques of human exceptionalism.

The relevant point for this project is only the methodological one:

> do not assume that the skin-bounded individual is always the correct causal grain.

That claim is compatible with multiscale analysis without requiring any stronger posthumanist thesis.

### 3.2 Machine

For the purposes of this discussion:

> **Machine** = a process-level description of an arrangement that receives/participates in flows, transforms or interrupts them, and produces further flows.

Important constraints:

- machine is not synonymous with physical artifact;
- machine is not metaphysically opposed to object;
- machine descriptions depend on selected inputs, outputs, and transformation boundaries;
- if "machine" is used so broadly that everything qualifies, its value is heuristic rather than classificatory.

Repository translation: mechanism, transition structure, controller, process, or causal organization—whichever established term actually fits.

### 3.3 Assemblage

Working reconstruction:

> **Assemblage** = a scale-relative organization of heterogeneous components whose interactions jointly matter for some behavior, without assuming an eternal or metaphysically privileged unity.

Repository translation: focal system plus components/couplings, with declared boundary, scale, representation, and challenge family.

### 3.4 Enclosure

Original image: physically bounded institution.

Generalized reconstruction:

> **Enclosure** = a comparatively stable coarse-grained boundary within which selected variables are monitored, coupled, normalized, or controlled.

Possible boundary types:

- spatial;
- temporal;
- informational;
- organizational;
- dynamical;
- causal.

Potential research extension: infer rather than stipulate useful boundaries.

### 3.5 Dividual

Working reconstruction:

> **Dividualization** = the degree to which a system/person is represented as separable variables that can circulate and exert causal effects independently.

This should be treated as continuous, not binary.

### 3.6 Mold

> **Mold** = a constraint whose defining parameters are comparatively stable at the analysis timescale while instances pass through it.

### 3.7 Modulation

> **Modulation** = a constraint whose defining parameters update as a function of system state, incoming cases, feedback, or time.

Repository translation: adaptive/state-dependent transition rule or controller, if that is what is actually meant.

### 3.8 Cybernetics

In the discussion:

> **Cybernetics** = study of control and communication through feedback, especially systems that compare actual behavior/state against a pattern/criterion and use the discrepancy to alter later behavior.

The thermostat example remains useful:


measured temperature -> error relative to setpoint -> heating action -> new temperature


Repository caution: passive attraction to an equilibrium, active feedback, compensation, and adaptation must remain separate claims.

### 3.9 Territorialization

Working translation:

> **Territorialization** = stabilization of a region, relation, organization, or recurring pattern in trajectory space.

Do not equate territorialization with competent regulation. A passive attractor can stabilize a region without sensing, correction, compensation, or adaptation.

### 3.10 Striation

Working translation:

> **Striation** = structured anisotropy imposed on a problem/state space, creating privileged, costly, fragile, forbidden, or effectively inaccessible routes.

This is the most directly operationalizable Deleuzian concept for the current repository.

### 3.11 Line of flight

Working translation:

> **Line of flight** = a trajectory that exits or transforms an existing organization of constraints.

Possible formal proxy:


tau is not in R_C(s), but tau is in R_C'(s)


where changing the constraint architecture from (C) to (C') makes the route reachable.

This is a heuristic mapping only. In experiments use standard reachability/action-space language unless Deleuzian terminology adds a testable distinction.

---

## 4. The strongest formal synthesis: constraint-induced topology of competence

The most promising concept emerging from the discussion is:

> **constraint-induced topology of competence**

This asks how constraints alter the structure of possible and actually realized trajectories relative to a goal criterion and challenge family.

Let:

- (S) = state space;
- (sin S) = current state;
- (C) = constraint architecture;
- (A_C(s)) = actions/transitions admissible under (C);
- (G is a subset of S) or (G(tau)) = goal criterion;
- (pi) = native policy/dynamics;
- (D) = challenge family.

Then several quantities should remain separate.

### 4.1 State-space existence

A goal state exists in the modeled state space:


G intersects S is non-empty


This says almost nothing about competence.

### 4.2 Reachability or opportunity

Define the reachable set:


R_C(s) = {s' such that an admissible path from s to s' exists under C}


Criterion reachability is:


G intersects R_C(s) is non-empty


This is opportunity, not realized competence.

### 4.3 Route cost

Define:


d_C(s, G)


as the minimum cost of a route from (s) to any state satisfying (G), under a declared cost model.

The cost could be:

- number of transitions;
- energy/resource use;
- time;
- intervention magnitude;
- damage;
- information requirement.

### 4.4 Route multiplicity/redundancy

Let:


N_C(s, G)


represent the number or diversity of substantively distinct routes to (G).

High route redundancy can support robustness even if the shortest route is unchanged.

This resembles the repository's distinction between having an available route and robustly realizing one across schedules/challenges.

### 4.5 Native realization


P_pi(G | s, C)


asks whether the system's own dynamics exploit reachable opportunities.

This is closer to competence than bare reachability.

### 4.6 Robust realization

Under a challenge family (D):


P_pi(G | s, C, D)


This is where recovery, robustness, flexibility, adaptation, and other profile dimensions become relevant.

### 4.7 Path dependence / hysteresis

Two trajectories can arrive at states that are equivalent under a chosen representation while retaining different futures because of hidden/history-dependent state.

Formally, for histories (H_1,H_2):


P(tau after t | x_t, H1) != P(tau after t | x_t, H2)


even when the chosen observed macrostate (x_t) is the same.

This exposes whether the representation is Markov-sufficient for the question. If not, apparent "ruts" may live in omitted state variables.

### 4.8 Striation as a vector of changes, not one scalar

A constraint change (C ->  C') can alter:

- (|R_C(s)|): reachable-set size;
- (d_C(s,G)): minimum route cost;
- (N_C(s,G)): route multiplicity;
- transition probabilities;
- robustness across (D);
- policy realization probability;
- sensitivity to initial conditions;
- reversibility/irreversibility;
- basin geometry;
- history dependence.

Therefore "more striated" should not be promoted as a single project metric without a specific experiment. It is better treated as a family of structural changes.

---

## 5. Mapping to existing repository evidence

### 5.1 P2-003 is a literal reachability partition

Relevant file:

- ../goal-discovery/docs/hypotheses/p2_003_barrier_reachability_results.md

In the adjacent-swap sorting system, immovable cells create an exact reachability boundary. The frozen barrier-feasibility rule classified all 7,440 tested size-5 immovable cases correctly.

This is an unusually clean example of constraint-induced topology:

- the target may exist;
- the agents may retain local rules;
- but the constraint partitions state space so required crossings are impossible.

In the present note's language, the barrier creates an extreme striation: some routes are deleted from the admissible transition graph.

The scientific description should remain "reachability invariant" rather than "striation" in the experiment itself.

### 5.2 P2-004 shows different constraints preserve different invariants

Relevant file:

- ../goal-discovery/docs/hypotheses/p2_004_moveable_order_reachability_results.md

Moveable passive cells do not create the same spatial partition. They can be moved by active neighbors, but two passive identities cannot cross one another. Their relative order is invariant.

The rule correctly classified all 90,720 tested new size-6 branches.

This is important because it demonstrates:

> "damage" is not a sufficient causal descriptor.

Different constraint types reshape trajectory space differently.

That is exactly the kind of result a constraint-topology programme should retain.

### 5.3 P2-005 supplies the key opportunity/realization decomposition

Relevant files:

- ../goal-discovery/docs/hypotheses/p2_005_opportunity_adjusted_performance.md
- ../goal-discovery/docs/hypotheses/p2_005_opportunity_adjusted_performance_results.md

This experiment separates:

1. unreachable;
2. reachable but unrealized;
3. reachable and robustly realized.

That distinction should be central to any future attempt to connect "possibility space" to competence.

A negative outcome on an unreachable branch is not the same scientific fact as a negative outcome where a valid route exists but the policy fails to exploit it.

The result also found that the sorting algotypes differed more strongly in opportunity than in conditional realization: once a route existed, several policies were already near ceiling.

This directly warns against collapsing state-space geometry and policy competence into one number.

### 5.4 Experiments 06–11 already manipulate reachable state space through action repertoire

Relevant synthesis:

- ../wiki/findings.md

One durable result is:

> perfect target information is insufficient if the available actions cannot create the missing lineage.

Adding daughter-fate plasticity changes the reachable state space.

This is a clean example of an intervention changing opportunity rather than simply changing prediction or sensing.

Similarly, the regeneration experiments separate:

- desired-state information;
- current-state information;
- reporter integrity;
- memory;
- structural position;
- generative action repertoire.

These are different ways a trajectory can be constrained.

### 5.5 Experiment 12 supplies multidimensional failure boundaries

Relevant file:

- ../experiments/12-growing-nca/README.md

The Growing NCA work is especially relevant because it shows that one-dimensional severity proxies repeatedly fail.

Recovery depends on experimentally separable factors including:

- amount of damage;
- geometry/orientation;
- location/local support;
- developmental timing/state;
- latent-state spatial compatibility;
- timely action availability.

The important lesson for the present theoretical frame is:

> **competence boundaries are surfaces in a multidimensional constraint/challenge space, not necessarily thresholds on one scalar damage variable.**

This is much closer to a useful "landscape" concept than generic talk about control.

### 5.6 Experiment 12 A1 is the strongest existing "rut" / hysteresis analogue

Relevant files:

- ../experiments/12-growing-nca/action_gate_probe.py
- ../experiments/12-growing-nca/test_action_gate.py
- ../experiments/12-growing-nca/README.md

A1 starts all damaged branches from the same radius-16 lesion and temporarily blocks updates inside the lesion footprint for 0, 16, 32, or 64 recovery steps.

Important facts:

- every nonzero blackout is worse than normal damaged recovery in every tested future stream at the primary horizon;
- 64-step blackout is clearly the most damaging regime;
- the strict monotonic dose prediction is mixed because 16 and 32 steps do not order consistently;
- after actions are restored, the 32- and 64-step branches do not catch up over the tested 256-step horizon;
- their divergence from normal damaged recovery increases on average.

The repository correctly calls this evidence of **path dependence over the tested horizon**, not proof of formal unreachability.

This result gives a concrete form to the "ruts" intuition:

> a temporary constraint at an earlier time changes the distribution of later trajectories even after that constraint is removed.

The remaining question is whether the apparent history dependence can be represented as ordinary Markov dynamics in a richer hidden state. Usually it can. "Hysteresis" here describes dependence relative to a chosen observed representation, not metaphysical memory outside state.

### 5.7 Q1-009 already directly tests the Hoel connection

Relevant files:

- ../goal-discovery/docs/hypotheses/q1_009_information_measures.md
- ../goal-discovery/docs/hypotheses/q1_009_information_measures_results.md
- ../goal-discovery/src/experiments/q1_information/measures.py
- ../goal-discovery/tests/test_information_measures.py

Q1-009 implemented:

- interventional effective information;
- macro/micro coarse-graining;
- causal emergence as (EI_{macro}-EI_{micro});
- matched finite-sample nulls;
- an interventional empowerment estimator.

This is important for the present discussion because the result is not a philosophical endorsement of coarse-grained emergence.

For the chosen partitions, the macro description carried **less** effective information than the micro description in the non-degenerate arms. The result explicitly notes that only one coarse-graining was tested and the partition was not searched.

Therefore the project already has a direct negative result against the easy claim:

> "The obvious collective macrostate must be causally privileged."

Any boundary-discovery extension should take this seriously.

### 5.8 Q1-009 also warns against calling a scalar "agency"

The empowerment measure initially looked like a promising goal-free agency quantity. After correcting defects and widening the intervention, its ordering tracked unused unilateral capacity/idleness rather than the intended collective agency interpretation.

This is a strong methodological lesson:

> a mathematically respectable measure does not inherit the semantic label we want to give it.

The causal question is what interventions actually make the measure move.

This aligns with the dialogue's skepticism about treating "agency" as a metaphysical primitive.

### 5.9 The focal-boundary metadata is already compatible with dynamic enclosure

Relevant files:

- ../wiki/concepts.md
- ../wiki/ontology.md

The repository already states that:

- a focal system is whatever collection the experiment treats as the system of interest;
- the same physical component can lie inside one experiment's boundary and outside another's;
- boundary and scale must be declared when they affect attribution;
- experiment declarations include focal boundary, scale, attribution level, and rationale.

This already rejects spatial enclosure as the sole legitimate boundary.

The missing piece is **boundary discovery**: deciding from intervention data which boundary/coarse-graining is most useful rather than merely declaring one.

### 5.10 Issue #75/RNM is the obvious established comparator

Relevant issue:

- https://github.com/BrianMills2718/collective-competence/issues/75

The planned Regulatory Network Machine / Cellnition comparator already formalizes:

- stable states;
- intervention-induced transitions;
- path dependence;
- cycles;
- unreachable states;
- routes to desired states.

This substantially occupies the generic "trajectory ruts" / reachability territory.

Therefore any new project contribution should not be:

> "constraints shape future possibilities."

That is established.

A stronger question is whether the project's competence layer, challenge-relative measurements, restricted-access identifiability, or boundary/representation selection adds something demonstrable beyond native RNM/control analysis.

---

## 6. The most promising new lane: boundary discovery

The most substantively new connection from the discussion is not Deleuzian terminology. It is the question:

> **Can the project discover, rather than merely stipulate, the boundary/coarse-graining at which competence is most causally or predictively coherent?**

This directly joins:

- the repository's focal-boundary metadata;
- Hoel-style causal emergence;
- Levin/TAME multiscale competency;
- the dialogue's "dynamic enclosure" idea;
- the project's problem-space/representation discipline.

### 6.1 Why the question is nontrivial

A skin boundary, anatomical region, subsystem, or agent grouping may be intuitive but causally poor.

Conversely, a nonlocal set of variables may form a better intervention-predictive macrostate.

However, "best" needs a declared objective. Candidate criteria include:

- **predictive sufficiency**: the macrostate retains relevant predictions of future outcomes;
- **interventional sufficiency**: it preserves the effects of allowed interventions;
- **compression**: it discards microdetail while retaining relevant causal structure;
- **cross-challenge stability**: it remains useful across a declared challenge family;
- **transfer**: it remains useful on another independently authored system;
- **causal effectiveness**: an appropriate interventional information measure improves at the macro level;
- **minimal state**: it is the smallest representation that preserves required future/intervention information.

These are not automatically equivalent.

### 6.2 A possible experiment schema

Given a system with microvariables (X), consider candidate partitions/coarse-grainings (phi_i(X)=Z_i).

For each (Z_i):

1. define a matched intervention family;
2. estimate prediction of future criterion outcomes;
3. estimate intervention-effect preservation;
4. estimate compression cost;
5. test stability across challenges;
6. compare against null/random partitions and obvious anatomical/spatial partitions;
7. do not optimize and test on the same data without a held-out contract.

A candidate objective might be conceptually:


J(phi) = intervention_prediction_retained - lambda * representation_complexity


This is only a sketch. The repository should prefer an established causal-abstraction or state-representation method if one fits, rather than inventing a bespoke metric.

### 6.3 Strong failure condition

The programme must allow:

> no privileged macro boundary was found; the micro representation or standard control representation remains superior.

Q1-009 makes this failure condition especially important.

---

## 7. Second promising lane: constraint-induced topology of competence

A broader research question is:

> **How do experimentally separable constraints reshape reachability, route structure, realization probability, and robustness, and which of those changes transfer across systems?**

This is already partially instantiated by P2-003–005 and Experiment 12.

### 7.1 Minimal decomposition

For each intervention/constraint (C), report separately where feasible:

- target reachable?
- shortest/lowest-cost route?
- number/diversity of routes?
- native policy realizes a route?
- realization robust across schedules/seeds/challenges?
- failure due to information, action repertoire, geometry, or policy?
- effect reversible after constraint removal?
- state representation sufficient to remove apparent history dependence?

### 7.2 Why this could add value

The project already has a competence profile, but this lens emphasizes that competence can fail for structurally different reasons:


goal exists but is unreachable


versus


goal is reachable but the native policy fails to realize it


versus


native policy succeeds only through a narrow/fragile route


versus


multiple redundant routes support robust recovery


Those differences matter mechanistically and could support predictive transfer.

### 7.3 Avoid a universal "striation score"

A tempting but probably bad move would be to invent one scalar "striation index."

The discussion itself gives reasons not to:

- reachability can grow while robustness falls;
- entropy can grow while welfare falls;
- shortest path can shrink while route redundancy collapses;
- controllability can rise while native policy realization remains poor.

Prefer a typed vector/profile unless a concrete benchmark establishes a useful scalar.

---

## 8. Third promising lane: state-dependent constraints and modulation

The mold/modulation distinction can become a technical question if expressed as:

> Does the constraint/transition rule itself update with system state or history?

A simple fixed-rule system has:


P(s_(t+1) | s_t)


with fixed parameters.

A modulating system has something like:


P(s_(t+1) | s_t, theta_t)


and:


theta_(t+1) = f(theta_t, s_t, o_t)


This can represent:

- adaptive thresholds;
- plastic controllers;
- changing resource gates;
- institutional scoring rules;
- developmental state changes.

The repository already distinguishes adaptation from fixed recovery. A modulation lane would therefore need to ask a sharper question than "parameters change."

Possible question:

> Which failure-boundary changes require plastic constraint parameters rather than a fixed high-dimensional controller?

Again, use adaptive-control/system-identification terminology in experiments.

---

## 9. Fourth lane: hysteresis, hidden state, and representation sufficiency

Experiment 12 A1 motivates this directly.

A history-dependent difference can arise because:

1. the physical system genuinely has persistent hidden state;
2. the chosen representation omits variables needed for Markov sufficiency;
3. different histories enter different basins despite similar visible states;
4. the intervention changes structure irreversibly.

A useful programme would explicitly test which explanation applies.

### 9.1 Matched-visible-state test

Find or construct pairs of states with closely matched visible representation but different histories.

Then test whether future recovery diverges under matched future stochastic/action streams.

If yes, search for additional latent variables that restore predictive sufficiency.

### 9.2 Representation ladder

Compare:

- visible morphology only;
- visible + local latent state summaries;
- visible + spatial latent compatibility;
- richer full state.

Ask at which representation historical labels cease adding predictive value.

This is a precise way to distinguish apparent hysteresis caused by coarse observation from deeper structural irreversibility.

---

## 10. "Line of flight" as an experiment-design heuristic

Do not introduce "line of flight" as a project metric. It can still suggest a useful intervention pattern.

Suppose a system repeatedly returns to a stable competence/failure regime under ordinary interventions.

Ask:

> Is there an intervention that changes the constraint graph so a previously unavailable class of trajectories becomes reachable?

Examples include:

- adding a missing actuator;
- restoring a communication channel;
- introducing fate plasticity;
- changing topology;
- releasing an immovable barrier;
- altering a regulatory input.

Formally, compare:


R_C(s)


and:


R_C'(s)


The important result is the change in reachability/route structure, not the philosophical label.

A strong experiment would preregister:

- which trajectories should become reachable;
- which should remain unreachable;
- why the specific constraint change should cause that change;
- what outcome would refute the mechanism.

---

## 11. "Territorialization" and attractors: useful only with an important distinction

The repository repeatedly warns that:

> specification satisfaction is not automatically competence.

That warning should govern any attractor-based use of territorialization.

Two systems may both converge to the same region:

### Passive system


s_t -> G


because (G) is simply a stable attractor.

### Active regulator


deviation -> sensing -> corrective action -> G


The first can be robust in a narrow sense but need not support claims about sensing, compensation, or adaptive regulation.

Therefore:

> territorialization can describe stabilization, but competence requires challenge-relative evidence about what mechanisms actively maintain or restore the criterion.

This is exactly aligned with the repository's existing scientific discipline.

---

## 12. Implications for Levin/TAME connections

The discussion repeatedly converged on ideas close to Levin's work:

- agents at multiple scales;
- goal-directedness without consciousness;
- problem spaces beyond ordinary physical coordinates;
- higher-level organization shaping lower-level option/action landscapes;
- developmental systems recovering large-scale morphology from local processes.

The repository already handles this carefully in ../wiki/concepts.md and ../wiki/ontology.md.

The additional insight from this discussion is:

> "higher-level agents bend lower-level option space" can be analyzed as a claim about how macro organization changes the reachable/likely transitions available to components.

That suggests an experimental translation:

1. define lower-level action/transition possibilities under baseline organization;
2. introduce or remove higher-level coupling;
3. compare reachable sets, route costs, and transition distributions;
4. ask whether the macro organization creates a stable, transferable change in those quantities.

Do not infer a higher-level agent merely because the action landscape changes. The attribution still needs the project's competence and boundary evidence.

---

## 13. Implications for Hoel / causal emergence

The discussion initially treated Hoel as a possible way to make coarse-graining non-arbitrary:

> choose a macro-description that has stronger causal structure than the micro-description.

Q1-009 makes the situation more interesting.

### What Q1-009 already establishes

- the project implemented interventional effective information rather than an observational proxy;
- analytic fixed points and finite-sample bias were tested;
- the chosen macro partition did not exhibit positive causal emergence in the tested non-degenerate cases;
- only one coarse-graining was tested;
- empowerment did not successfully operationalize the intended agency concept.

### The useful next question is therefore not

> "Does causal emergence exist?"

but:

> **Can an independently justified search/selection procedure identify a coarse-graining that improves intervention-relevant prediction or causal effectiveness without overfitting?**

Any such effort must compare against established causal-abstraction/coarse-graining methods.

A null result is acceptable and scientifically important.

---

## 14. Normative interpretation: control is not the thing to minimize

The discussion explicitly rejected:


less control = better


Examples make the failure obvious:

- immune regulation;
- pacemakers;
- morphogenesis;
- traffic coordination;
- error correction;
- public-health control of contamination.

A system can gain welfare from stronger constraint.

Therefore "liberating" and "constraining" should not be terminal value labels in this programme.

A consequentialist evaluation layer would instead ask:


constraint architecture -> P(tau) -> U(tau)


A more realistic version accounts for model uncertainty:


E_(M,tau)[U(tau) | C, pi, M]


This also explains why optionality may have **instrumental** rather than intrinsic value. Preserving reversible routes can be useful when the model of the future is uncertain. That is option value, not necessarily a metaphysical value of freedom.

The repository should remain neutral about the utility function unless a future application explicitly supplies one.

---

## 15. Important objections preserved from the dialogue

These objections should not be lost because they prevent the theoretical vocabulary from becoming sloppy.

### 15.1 "Relatively stable" is always scale-dependent

Any distinction relying on stable/temporary, mold/modulation, enclosed/open, or persistent/transient requires a reference timescale.

Therefore every such claim should implicitly or explicitly specify the temporal resolution.

### 15.2 "Possible/impossible" can be too binary

At the physical level, unusual perturbations or noise may make almost anything technically nonzero-probability.

Project-relevant "reachability" must therefore always be defined relative to:

- an allowed action/intervention set;
- a transition model;
- resource/time bounds if applicable;
- representation and tolerance.

The repository already does this well in graph-oracle work.

### 15.3 One realized worldline does not remove probabilistic modeling

Even if one adopts deterministic metaphysics, researchers do not have access to the exact microscopic state of the universe. Probability distributions remain epistemically and operationally necessary.

Therefore trajectory probabilities are legitimate scientific objects even if one rejects ontic randomness.

### 15.4 Killing is bodily control too

This is a reminder not to turn sovereignty/discipline/control into mutually exclusive mechanisms.

The categories are historically/philosophically suggestive, not a clean taxonomy of dynamical interventions.

### 15.5 Dividualization existed before databases

Modern systems increase degree, portability, automation, and causal reach. They do not create separable attributes from nothing.

### 15.6 More possible trajectories is not necessarily better

Support, entropy, controllability, robustness, and utility are different quantities.

### 15.7 "Agency" cannot be rescued by naming a metric agency

Q1-009's empowerment result is a concrete internal warning.

### 15.8 Coarse-graining is not automatically superior

Q1-009's negative causal-emergence result is a concrete internal warning.

### 15.9 Boundaries can be useful without being metaphysically fundamental

Operational utility is enough. A boundary can be model-relative and still scientifically valuable if it improves prediction, intervention, compression, or explanation.

---

## 16. Suggested research questions

The following are candidate questions, not commitments.

### R1. Boundary discovery

> Under a fixed observation/intervention family, which candidate coarse-graining best preserves intervention-relevant predictions while reducing microstate complexity?

Potential value: operationalizes dynamic enclosure and multiscale attribution.

Failure condition: microstate or obvious native representation remains best; no stable macro boundary transfers.

### R2. Constraint topology

> Which intervention-induced changes in reachability, route cost, and route redundancy predict competence/failure-boundary shifts across independently authored systems?

Potential value: unifies exact sorting reachability, NCA failure boundaries, and RNM comparison.

Failure condition: standard reachability/control analysis completely subsumes the competence layer.

### R3. Path dependence versus omitted state

> When two branches have matched observed macrostate but different histories, can richer state representations remove the future divergence?

Potential value: distinguishes genuine irreversible route changes from observation-induced apparent hysteresis.

Failure condition: no history effect after appropriate state matching, or ordinary latent-state variables fully explain it.

### R4. Constraint modulation

> Do dynamically updating constraint parameters produce competence/failure-boundary changes that fixed controllers of comparable capacity do not?

Potential value: gives technical content to mold/modulation.

Failure condition: fixed controller explains the effect equally well.

### R5. Route redundancy and robustness

> Conditional on target reachability and similar minimum path cost, does the diversity of independent routes predict recovery robustness?

Potential value: adds more structure than binary reachability.

Failure condition: route redundancy has no predictive value after ordinary state/geometry covariates.

### R6. Cross-scale option-space shaping

> Does introducing/removing a higher-level coupling systematically change lower-level reachable/action distributions in a way that predicts whole-system competence?

Potential value: operationalizes a Levin-like "bending option space" claim.

Failure condition: apparent effect reduces to local capacity/resource changes with no higher-level explanatory gain.

### R7. Blind identification of constraint topology

> Under restricted access, can an analyst identify whether failure is due to unreachability, poor route realization, or fragile route structure without being given the authored mechanism?

Potential value: joins constructive competence with Goal Discovery.

Failure condition: established active-learning/model-discrimination methods solve the benchmark with no added competence information.

---

## 17. Suggested experimental design principles

If any of the questions above are pursued:

1. **Reuse established machinery first.** RNM/Cellnition, standard reachability algorithms, causal abstraction methods, control theory, or system identification should be baselines where applicable.
2. **Freeze the representation before outcome inspection** when the representation itself is part of the claim.
3. **Separate opportunity from policy performance.**
4. **Match intervention burden where possible.**
5. **Preserve individual failures**, not only averages.
6. **State the temporal horizon** for any claim of path dependence or recovery.
7. **Do not infer formal unreachability from failure to recover within a finite horizon.**
8. **Do not infer semantic goals from an attractor, error signal, hidden state, or target-correlated variable alone.**
9. **Do not infer a privileged macro boundary from interpretability alone.**
10. **Allow negative results to collapse the philosophical interpretation back into ordinary control theory.**

---

## 18. How the earlier Deleuze taxonomy should and should not be used

### Potentially useful

The historical concepts can prompt questions such as:

- is a constraint fixed or dynamically updated?
- is it spatially local or distributed over time/information channels?
- does it alter the action set, the transition probabilities, or only the policy?
- does it create irreversible partitions?
- does it continuously modulate eligibility/access?
- does a representation of the system travel independently across contexts?

### Probably not useful for the current repository

Do not organize experiments around:

- sovereignty versus discipline versus control as mutually exclusive regimes;
- a general claim that digital control replaces bodily discipline;
- liberation as minimization of constraints;
- autonomous free will as the baseline being lost;
- "dividual" as a binary modern/nonmodern distinction.

Those formulations are too broad or normatively loaded for the repository's current evidence discipline.

---

## 19. A concise project-level synthesis

The useful residue of the discussion can be stated without Deleuzian terminology:

> **A competence claim should be understood against the geometry of the system's admissible trajectories. Constraints can change which outcomes are reachable, the costs and redundancy of routes, whether native dynamics exploit available routes, and how those routes survive perturbation. These effects depend on representation, boundary, scale, and history. The project already measures several pieces of this structure; the most promising extension is to test whether useful boundaries/coarse-grainings and transferable constraint-topology relations can be discovered rather than stipulated.**

The philosophical translation is:

> **"Territorialization/striation" can be treated heuristically as stabilization and channeling of trajectory space; a "line of flight" can be treated as a route made newly available by a changed constraint architecture.**

The technical warning is:

> **Those translations add value only if they generate predictions or comparisons not already supplied by reachability analysis, control theory, causal abstraction, or existing multiscale frameworks.**

---

## 20. Recommended immediate relation to current roadmap

This note should **not** displace the current project order in ../wiki/current.md.

The current evidence workbench and owner review remain the immediate priority. After that, the planned RNM comparator is particularly relevant because it can establish the baseline for transition-graph/reachability claims before any new "constraint topology" machinery is considered.

A sensible sequence would be:

1. complete current Experiment 12 review;
2. run or otherwise benchmark against RNM/Cellnition if the license/use gate is satisfied;
3. explicitly inventory which proposed "trajectory topology" quantities RNM already supplies;
4. identify one residual question that concerns competence, boundary discovery, restricted-access identification, or transfer;
5. only then design a new experiment.

This prevents the present theoretical synthesis from becoming another vocabulary layer in search of a problem.

---

## 21. Dialogue-derived conceptual checkpoints

These are short checkpoints capturing the strongest transformations in the discussion.

### Checkpoint A — from objects to processes

Initial claim:
> society is made of machines.

Refinement:
> "machine" is useful when it selects a process/transformation that an object-level description hides; it is not evidence that ordinary objects are unreal.

### Checkpoint B — from enclosure to boundary selection

Initial claim:
> discipline encloses bodies in space.

Refinement:
> physical enclosure is one kind of coarse-grained causal boundary; useful boundaries can be dynamical, temporal, informational, or relational.

### Checkpoint C — from autonomy to causal leverage

Initial claim:
> control undermines autonomous individual agency.

Refinement:
> ask which variables/interventions change future trajectories and at what scale; no libertarian free-will premise is required.

### Checkpoint D — from dividual as category to dividualization as degree

Initial claim:
> modern control replaces individuals with dividuals.

Refinement:
> attributes have always been separable; modern systems increase their independent mobility, recombination, automatic classification, and causal reach.

### Checkpoint E — from discipline/control binary to fixed/adaptive constraints

Initial claim:
> discipline molds; control modulates.

Refinement:
> both are constraints; the useful distinction is whether constraint parameters remain fixed or update with state/history at the chosen timescale.

### Checkpoint F — from control to trajectory geometry

Initial claim:
> systems control possible futures.

Refinement:
> distinguish reachability, transition probability, route cost, route redundancy, policy realization, robustness, and path dependence.

### Checkpoint G — from liberation to option structure

Initial claim:
> liberation widens possible futures.

Refinement:
> more support/entropy is not necessarily good; controllability, option value, robustness, and welfare are distinct.

### Checkpoint H — from philosophical liberation to normative separation

Initial claim:
> praxis should seek lines of flight/resistance.

Refinement:
> escaping a constraint is not intrinsically welfare-improving; descriptive trajectory structure and normative evaluation must remain separate.

### Checkpoint I — from arbitrary coarse-grain to empirical test

Initial claim:
> useful macro boundaries may outperform micro descriptions.

Refinement:
> Q1-009 already tested one such claim and found no causal emergence for its chosen partition; macro privilege must be demonstrated, not assumed.

### Checkpoint J — from agency metric to construct validation

Initial claim:
> empowerment may quantify agency.

Refinement:
> in Q1-009 the implemented measure tracked unused unilateral capacity/idleness; a measure's semantic interpretation must be validated by interventions.

---

## 22. Terms worth searching in neighboring literatures before building anything

If the ideas in this note become active work, literature/reuse searches should include at least:

- state-space reachability;
- controllability;
- viability theory / viability kernels;
- basin geometry;
- metastability;
- hysteresis;
- path dependence;
- causal abstraction;
- state aggregation / bisimulation;
- predictive state representations;
- sufficient statistics for control;
- Markov state abstraction;
- options / option value under uncertainty;
- robust control;
- adaptive control;
- switched/hybrid systems;
- active system identification;
- causal emergence / effective information;
- macrovariable discovery;
- empowerment and intrinsic control measures;
- graph robustness / path diversity;
- network controllability;
- goal recognition and Goal Recognition Design;
- specification mining;
- active automata learning;
- Regulatory Network Machine / Cellnition.

The repository's reuse-first rule should apply before any bespoke "territorialization," "striation," or "dynamic enclosure" metric is implemented.


---

## 23. Additional discussion lanes worth preserving

These directions emerged after the first research note was drafted. They are closely related to the same trajectory-space framework and should be treated as candidate research questions, not established project findings.

### 23.1 Cross-scale conflict in competence

Much of the Collective Competence programme asks how component capabilities and interactions produce whole-level competence. An equally important inverse question is:

> **When does increasing competence at one scale reduce competence at another?**

For nested systems, it may be possible that:

```text
delta K_collective > 0
delta K_component  < 0
```

Examples in principle include:

- a tissue becoming better at maintaining global morphology by restricting the option space of individual cells;
- an organization becoming more coordinated while reducing the independent controllability of its members;
- a higher-level controller eliminating local degrees of freedom to gain robustness at the collective level.

This would make multiscale competency less harmonious than a simple "competence scales upward" narrative.

A useful experimental question is:

> Under what interventions do gains in whole-system robustness, recovery, or controllability systematically trade off against lower-level reachable states, local empowerment, flexibility, or resource access?

This should not be framed normatively by default. A reduction in component option space can be beneficial, harmful, or neutral depending on the criterion under study.

This lane may also provide a more rigorous interpretation of the earlier "liberating versus constraining forces" discussion: the same architecture can expand one scale's reachable/controllable trajectory set while narrowing another's.

### 23.2 A good causal coarse-grain is not automatically an agent

The discussion around Hoel-style causal emergence and Levin-style multiscale agency exposes an important distinction.

A macro-description can be:

- causally coherent;
- predictively useful;
- interventionally sufficient;
- highly compressed;

without necessarily being an **agent**.

It may be useful to distinguish at least four layers:

1. **causal coherence** — macrovariables capture reliable causal structure;
2. **control coherence** — interventions at that level provide a useful description of steering;
3. **goal coherence** — a stable goal-relative criterion can be attributed at that level;
4. **competence** — the system robustly attains, maintains, restores, or adapts toward that criterion over a declared challenge family.

This suggests a hierarchy rather than an identity:

```text
good coarse-grain
    does not imply controller
    does not imply agent
    does not imply high competence
```

The exact implication structure is itself a research question.

This is especially relevant because Q1-009 already showed that one intuitively meaningful macro partition did **not** exhibit positive causal emergence, and that an empowerment measure did **not** warrant an agency interpretation.

A future macro-boundary search should therefore avoid treating "high causal effectiveness" as sufficient evidence for agency.

### 23.3 Representation-relative hysteresis and Markov sufficiency

The earlier path-dependence discussion can be sharpened through a representation question.

Suppose that, under an observed representation X_t:

```text
P(X_(t+1) | X_t, H) != P(X_(t+1) | X_t)
```

where H is prior history.

This appears history-dependent.

But after adding latent variables Z_t, it may become:

```text
P(X_(t+1), Z_(t+1) | X_t, Z_t, H)
=
P(X_(t+1), Z_(t+1) | X_t, Z_t)
```

Then the apparent hysteresis was partly a consequence of an insufficient state representation.

This motivates a research question:

> **At what representation does history cease to provide additional predictive power over future trajectories?**

For Experiment 12, this could mean comparing:

- visible morphology only;
- visible morphology plus local hidden-state summaries;
- visible morphology plus spatial latent compatibility;
- full NCA state.

A useful outcome would be a **representation ladder** showing where the process becomes approximately Markov-sufficient for recovery prediction.

This would help separate:

- hidden-state path dependence;
- basin dependence;
- irreversible structural changes;
- mere observational insufficiency.

It would also make "memory" claims more precise.

### 23.4 Goal equivalence versus causal/mechanistic equivalence

The repository already handles goal ambiguity carefully: multiple candidate criteria may remain behaviorally equivalent under a declared observation/intervention contract.

There is an analogous hierarchy for mechanisms.

Two systems or explanations may be:

1. **observationally equivalent** — same observed trajectories under passive observation;
2. **interventionally equivalent** — same outputs under the allowed intervention family;
3. **mechanistically distinct** — different internal causal organizations despite observational/interventional equivalence under the current contract.

A useful inclusion relation is:

```text
mechanistic identity
    is narrower than interventional equivalence
    is narrower than observational equivalence
```

This suggests that competence itself may sometimes be best represented not as a property of one mechanism but as an **equivalence class of counterfactual behavior under a declared intervention family**.

That would align naturally with the project's emphasis on access contracts and abstention.

Potential research question:

> Can two mechanistically different systems be competence-equivalent over one challenge family but separate under a targeted intervention chosen to distinguish their counterfactual structure?

This also creates a bridge between Goal Discovery, active model discrimination, and mechanism inference.

### 23.5 Option value under model uncertainty

The earlier discussion rejected the idea that "more freedom" or "more trajectories" is automatically good.

However, preserving future options can have **instrumental value** under uncertainty even when optionality has no intrinsic value.

A standard option-value form is:

```text
V_option
=
E[max_a U(a) | future information]
-
max_a E[U(a) | current information]
```

The intuition is:

- committing early may maximize expected utility under the current model;
- preserving reversibility may become better if future information can change which action is optimal;
- therefore "less striation" or "more reachable alternatives" can sometimes be useful because the model is uncertain, not because freedom is intrinsically valuable.

This gives a consequentialist explanation for why irreversibility and lock-in can matter.

Potential relevance to the repository:

- compare interventions with similar short-horizon performance but different retained future reachability;
- measure whether preserved route diversity improves performance after later environmental changes;
- distinguish immediate utility from retained option value.

This could connect competence, flexibility, adaptation, and uncertainty without introducing a normative commitment beyond the chosen utility/criterion.

### 23.6 The observer/metric can enter the causal loop

Goal Discovery currently treats analyst access and representation carefully, but a stronger reflexive case is possible:

> the act of measuring/classifying a system changes the system because the classification becomes consequential.

This creates a loop:

```text
measurement
    -> policy/selection
    -> behavioral adaptation
    -> new measurement
```

This is relevant to Goodhart-like dynamics, algorithmic scoring, adaptive institutions, and any system where agents respond to the metric used to evaluate them.

The important distinction is between:

- **passive observation** — measurement does not alter the transition structure;
- **measurement-coupled control** — a score or inferred state is fed back into access, rewards, penalties, or environment;
- **strategic adaptation** — the measured system changes behavior in response to the metric.

This is arguably one of the strongest technically meaningful descendants of the original "society of control" discussion.

Potential research questions:

- When does a metric remain predictive after becoming control-relevant?
- How quickly does behavior adapt to the measurement rule?
- Does adaptive metric replacement create a higher-order modulation loop?
- Can an intervention distinguish genuine competence improvement from metric gaming?

### 23.7 Endogenous modification of the problem/action space

Most competence analyses assume a fixed:

- state space S;
- action set A;
- goal criterion G.

But sufficiently capable systems can modify the very space in which they act.

Examples include:

- inventing a tool;
- creating a new communication channel;
- changing morphology;
- altering the environment;
- creating new institutions;
- adding a new sensor;
- changing the representation used to define success.

Then:

```text
(S_t, A_t, G_t)
    ->
(S_(t+1), A_(t+1), G_(t+1))
```

This is more than navigating a fixed problem space. It is **transforming the problem space**.

This may be an important distinction between ordinary control and open-ended competence.

Potential research questions:

1. Can a system increase its competence by changing its own action repertoire rather than improving policy within a fixed repertoire?
2. Can it create new observables that make previously indistinguishable states separable?
3. Can it alter topology so previously unreachable targets become reachable?
4. Can it redefine an effective macrovariable or boundary in response to challenge?
5. How should competence be measured when S, A, or G changes during the episode?

This lane seems particularly relevant to morphogenesis, tool use, collective reorganization, and adaptive systems.

### 23.8 Why cross-scale conflict and problem-space modification are especially interesting

Among these additional lanes, two appear least reducible to ordinary static reachability analysis:

- **cross-scale competence conflict**;
- **endogenous modification of state/action/problem space**.

The first asks how constraint benefits and costs redistribute across nested levels.

The second asks how a system changes the transition graph itself rather than merely navigating it.

Together they suggest a broader picture:

> A collective can be competent not only because it moves effectively through a given trajectory landscape, but because it can reshape that landscape—possibly improving controllability at one scale while constraining it at another.

That is a potentially important extension of the current trajectory-space framing, but it still requires operational definitions and established-method comparison before becoming a project claim.


---

## 24. Further research lanes: composition, observability, plasticity, and bounded reachability

These additional directions emerged from the same trajectory-space discussion. They are plausible extensions of the programme but are not established findings.

### 24.1 Observability–controllability–policy decomposition

The repository already distinguishes missing information from missing actions. This can be sharpened into a general failure taxonomy.

A goal-relative failure can occur because:

1. **observability failure** — the system cannot distinguish states that require different responses;
2. **controllability/reachability failure** — the system cannot reach the required state with its available actions;
3. **policy/realization failure** — the required state is observable and reachable, but the native dynamics/policy fail to exploit the available route.

In compact form:

```text
failure
  -> cannot distinguish relevant states
  -> cannot reach required states
  -> can distinguish and reach, but policy fails
```

This is potentially useful because several existing experiments already instantiate different branches of this decomposition:

- reporter failure and hidden abundance ambiguity are observability failures;
- lineage extinction without fate plasticity is an action/reachability failure;
- P2-005 explicitly isolates reachable-but-unrealized routes.

A strong research question is:

> Can competence failures across different substrates be classified prospectively by which of these three bottlenecks is experimentally load-bearing?

The taxonomy should remain open to mixed failures where more than one bottleneck is active.

### 24.2 Competence composition

A central question for a project named Collective Competence is:

> **Under what conditions do competent parts compose into a competent whole, and when does composition destroy or transform competence?**

There is no reason to expect additivity:

```text
K(A + B) != K(A) + K(B)
```

Possible regimes include:

- competent parts produce an incompetent whole;
- individually weak parts produce a highly competent whole;
- coupling creates a new competence unavailable to either part alone;
- adding a competent component reduces whole-system competence;
- the whole inherits only a subset of part-level competencies;
- the whole gains robustness at the cost of component flexibility.

This suggests a compositional research programme in which the important variable is not only the competence of components, but the **coupling architecture** between them.

Potential questions:

1. Which competence dimensions are compositional?
2. Which require specific coupling topologies?
3. When does adding a component enlarge reachable state space but reduce robust realization?
4. When does redundancy increase reliability versus create interference?
5. Can a whole-level competence be predicted from component capability profiles plus coupling descriptors?

A useful negative result would be that no substrate-neutral composition rule survives transfer.

### 24.3 Robustness–plasticity tradeoffs

Strong canalization toward a stable target can improve recovery from familiar perturbations while reducing adaptation to novel conditions.

This suggests a tension:

```text
stronger stabilization
    -> familiar-perturbation robustness may increase
    -> adaptability/plasticity may decrease
```

This is not a universal law; it is a hypothesis family.

The important distinction is between:

- **robustness** — staying or returning to a criterion under perturbation;
- **plasticity** — changing policy, structure, or representation to handle new conditions;
- **flexibility** — achieving the same criterion by different means;
- **adaptation** — retained change that improves later performance.

Potential experiments could hold nominal performance constant while varying plasticity and then challenge systems with out-of-distribution perturbations.

This lane connects the earlier "territorialization" language to a concrete scientific tension: deep basins can be useful until the environment changes enough that leaving the basin becomes necessary.

### 24.4 Endogenous goal change

The previous section considered systems that can modify state and action spaces. A more difficult case is when the effective goal criterion itself changes.

Conceptually:

```text
G_t -> G_(t+1)
```

This raises several identification problems.

A changed trajectory may reflect:

- policy adaptation toward the same goal;
- changed estimate of the environment;
- changed representation of the goal;
- genuine goal drift;
- a switch among multiple latent objectives.

Potential research questions:

1. What intervention evidence would distinguish policy adaptation from goal change?
2. Can a restricted-access analyst detect a goal switch without semantic labels?
3. When several candidate goals explain pre-change behavior, can a post-change intervention shrink the equivalence class?
4. How should competence be defined when the criterion itself is time-varying?

This is particularly relevant to Goal Discovery because a fixed candidate-goal family may be insufficient if the system changes what it is regulating toward.

### 24.5 Multi-objective competence and Pareto structure

Many real systems face more than one goal or viability constraint.

Instead of one scalar objective, consider:

```text
U_1, U_2, ..., U_n
```

A system may then occupy a **Pareto frontier**: improving one objective necessarily worsens at least one other objective.

This matters because "more competent" can become ill-defined even within one scale.

Potential questions:

- Does an intervention move the system to a better Pareto region or merely trade one competence dimension for another?
- Are cross-scale conflicts actually multi-objective tradeoffs in disguise?
- Can challenge families reveal hidden objectives because different perturbations expose different tradeoff surfaces?
- Does a collective improve by dynamically reweighting objectives rather than maximizing a fixed one?

The repository should avoid collapsing such cases into one scalar unless the aggregation rule is explicitly supplied.

### 24.6 Causal bottlenecks and load-bearing leverage

Some small component, signal, or interaction can control a disproportionately large part of future trajectory space.

A useful operational question is:

> How much does intervening on component or relation i contract, expand, or redirect the reachable and robust trajectory set?

Possible bottleneck measures could compare:

- change in reachable-set size;
- change in minimum route cost;
- change in route redundancy;
- change in recovery probability;
- change in competence-profile dimensions.

This is close to the repository's existing "causally load-bearing" language but emphasizes **leverage over trajectory geometry**.

A component can be causally load-bearing even if it is physically small, rarely active, or statistically unremarkable under passive observation.

That makes intervention-based measurement essential.

### 24.7 Timescale-dependent agency and boundary selection

The earlier discussion objected to undefined claims of "temporary" or "stable" organization. The same issue applies to agent boundaries.

The most useful boundary may depend on the prediction/intervention horizon.

Conceptually:

```text
B_star = B_star(T)
```

where T is the horizon or timescale of interest.

Examples in principle:

- at millisecond scales, a local neural/cellular subsystem may be the useful unit;
- at developmental timescales, tissue-level organization may be more predictive;
- at longer horizons, organism–environment or social collectives may become the more useful boundary.

This suggests that boundary discovery should not search for one timeless privileged agent.

Instead ask:

> Which boundary/coarse-graining is most interventionally useful at horizon T for criterion family G and challenge family D?

A boundary that is excellent for short-horizon prediction may be poor for long-horizon control.

### 24.8 Adversarial competence and co-adaptive environments

Most current competence examples treat the environment as passive or exogenously changing.

A harder case is an environment containing another adaptive system that reacts strategically.

Then:

```text
P(s_(t+1) | s_t, a_t, E_t)
E_(t+1) = f(E_t, system behavior)
```

The environment becomes part of the feedback loop.

Relevant phenomena include:

- arms races;
- deceptive signals;
- strategic obstruction;
- adaptive countermeasures;
- cooperation/competition mixtures;
- changing action costs in response to observed policy.

Potential research questions:

1. Does a competence profile measured against passive perturbations predict performance against adaptive adversaries?
2. Which capabilities become load-bearing only under co-adaptation?
3. Can route redundancy protect against adversarial blocking?
4. Does an adversary reveal hidden constraints that random damage does not?

This could extend the challenge-family concept from perturbation distributions to **responsive opponents**.

### 24.9 Counterfactual identity under component replacement

Regeneration and collective reorganization raise an identity question:

> If components are replaced while a system preserves its competence profile and causal organization, in what operational sense is it the same agent/system?

A possible research-friendly approach is to treat identity as preservation of some counterfactual organization rather than preservation of matter.

Candidate invariants might include:

- response to intervention family;
- goal-equivalence class;
- reachable/robust trajectory structure;
- controller architecture;
- competence profile.

This should not become a metaphysical claim by default.

A useful question is:

> Which transformations can replace parts while preserving the system's experimentally measured counterfactual behavior?

This is particularly relevant to regeneration because a recovered morphology may contain different material components while preserving higher-level function.

### 24.10 Resource-bounded reachability

Binary graph reachability is often too permissive.

A target that is reachable only after an astronomically long sequence or with unrealistic energy/information requirements is not practically available.

A more useful object is something like:

```text
R_C(s ; T, E, I)
```

where:

- T = time budget;
- E = energy/resource budget;
- I = information/observation budget.

This connects naturally to the repository's challenge/resource-family language.

Potential questions:

- How does competence change as resource budgets tighten?
- Are two systems equally reachable but radically different in practical route cost?
- Does one architecture preserve performance by spending more information, time, or energy?
- Can apparent failure be reclassified as resource-bounded rather than structurally unreachable?

This extension also gives a cleaner interpretation of "accessible possibility" than unconstrained physical possibility.

### 24.11 Why competence composition and the three-way failure decomposition are especially central

Two of these lanes appear especially foundational for the repository.

First:

> **competence composition** asks what it means for a collective to possess a competence not reducible to simply listing component competencies.

Second:

> **observability–controllability–policy decomposition** asks exactly where a competence failure occurs.

Together they suggest a disciplined framing:

```text
components + coupling
    -> what information distinctions are available?
    -> what state transitions are available?
    -> what routes does the native policy realize?
    -> what competence profile appears at the collective scale?
```

This could provide a rigorous bridge from mechanism to collective-level competence without assuming that emergence, agency, or intelligence follows merely from impressive global behavior.


---

## 25. Additional lanes: requisite variety, intervention bases, meta-competence, and abstraction

These ideas emerged after the prior research sections. They are candidate directions only and should be evaluated against established cybernetics, control, diagnosis, and experimental-design literatures before any new framework is built.

### 25.1 Requisite variety

Ashby's Law of Requisite Variety is highly relevant to the repository's existing separation of information, action repertoire, and challenge family.

A compact intuition is:

```text
effective response variety
    must be sufficient for
relevant disturbance variety
```

The important word is **relevant**. A regulator does not need a unique response to every microscopic disturbance; it needs enough distinctions and actions to handle the disturbance classes that require different corrective responses.

This creates a useful decomposition:

- disturbance classes that matter for the criterion;
- observations that distinguish those classes;
- actions capable of producing the required different responses;
- policy/controller that maps distinctions to actions.

Several existing experiments already resemble failures of requisite variety:

- different hidden abundances become observationally indistinguishable after reporter failure even though they require different repair actions;
- a system can know the desired composition but lack an action capable of regenerating a missing lineage;
- barriers can remove required routes even when the target and local rule remain intact.

A useful research question is:

> Can competence failure be predicted by a mismatch between challenge-relevant disturbance classes and the system's effective distinguishable-response repertoire?

This could potentially unify observability and controllability without collapsing them.

### 25.2 Minimal intervention basis

Goal Discovery asks which interventions discriminate rival explanations. A sharper question is:

> **What is the smallest intervention family sufficient to distinguish the surviving model/goal/competence equivalence classes?**

Suppose the current evidence leaves rivals:

```text
M1, M2, ..., Mn
```

The objective is to find a compact intervention set I_star such that the rivals make different counterfactual predictions under I_star.

This turns active experiment design into a compression problem:

```text
many possible interventions
    ->
smallest sufficient discriminating basis
```

Possible quantities include:

- number of interventions;
- total intervention cost;
- experimental time;
- expected information gain;
- robustness of discrimination to noise;
- whether the result transfers across initial conditions.

This is especially relevant to the repository because it already values abstention and preservation of equivalence classes. The next experiment need not identify everything; it should be chosen to maximally reduce the ambiguity that matters.

A strong benchmark would compare any project-specific intervention-selection method against established active diagnosis, optimal experiment design, Goal Recognition Design, or active automata/model-learning methods.

### 25.3 Critical transitions in competence

Competence boundaries may sometimes be sharp rather than smoothly degrading.

A parameter can vary gradually while the system remains competent until a threshold region is crossed, after which recovery collapses or a different regime appears.

Potential signatures near such a boundary could include:

- increasing recovery time;
- increased variance across matched stochastic streams;
- increased sensitivity to small perturbations;
- shrinking route redundancy;
- sudden loss of reachability;
- basin boundary crossing.

Experiment 12's different recovery regimes across lesion sizes make this conceptually relevant, but the existing sparse radius points are not enough to claim a critical phenomenon.

A careful research question would be:

> Does competence loss occur through a smooth degradation or through identifiable regime transitions in a declared challenge parameter space?

This should be tested with sufficiently dense sampling and without importing phase-transition language merely because a curve looks steep.

### 25.4 Temporal abstraction of competence

A competence at one scale may become an atomic action at a higher scale.

For example:

```text
many micro actions
    ->
reliable lower-level skill
    ->
one macro-level action primitive
```

This suggests a hierarchy in which:

- lower-level dynamics implement a skill;
- higher-level control treats that skill as an available action;
- higher-order competencies compose those action primitives.

This may provide a cleaner account of multiscale agency than merely asserting that agents exist at many scales.

Potential questions:

1. When is a lower-level competence reliable enough to be abstracted as a macro action?
2. What error model should accompany that abstraction?
3. How does higher-level planning change when a lower-level skill degrades?
4. Can macro competence be predicted from a library of lower-level options plus their failure boundaries?

This also connects competence composition to hierarchical control and options/skills in reinforcement learning.

### 25.5 Meta-competence and self-diagnosis

A system may not only recover from failure but identify **why** recovery is failing and change strategy accordingly.

A useful hierarchy is:

```text
ordinary competence
    -> act toward criterion

robust competence
    -> continue or recover under perturbation

meta-competence
    -> diagnose the failure class
    -> reconfigure sensing/action/policy
    -> restore competence if possible
```

Relevant failure classes might include:

- sensor/reporter failure;
- actuator failure;
- action-space restriction;
- resource depletion;
- structural unreachability;
- memory loss;
- model mismatch.

The repository's reporter-failure and action-repertoire experiments make this especially relevant.

Potential research question:

> Can a system distinguish failure modes that produce similar immediate performance loss and select different corrective responses appropriate to each?

This would require matched failures that are behaviorally similar at first but demand different interventions.

### 25.6 Competence universality classes

Different substrates may implement competence through very different mechanisms while sharing the same abstract failure structure.

Possible classes include:

- observation-limited;
- action-limited;
- route/barrier-limited;
- memory-limited;
- coordination-limited;
- resource-limited;
- plasticity-limited;
- diagnosis-limited.

The stronger claim would not be that these are universal natural kinds, but that they form useful **counterfactual equivalence classes** across systems.

A transferable class would require:

1. the same intervention distinction to predict failure across independently authored systems;
2. similar counterfactual signatures despite different implementation details;
3. better explanatory or predictive value than substrate-specific surface descriptors.

This may fit the project's transfer-first strategy better than searching for one universal scalar of competence.

### 25.7 Morphological and environmental computation

Some of a system's apparent intelligence or control burden may be carried by body structure or environmental regularities rather than an explicit controller.

A useful decomposition is:

```text
controller organization
+
body/morphology
+
environmental structure
    ->
observed competence
```

Changing the focal boundary can therefore move apparent "computation" between:

- controller;
- body;
- environment.

This is directly relevant to dynamic enclosure and boundary discovery.

Potential questions:

- Can morphology reduce the control complexity required for successful behavior?
- Does changing environmental structure preserve competence after controller simplification?
- Which intervention reveals whether the body/environment is causally load-bearing rather than merely correlated with success?
- Does the best predictive boundary include persistent environmental structure?

This lane should connect to established morphological-computation and embodied-cognition work rather than inventing a parallel vocabulary.

### 25.8 Early-warning signals for competence loss

Most failure-boundary mapping detects the boundary by observing actual failure.

A stronger capability would be to identify signs that the system is approaching loss of competence **before** the criterion is violated.

Candidate signatures could include:

- increasing recovery time;
- rising intervention cost;
- reduced route redundancy;
- increased sensitivity to small perturbations;
- growing dependence on one bottleneck;
- increased variance across matched replications;
- narrowing viability margin.

The key question is:

> Can an external observer—or the system itself—predict impending loss of recoverability from pre-failure dynamics?

This connects failure-boundary work to diagnosis and intervention timing.

A strong result would require prospective prediction of later failure, not retrospective fitting after the boundary is known.

### 25.9 A possible progression from competence to meta-competence

Several of these ideas form a coherent progression:

```text
1. requisite variety
   enough distinctions and actions exist

2. intervention identification
   determine which distinctions are causally relevant

3. failure diagnosis
   identify which capability or constraint is failing now

4. adaptive reconfiguration
   alter sensing, action repertoire, policy, or structure

5. restored competence
   return to or redefine a viable goal-relative regime
```

This progression could be useful because it connects several currently separate research themes:

- information sufficiency;
- reachability;
- active experiment design;
- diagnosis;
- plasticity;
- adaptive control.

It also suggests a stronger notion of competence than merely producing a successful trajectory.

### 25.10 Why these lanes may matter

Among this set, three directions appear especially likely to change experimental design rather than only vocabulary:

- **requisite variety** — because it may unify information and action limitations relative to challenge complexity;
- **minimal intervention basis** — because it turns identifiability into an explicit experiment-selection problem;
- **meta-competence/self-diagnosis** — because it asks whether a system can discriminate the cause of its own failure and reconfigure accordingly.

Together they point toward a general architecture for experimentally characterizing problem-solving systems:

```text
challenge variety
    ->
available distinctions
    ->
available actions
    ->
route realization
    ->
failure diagnosis
    ->
adaptive reconfiguration
```

Any such architecture should still be treated as a hypothesis scaffold. Established cybernetics, fault diagnosis, active experiment design, adaptive control, and systems engineering should be used as comparators before claiming a distinct project contribution.

---

## 26. Final research stance

The discussion does not justify adding Deleuze as a foundational theory of the project.

It does justify a narrower claim:

> **The philosophical vocabulary highlighted a family of technical questions the repository is already partly equipped to answer: how constraints reshape reachable and realized trajectories; how those effects depend on scale, representation, and history; and whether a causally useful collective boundary can be identified rather than stipulated.**

The strongest existing evidence relevant to that family is already in:

- P2-003: exact immovable-barrier reachability;
- P2-004: exact moveable-passive order invariant;
- P2-005: opportunity versus realization versus robust realization;
- Experiments 06–11: information/action/memory/reachability decomposition;
- Experiment 12: multidimensional external-system failure boundaries and path-dependent action restriction;
- Q1-009: negative causal-emergence result for the chosen coarse-grain and failed agency interpretation of empowerment;
- issue #75: planned RNM reachability/path-dependence comparator.

The strongest candidate extension is:

> **discover and validate boundaries/coarse-grainings and constraint-topology features that predict competence/failure boundaries across interventions and across independently authored systems.**

If established control/reachability/causal-abstraction methods already answer that question, the correct project outcome is to adopt them and reduce the philosophical story rather than manufacture a parallel framework.
