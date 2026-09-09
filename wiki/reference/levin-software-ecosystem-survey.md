---
doc-role: external-software-landscape-survey
authority: research-reference
lifecycle: active
surveyed: 2026-09-09
sources:
  - https://drmichaellevin.org/resources/software.html
  - research-landscape.md
  - ../questions.md
---
# Levin-lab software ecosystem: overlap, prior art, and substrate survey

[Reference index](README.md) · [Research landscape](research-landscape.md) · [Research questions](../questions.md) · [Current work](../current.md)

## Why this survey exists

The Levin lab's software page contains a much denser body of executable prior work than a paper-only literature scan makes obvious. Several packages are not merely generic tools: they instantiate questions that overlap directly with this programme's constructive **Collective Competence** arm, while others provide ready-made external systems for the **Goal and Competence Discovery** arm.

This survey asks four questions for every relevant package listed on the Levin software page as of 2026-09-09:

1. **Does it already answer or instantiate a question this repository might otherwise claim as novel?**
2. **Does it supply a mature system that should be reused instead of rebuilt?**
3. **What does it *not* solve, especially with respect to candidate-goal and competence identifiability under restricted observation/intervention access?**
4. **What should this project do about it: abandon a novelty claim, reframe, reuse as a substrate, or keep only as a method/reference?**

The main source is Michael Levin's [Tools and Software page](https://drmichaellevin.org/resources/software.html), checked against the linked repositories and associated papers where the overlap is scientifically important. This is an overlap/strategy audit, **not** a claim that the remaining niche is already novel. Broader novelty still requires surveying adjacent control, inverse-problem, causal-inference, system-identification, agency-detection, and IRL/goal-recognition literatures.

## Executive conclusion

The audit materially narrows the defensible contribution of this repository.

The following broad claims are **already heavily occupied** and should not be presented as the project's novelty:

- simple/local cellular policies can yield robust whole-level morphogenesis;
- changing component-level competency changes whole-system developmental/evolutionary outcomes;
- cell-level homeostatic goals can scale into larger anatomical goals;
- local communication, shared stress/error signals, finite resources, bioelectric fields, and learned local policies can coordinate morphology;
- morphogenetic systems can exhibit regeneration, rescaling, persistence, distributed pattern information, and apparent memory;
- goal-directed morphogenesis can be framed with control, Bayesian, active-inference, or multiscale-cognition language;
- stable-state landscapes can be turned into intervention/reachability maps with path dependence, cycles, and unreachable states;
- regulatory mechanisms can be inferred automatically from formalized perturbation/phenotype data;
- distributed sorting is already explicitly studied as a basal-cognition/morphogenesis model.

The strongest surviving project identity is therefore not **"show that collectives can be competent"** and not **"decompose morphogenetic competence into familiar ingredients."** It is closer to:

> **Given a declared observation/intervention access contract, which goal-relative competence claims are supported, contradicted, or underdetermined by behavior; and can experimentally separable capability constraints make risky predictions about competence and failure boundaries across independently authored systems?**

That question is still a hypothesis, not a novelty verdict. The practical implication is much firmer: **the project should become reuse-first and interrogation-first. Do not build another general tissue simulator or another bespoke developmental toy merely to demonstrate a primitive already represented in this ecosystem.**

## Interpreting the two motivating images

The first image that prompted this audit depicts a multiscale developmental model in which each cell observes a local neighborhood, embeds/aggregates neighboring state, applies a shared ANN policy, and updates its own state; a genome contains structural initial-state information plus shared functional ANN parameters, while selection acts on final morphology. That architecture is not just visually adjacent to our constructive programme: it is the setting of the **Cellular Competency** line of work, where the competence of local developmental agents is varied and organism-level evolutionary consequences are measured.

The second image is a membrane-voltage tissue simulation of the kind implemented by **BETSE** (BioElectric Tissue Simulation Engine). BETSE already supplies a detailed 2-D multiphysics tissue substrate with electrodiffusion, ion channels, gap junctions, gene-regulatory and biochemical networks. The correct lesson is not that bioelectric work is off limits; it is that building our own general bioelectric tissue engine would add little scientific value compared with wrapping an established model under the Dynamical Laboratory intervention/evidence contract.

## Highest-overlap systems

### 1. Sorting Algorithms as Basal Cognition

**Software/paper:** Taining Zhang, Adam Goldstein, Michael Levin, *Classical sorting algorithms as a model of morphogenesis: Self-sorting arrays reveal unexpected competencies in a minimal model of basal intelligence*, Adaptive Behavior (online 2024; vol. 33). DOI `10.1177/10597123241269740`. Source code is linked from the Levin software page.

**What it already does:** recasts classical sorting as distributed element-level agency, removes assumptions of top-down control and perfect hardware, studies failures/damage, robustness, problem-space traversal, defect circumvention, and chimeric mixtures of sorting policies.

**Overlap:** direct prior art for Experiment 01. Our self-sorting work should be treated as a calibration/reproduction-and-extension surface, not a novel demonstration that local rules produce robust global order or that sorting can model basal cognition.

**Still useful here:** Experiment 01 can remain valuable because our programme uses it to calibrate distinctions such as attainment versus continued maintenance, intervention design, and later blind analysis. Those are programme-method uses, not novelty of the sorting phenomenon.

**Action:** **retain as calibration; explicitly disclaim novelty.**

### 2. Cellular Competency evolution model

**Repository:** `https://github.com/lksshw/CellularCompetency`

**Paper:** Lakshwin Shreesha & Michael Levin (2023), *Cellular Competency during Development Alters Evolutionary Dynamics in an Artificial Embryogeny Model*, Entropy 25(1):131. DOI `10.3390/e25010131`.

**What it already does:** compares developmental systems whose cells have different degrees/forms of local task-solving ability and asks how competent cellular behavior changes the mapping from genome to final morphology and therefore evolutionary dynamics.

**Overlap:** this directly occupies the broad constructive question "how does component capability affect whole-level competence?" It is especially close to any framing in which a cell has a perception → policy → action loop and whole-level morphology is selected/evaluated.

**What it does not settle for us:** it does not provide a general identifiability theory for what an external analyst may infer about candidate goals or competence dimensions under an intentionally restricted access contract.

**Action:** **abandon novelty claims about component competency scaling per se; use as a benchmark/external specimen if an intervention question justifies it.**

### 3. Scale-free Cognition / scaling of goals via homeostasis

**Repository:** `https://github.com/LPioL/scalefreecognition`

**Paper:** Léo Pio-Lopez et al. (2023), *The scaling of goals from cellular to anatomical homeostasis: an evolutionary simulation, experiment and analysis*, Interface Focus 13:20220072. DOI `10.1098/rsfs.2022.0072`.

**What it already does:** explicitly asks how homeostatic goals at a cellular scale relate to larger anatomical homeostasis and uses evolutionary simulation/NCA-style models to investigate scale-up of goals.

**Overlap:** this is a direct warning against claiming novelty for "how local goals/competencies become a whole-level goal." That conceptual territory is explicitly occupied.

**Remaining distinction:** our discovery arm can ask whether a *blinded external analyst* can identify which goal criteria are warranted, whether multiple candidate criteria remain equivalent, and what additional interventions would discriminate them. That is a different inverse problem from demonstrating goal scaling inside a designed model.

**Action:** **reframe away from goal-scaling novelty; cite as central prior art.**

### 4. MinimalDevelopmentalComputation

**Repository:** `https://github.com/santamanicka/MinimalDevelopmentalComputation`

**Paper:** Santosh Manicka & Michael Levin (2022), *Minimal Developmental Computation: A Causal Network Approach to Understand Morphogenetic Pattern Formation*, Entropy 24:107. DOI `10.3390/e24010107`.

**What it already does:** implements a two-level tissue/intracellular-controller architecture with dynamic connectivity, target-pattern maintenance and regeneration, perturbation/cell removal, rescaling/canalization, parameter learning, and causal-network analysis of distributed developmental information.

**Overlap:** very high with our constructive regeneration primitives. It weakens any claim that regeneration, distributed internal state, rescaling, local controllers, or causal distribution of pattern information are novel features of our decomposition.

**Why it is strategically valuable:** it is almost ideal as an **externally authored transparent test system**. We can make pre-registered predictions about which interventions should alter recovery, hide the authored target semantics from a discovery analyst, and test whether our access-contract machinery recovers only warranted criteria.

**Action:** **high-priority external substrate; do not reproduce its phenomena in another bespoke toy.**

### 5. 2D Stress based GA evolution / stress sharing

**Repository:** linked from the software page (`CellularCompetency2D`).

**Paper:** Lakshwin Shreesha & Michael Levin (2024), *Stress sharing as cognitive glue for collective intelligences: A computational model of stress as a coordinator for morphogenesis*, BBRC 731:150396. DOI `10.1016/j.bbrc.2024.150396`.

**What it already does:** models stress as error in a homeostatic loop and shows that sharing stress can improve speed/cohesion toward anatomical targets and extend influence across a collective.

**Most important result for this project:** the paper reports that anatomical goal states could **not** be inferred merely from observing stress states. This is directly relevant to our insistence that internal variables or error-like signals do not automatically reveal semantic goals.

**Action:** **treat as both constructive prior art and a motivating negative result for Goal Discovery.** It supports explicit access contracts and intervention-based identifiability rather than passive reading of an internal "error" variable.

### 6. CompetitionAsCoordination

**Repository:** `https://github.com/psmiley2/CompetitionAsCoordination`

**Paper:** Peter Smiley & Michael Levin (2022), *Competition for finite resources as coordination mechanism for morphogenesis*, BioSystems 221:104762. DOI `10.1016/j.biosystems.2022.104762`.

**What it already does:** evolves virtual embryos whose cells proliferate/differentiate/use resources and finds finite resource reservoirs can become a coordination medium yielding more consistent morphology.

**Overlap:** established example of a seemingly low-level component constraint becoming a whole-level coordination mechanism. This reinforces that our programme should not accumulate more mechanism-demonstration toys unless they test a distinct prediction.

**Action:** **prior art; optional external specimen for resource/reachability hypotheses.**

### 7. Muse

**Repository:** `https://github.com/bhartl/muse`

**Paper family:** Hartl, Risi & Levin (2024), *Evolutionary Implications of Self-Assembling Cybernetic Materials with Collective Problem-Solving Intelligence at Multiple Scales*, Entropy 26(7); Pio-Lopez, Hartl & Levin (2025), *Aging as a Loss of Goal-Directedness*, Advanced Science 12(46).

**What it already does:** provides a hybrid NCA framework for evolving multiscale developmental competency. The aging work explicitly studies completed developmental goals, cellular competency, communication failure, genetic damage, morphology loss, active information storage/transfer entropy, persistent spatial information after organ loss, and regenerative restoration.

**Overlap:** high with our vocabulary of competency, communication, memory, target morphology, maintenance, damage and recovery. These are not safe novelty claims by themselves.

**Operational note:** the repository describes the framework as not fully documented and depends on an actively evolving `mindcraft`/NeurEvo stack. That makes it scientifically interesting but operationally less clean than the canonical Growing NCA or MinimalDevelopmentalComputation for the next immediate experiment.

**Action:** **important prior art; medium-priority external substrate once a concrete hypothesis warrants the integration cost.**

### 8. Cellnition / Regulatory Network Machine (RNM)

**Repository:** `https://github.com/betsee/cellnition`

**Paper:** Alexis Pietak & Michael Levin (2025), *Harnessing the analog computing power of regulatory networks with the Regulatory Network Machine*, iScience 28:112536. DOI `10.1016/j.isci.2025.112536`.

**Why this is the most important newly surfaced neighbor:** RNM treats a regulatory network as a dissipative dynamical system with inputs and stable output states, then constructs Network Finite State Machines mapping input-driven transitions. It explicitly identifies path dependence, irreversible transitions, cycles, unreachable states, and intervention routes to desired equilibria. Cellnition is a Python implementation with tests/CI and published tutorials.

**Overlap:** very high with our action/reachability, intervention-map, persistent-history, and competence-boundary language. We should not claim novelty merely for asking what states are reachable, discovering path-dependent stable changes, or finding intervention sequences that move a system to a desired state.

**Critical distinction:** RNM assumes output states whose relevance to biomedical/technical objectives is **identified externally**. Its job is largely "given meaningful output states and available inputs, map transition logic and persuasive routes." Our Goal Discovery ambition is different only if we really enforce it: **do not supply the semantic goal answer; ask which candidate goal/competence claims are identifiable from permitted observations/interventions, allow equivalence classes, and permit abstention/underdetermination.**

This makes RNM an unusually good comparator. A future benchmark can run the same system in two modes:

- **RNM-like white-box/control mode:** meaningful outputs supplied; map reachability and routes.
- **Goal Discovery mode:** semantic labels withheld; ask what high-level criteria the behavior warrants.

If our system cannot demonstrate a clear epistemic distinction from RNM-like analysis, a major part of the discovery story is redundant.

**Licensing note:** the Cellnition repository states Apache-style open source with a Tufts non-commercial rider; check exact terms before incorporation.

**Action:** **priority comparator/benchmark. Do not duplicate its reachability machinery without a concrete gap.**

### 9. Growing Neural Cellular Automata

**Canonical work:** Mordvintsev, Randazzo, Niklasson & Levin (2020), *Growing Neural Cellular Automata*, Distill. DOI `10.23915/distill.00023`.

**Current role:** already our Experiment 12 external specimen. This audit strengthens rather than weakens that choice: it is externally authored, learned, stochastic, has hidden state, and supplies growth/persistence/regeneration variants.

**Action:** **keep current phase-2 work.** The scientific value is not showing that NCA regenerates; it is making risky predictions about its recovery boundary, latent-state consistency, available actions, and then testing what a blinded analyst can infer.

## Bioelectric and biologically anchored systems: reuse, do not rebuild

### BETSE / BETSEE

**BETSE:** BioElectric Tissue Simulation Engine, Alexis Pietak & Michael Levin (2016), *Exploring Instructive Physiological Signaling with the Bioelectric Tissue Simulation Engine*, Frontiers in Bioengineering and Biotechnology 4:55.

BETSE is a Python multiphysics simulator for 2-D cell collectives including electrodiffusion, electro-osmosis, galvanotaxis, voltage-gated channels, gap junctions, GRNs and biochemical reaction networks. The old GitLab mirror is archived, but current development/releases are on `https://github.com/betsee/betse`; BETSEE is its GUI.

**Implication:** our roadmap should not include creating a general bioelectric tissue engine. BETSE is a plausible established backend when a hypothesis specifically needs bioelectric tissue physics.

**Action:** **candidate phase-3 substrate; wrap, do not replace.**

### BioElectricNetwork

**Repository:** `https://github.com/santamanicka/BioElectricNetwork`

**Paper:** Manicka & Levin (2019), *Modeling somatic computation with non-neural bioelectric networks*, Scientific Reports 9:18612. DOI `10.1038/s41598-019-54859-8`.

Minimal non-neural bioelectric networks are trained/evolved to implement logic and pattern detection and are analyzed with dynamical-systems/information-theory tools.

**Overlap:** non-neural physiological computation, local sensing/integration, collective information processing. **Action:** strong intermediate external substrate if a question needs concrete bioelectric computation without full BETSE complexity.

### ElectricMorphogenesis

**Repository:** linked from the software page.

**Paper:** Manicka & Levin (2025), *Field-mediated bioelectric basis of morphogenetic prepatterning*, Cell Reports Physical Science 6(10):102865. DOI `10.1016/j.xcrp.2025.102865`.

The work uses an intrinsic electric field and negative feedback to enable/shape tissue voltage patterns, reports macroscale field causality/compression and transient-field steering.

**Overlap:** feedback, collective pattern regulation, macroscale intervention targets. **Action:** useful external system for asking whether our decomposition predicts effects of intervention level/scale; not evidence that "feedback enables robust patterning" is novel.

### NeuralPlatePatterning

**Repository:** linked from the software page.

**Paper:** Manicka, Pai & Levin (2023), *Information integration during bioelectric regulation of morphogenesis of the embryonic frog brain*, iScience 26:108398. DOI `10.1016/j.isci.2023.108398`.

A minimal genetic-bioelectric model integrates multicellular voltage patterns into gene-expression decisions and made predictions tested in Xenopus brain development.

**Strategic importance:** one of the best routes from computational toy/external NCA work into a biologically anchored model with experimental validation. **Action:** high-value later substrate after we can formulate a concrete intervention prediction.

### PLIMBO

**PLIMBO:** Planarian Interface for Modelling Body Organization, Pietak & Levin (2019). The tagged v0.0.1 release explicitly describes itself as the first and presumably only stable PLIMBO-specific release, with later work expected under a broader successor.

**Implication:** scientifically relevant as an executable planarian body-axis model, but should be treated as a publication artifact rather than long-term infrastructure.

**Action:** **possible replication/benchmark artifact; not a foundation to build on.**

### Planarian regeneration reverse-engineering software (Lobo & Levin 2015)

**Paper:** Daniel Lobo & Michael Levin (2015), *Inferring regulatory networks from experimental morphological phenotypes: a computational method reverse-engineers planarian regeneration*, PLoS Computational Biology 11:e1004295. DOI `10.1371/journal.pcbi.1004295`.

**What it already does:** formalizes surgical/genetic/pharmacological perturbation → morphology outcomes, evolves candidate regulatory networks, simulates interventions, scores agreement and recovers mechanistic networks capable of explaining the phenotype corpus.

**Why this matters:** it is serious inverse-problem prior art. "Infer something about regeneration from perturbation/behavior" is far too broad a novelty claim.

**Difference we must preserve:** Lobo/Levin infer **underlying regulatory mechanism** from semantically identified morphology/perturbation outcomes. Goal Discovery seeks **warranted high-level goal/competence claims** under a declared access contract without being given the authored semantic answer. A mechanism may remain unknown while a relational goal criterion is supported; conversely, a mechanism model does not by itself establish a unique semantic goal.

**Action:** **central comparator in the discovery survey; candidate ground-truth system for blind analysis.**

### Planform and Limbform

**Planform:** formal graph-encoded planarian regeneration database/tool; the current site reports >1,500 experiments.

**Limbform:** analogous formalized limb-regeneration database; the published resource contains >800 experiments across multiple taxa.

These are strategically important because they offer **real intervention/outcome corpora** rather than another artificial calibration system. They do not themselves solve our goal-identifiability question.

**Action:** **high-priority future data sources** for testing whether the discovery machinery survives contact with heterogeneous published biological evidence.

## Conceptual and inverse-problem neighbors

### MorphoBayes

Kuchling, Friston, Georgiev & Levin (2020), *Morphogenesis as Bayesian Inference*, Physics of Life Reviews 33:88-108. DOI `10.1016/j.plrev.2019.06.001`.

**Implication:** morphogenesis-as-inference/target-control is established conceptual territory. Do not claim novelty for interpreting pattern formation as inference toward desired morphology. **Action:** conceptual prior art.

### MorphoPsy / active inference

Pio-Lopez et al. (2022), *Active Inference, Morphogenesis, and Computational Psychiatry*, Frontiers in Computational Neuroscience 16:988977. DOI `10.3389/fncom.2022.988977`.

**Implication:** cells/collectives as active-inference agents in morphogenesis is already explicit. **Action:** conceptual prior art; useful contrast because our programme need not assume a free-energy/active-inference generative model.

### Equilibrium Flow

Zhang & Levin (2025), *Equilibrium flow: From Snapshots to Dynamics*, arXiv `2509.17990`.

It asks how strongly an observed distribution of static patterns constrains underlying dynamics and finds a solution family influenced by data and inductive bias; it can also inverse-design dynamics preserving target distributions.

**Relevance:** reinforces the general lesson that inverse problems are non-unique. It infers plausible **dynamics**, not semantic candidate goals, but it is an important neighbor for any claim that observations uniquely reveal what a system is doing.

**Action:** **cite in underdetermination/inverse-problem framing.**

### Analyzing causal emergence in networks (`einet`)

Klein & Hoel's tools search for higher-scale coarse-grainings with greater effective information; Hoel & Levin explicitly discuss informative higher scales for prediction/control.

**Overlap:** our original Dynamical Laboratory brief already asks whether macro-representations become more predictive or controllable. That is not novel territory.

**Action:** **reuse as a method where its assumptions fit; do not invent a parallel macro-causality metric.**

### LENIA Umwelt

**Repository:** `https://github.com/jessescool/lenia-umwelt`

**Paper/preprint:** Cool, Hartl, Levin & Petti (2026), *Agnosiophobia in a virtual agent: behavioral and dynamical architecture in Lenia*, arXiv `2605.30708`.

The system introduces regions with unavailable sensory information and studies how Lenia creatures respond; the authors interpret behavior as consistent with avoidance of information occlusion and possibly a more fundamental morphology-preservation objective.

**Why this is unusually useful:** it is a non-developmental, independently authored virtual organism with explicit sensory-information interventions and an interpretive question about what goal best explains behavior.

**Action:** **high-priority Goal Discovery benchmark.** Blind the semantic interpretation and test whether our analyzer supports morphology preservation, mere obstacle avoidance, information-seeking/avoidance, or an equivalence class under the permitted interventions.

### Distributed Agential Chess

Kofman, Campitelli & Levin (2025), *Chess as a Model of Collective Intelligence: Analyzing a Distributed Form of Chess with Piece-wise Agency*, DOI `10.13133/2532-5876/18904`.

**Implication:** distributed agency outside morphogenesis is also active prior art. **Action:** optional cross-domain transfer benchmark if the programme needs to prove substrate-neutrality; not immediate priority.

## Analysis and import tools we should reuse

### Inform / PyInform and CAIM

Inform/PyInform provide established information-theoretic measures for dynamical/collective systems; CAIM applies information analysis to imaging data. These tools are relevant to active information storage, mutual information, transfer entropy and related analyses.

**Guardrail:** an information metric is not by itself a goal, memory, causal role, or competence measure. Use established implementations where the statistic is warranted, but retain the repository's existing discipline of intervention/interpretation checks.

### Boolion

Taylor decomposition/continuous relaxation for Boolean networks; associated with Manicka et al. (2023), *The nonlinearity of regulation in biological networks*, npj Systems Biology and Applications 9:10.

**Action:** method/reference for a concrete regulatory-network experiment, not core infrastructure.

### GABEE

Genetic Algorithm for Bio-Electric Exploration; used to search bioelectric pattern-forming mechanisms. **Action:** prior method for parameter/mechanism search; reuse/compare if we need bioelectric search rather than write a new genetic-search layer.

### SBMLtoODEjax

**Repository:** `https://github.com/flowersteam/sbmltoodejax`

Etcheverry, Levin, Moulin-Frier & Oudeyer (2023), *SBMLtoODEjax: Efficient Simulation and Optimization of Biological Network Models in JAX*, arXiv `2307.08452` / NeurIPS AI for Science workshop.

**Strategic importance:** converts existing SBML ODE models into JAX-compatible Python models for simulation/optimization. Its own motivation is reuse of existing biological network models and intervention-oriented analysis.

**Action:** **important reuse-first import route.** Before implementing a new ODE/GRN specimen, search BioModels/SBML and see whether an existing model can be wrapped through this route. Note the documented feature limitations (e.g. some SBML events/functions/models are unsupported).

### Cellular / Annette / Neato

Generic CA, recurrent-network, and neuroevolution infrastructure. **Action:** infrastructure only; never use our scientific effort to rebuild these abstractions unless an experiment forces a small missing piece.

## Complete screening of the software page

This table records the disposition of every entry visible on the Levin software page so that future agents can see what was actually screened rather than silently rediscovering it.

| Software-page entry | Relevance to this programme | Disposition |
|---|---|---|
| 2D Stress based GA evolution | **Very high** — shared error/stress coordination + goal non-identifiability result | Central prior art / possible benchmark |
| Analyzing causal emergence in networks | High methodological overlap with scale/prediction/control | Reuse method when applicable |
| Annette | Generic RNN infrastructure | Peripheral infrastructure |
| Baccountant | Bacterial colony growth quantification | Peripheral |
| BETSE | **Very high** as existing bioelectric tissue simulator | External substrate; do not rebuild |
| BETSEE | GUI for BETSE | Tooling only |
| BioElectricNetwork | High: non-neural computation/pattern detection | External substrate/prior art |
| Boolion | Regulatory-network analysis method | Method/reference |
| CAIM | Information analysis of imaging data | Method/reference |
| CalculIon | Single-cell bioelectric calculation utility | Utility/reference |
| Cellnition | **Very high**: NFSM state transitions, reachability, path dependence, cycles | Priority comparator/benchmark |
| Cellular | Generic CA library | Infrastructure only |
| Cellular competency evolution model | **Very high direct conceptual overlap** | Central prior art / possible benchmark |
| CompetitionAsCoordination | High: resource-mediated morphogenetic coordination | Prior art / optional substrate |
| Conditional Diffusion Evolution | Evolutionary optimization method | Peripheral unless optimization needed |
| Diffusion Evolution | Evolutionary optimization method | Peripheral unless optimization needed |
| Distributed Agential Chess | High for non-biological distributed agency | Optional cross-domain substrate |
| EDeN | Electroceutical design/intervention database | Useful intervention reference, not core |
| EDeN interface | Interface to EDeN | Peripheral |
| ElectricMorphogenesis | **High**: field-level bioelectric feedback/pattern control | External substrate/prior art |
| Equilibrium Flow | **High inverse-problem relevance**: snapshots → possible dynamics | Conceptual/method comparator |
| FieldSHIFT | Cross-domain hypothesis-generation tool | Peripheral |
| GABEE | Bioelectric mechanism search | Reuse/reference method |
| GenAge Atavism Analysis | Aging/meta-phylostratigraphy analysis | Peripheral to current questions |
| Growing Neural Cellular Automata | **Very high**; current Experiment 12 | Keep as active substrate |
| Inform | Information-theory library | Reuse method |
| Iterated Prisoners Dilemma | Multiscale/self-scaling game model | Optional cross-domain case, not immediate |
| LENIA Umwelt | **Very high for blinded goal inference and sensory interventions** | Priority future benchmark |
| Limbform | **High real intervention/outcome corpus** | Future biological data source |
| Metaphylostratigraphy | Evolutionary-age analysis code | Peripheral |
| MinimalDevelopmentalComputation | **Very high constructive overlap and benchmark value** | Priority external substrate |
| MorphoBayes | High conceptual overlap: Bayesian morphogenesis | Prior art/conceptual comparator |
| MorphoPsy | High conceptual overlap: active-inference morphogenesis | Prior art/conceptual comparator |
| MultiVERSE | Multilayer network embedding | Method only if needed |
| Muse | **Very high multiscale competency/memory/repair overlap** | Prior art + later substrate |
| Neato | NEAT implementation | Infrastructure only |
| Neoblast competition simulation | Collective boundary/competition conceptual model | Peripheral/reference |
| NeuralPlatePatterning | **High biologically validated bioelectric model** | Strong later substrate |
| Planarian regeneration simulation | **Very high inverse-mechanism neighbor** | Comparator + possible ground-truth system |
| Planform | **High biological experiment corpus** | Priority future data source |
| PLIMBO | High planarian mechanistic model, but old publication artifact | Optional benchmark/artifact |
| PyInform | Python information-theory wrapper | Reuse method |
| SBMLtoODEjax | **High strategic reuse value** | Import route for published models |
| Scale-free Cognition | **Very high direct goal-scaling overlap** | Central prior art |
| Somatic cells protect stem cells from lethal environment | Conceptual multiscellularity/prediction-error model | Reference/peripheral |
| Sorting Algorithms as Basal Cognition | **Very high direct overlap with Exp01** | Calibration prior art |

## Revised overlap matrix for our programme

| Proposed/project element | Status after this audit | Consequence |
|---|---|---|
| Local rules yield coherent global morphology | **Established / crowded** | Do not claim novelty |
| Component competency changes whole-level performance/evolution | **Directly established nearby** | Do not claim novelty |
| Cell goals scale into anatomical goals | **Directly established nearby** | Do not claim novelty |
| Bioelectric feedback/communication coordinates tissue pattern | **Deeply established and implemented** | Reuse existing systems |
| Distributed pattern memory / regeneration / restoration | **Strong nearby work** | Treat our toys as calibrations only |
| Reachability/path dependence/intervention maps of dissipative networks | **Strongly occupied by RNM/Cellnition + control theory** | Distinguish discovery semantics or reuse machinery |
| Infer regulatory mechanism from perturbation/morphology data | **Established by Lobo/Levin and broader systems biology** | Not our novelty |
| Infer candidate goals without supplied semantics/optimality and allow underdetermination | **Still potentially distinctive, not established by this audit** | Make identifiability/access contract central |
| Same external system used for white-box causal map and blinded goal/competence inference | **Potentially distinctive methodology** | Turn into a benchmark protocol |
| Predict failure-boundary shifts from experimentally separable capability constraints across independent systems | **Potentially valuable; must be demonstrated** | Pre-register risky predictions and test transfer |
| Formalize exactly what additional intervention resolves rival goal/competence explanations | **Promising niche; must survey beyond Levin** | Develop as discovery criterion |

## Recommended external-specimen queue

Do **not** interpret this as a fixed chronology. Choose the smallest system that tests a risky claim.

1. **Growing NCA — continue now.** Finish location/geometry/timing, latent-consistency, and action/reachability interventions. The point is prediction, not another regeneration demo.
2. **Cellnition/RNM — comparator soon.** Establish exactly where our access-contract/semantic-inference problem begins after RNM-style reachability analysis ends.
3. **MinimalDevelopmentalComputation — next transparent external morphogenesis benchmark.** Test transfer of the same intervention distinctions on a model not authored by us.
4. **LENIA Umwelt — high-value blinded discovery benchmark.** Sensory occlusion and morphology-preservation interpretations give rival candidate goals that can be challenged by interventions.
5. **BioElectricNetwork or NeuralPlatePatterning — biological/bioelectric rung.** Prefer the smallest one that tests a specific prediction.
6. **BETSE — when tissue physics itself matters.** Use as backend; do not make it a generic phase requirement.
7. **Planarian Lobo model / PLIMBO — ground-truth planarian model.** Good for comparing mechanism inference with goal/competence inference.
8. **Planform / Limbform — real literature corpora.** Use when discovery machinery can tolerate heterogeneous experimental evidence.
9. **SBMLtoODEjax + BioModels — general import path.** Search existing models before inventing new dynamical systems.
10. **Muse / Distributed Chess — transfer stress tests** after the core distinction is technically stable.

## A benchmark pattern that could distinguish this project

For an externally authored executable system, maintain three roles:

1. **Oracle:** has source code, authored semantics, target labels and full state.
2. **White-box experimenter:** may inspect/intervene to establish causal dependencies and competence boundaries.
3. **Blind analyst:** receives only the observations/interventions allowed by a declared contract and must report candidate goals/competence dimensions, contradictions, equivalence classes and unresolved alternatives.

Then ask two independent questions:

- **Forward:** did the capability decomposition predict a non-obvious intervention outcome or failure-boundary shift?
- **Inverse:** did the blind analyst infer no more and no less than the evidence licensed?

A strong result is not "the analyst guessed the authored goal." A stronger result is calibrated discrimination: the analyst recovers a relational or coarse goal when that is all behavior identifies, refuses a more specific semantic target when rivals remain equivalent, and names the intervention that would separate them.

Cellnition/RNM, the Lobo planarian system, MinimalDevelopmentalComputation, and LENIA Umwelt provide especially good adversarial cases because each puts pressure on a different part of this benchmark.

## Concrete changes to our scientific posture

### Stop doing

- Do not build another isolated one-purpose morphogenesis toy to demonstrate feedback, memory, sensing, plasticity, communication, or regeneration.
- Do not write a general tissue/bioelectric simulator.
- Do not call local-to-global competency, goal scaling, pattern memory, or morphogenesis-as-problem-solving novel.
- Do not infer semantic goals from an internal stress/error/latent variable merely because it correlates with deviation from an authored target.
- Do not introduce custom reachability/path-dependence vocabulary where control theory or RNM already supplies a clearer concept.
- Do not introduce new information-theory metrics before checking Inform/PyInform and the broader literature.

### Start/continue doing

- Pre-register **risky qualitative predictions** before external-system interventions.
- Separate authored target semantics from experimentally identifiable goal criteria.
- Treat observation/action access as part of the theorem/claim, not an implementation detail.
- Compare rival explanations and report underdetermination explicitly.
- Reuse externally authored models, especially when their original paper already contains a strong interpretation that can be withheld from the blind analyst.
- Search existing biological model repositories/SBML before writing a new mechanistic model.
- Measure transfer: a decomposition earns value only when it predicts outcomes beyond the calibration systems that motivated it.

## Recommended wording for the project question after this audit

A safer umbrella formulation is:

> **What experimentally separable constraints determine the goal-relative competencies and failure boundaries of dynamical systems, and under a declared observation/intervention contract which of those competencies and candidate goals are behaviorally identifiable?**

The constructive half can be operationalized as:

> **Can interventions on information, latent state, memory, coupling and available actions predict non-obvious changes in competence boundaries across independently authored systems?**

The discovery half can be operationalized as:

> **Which candidate goal criteria and competence dimensions are supported, contradicted or left equivalent by the available behavior, and what additional intervention would discriminate the surviving explanations?**

These formulations deliberately avoid claiming that this project discovered collective competence, homeostasis, goal scaling, bioelectric coordination, reachability, or inverse modeling.

## Sources and primary links

Main software catalogue:
- Michael Levin lab, *Tools and Software*: https://drmichaellevin.org/resources/software.html

High-overlap primary papers/software:
- Zhang, Goldstein & Levin, sorting as morphogenesis: DOI `10.1177/10597123241269740`
- Shreesha & Levin, Cellular Competency: DOI `10.3390/e25010131`; https://github.com/lksshw/CellularCompetency
- Pio-Lopez et al., scaling of goals: DOI `10.1098/rsfs.2022.0072`; https://github.com/LPioL/scalefreecognition
- Manicka & Levin, Minimal Developmental Computation: DOI `10.3390/e24010107`; https://github.com/santamanicka/MinimalDevelopmentalComputation
- Shreesha & Levin, stress sharing: DOI `10.1016/j.bbrc.2024.150396`
- Smiley & Levin, CompetitionAsCoordination: DOI `10.1016/j.biosystems.2022.104762`; https://github.com/psmiley2/CompetitionAsCoordination
- Pietak & Levin, Regulatory Network Machine: DOI `10.1016/j.isci.2025.112536`; https://github.com/betsee/cellnition
- Mordvintsev et al., Growing NCA: DOI `10.23915/distill.00023`
- Pio-Lopez, Hartl & Levin, Aging as Loss of Goal-Directedness: Advanced Science (2025); https://github.com/bhartl/muse
- Manicka & Levin, BioElectricNetwork: DOI `10.1038/s41598-019-54859-8`; https://github.com/santamanicka/BioElectricNetwork
- Pietak & Levin, BETSE: Frontiers in Bioengineering and Biotechnology 4:55; https://github.com/betsee/betse
- Manicka & Levin, ElectricMorphogenesis: DOI `10.1016/j.xcrp.2025.102865`
- Manicka, Pai & Levin, NeuralPlatePatterning: DOI `10.1016/j.isci.2023.108398`
- Lobo & Levin, planarian regulatory-network inference: DOI `10.1371/journal.pcbi.1004295`
- Planform: https://lobolab.umbc.edu/planform/
- Limbform: https://lobolab.umbc.edu/limbform/
- Kuchling et al., Morphogenesis as Bayesian Inference: DOI `10.1016/j.plrev.2019.06.001`
- Pio-Lopez et al., Active Inference and Morphogenesis: DOI `10.3389/fncom.2022.988977`
- Zhang & Levin, Equilibrium Flow: arXiv `2509.17990`
- Cool et al., LENIA Umwelt / Agnosiophobia: arXiv `2605.30708`; https://github.com/jessescool/lenia-umwelt
- Etcheverry et al., SBMLtoODEjax: arXiv `2307.08452`; https://github.com/flowersteam/sbmltoodejax

## Bottom line

The Levin software ecosystem does **not** make the whole repository redundant. It does make a large fraction of the constructive *demonstration space* redundant.

That is useful information. The repository's own original reuse-first brief already said that the durable object should be trajectories/evidence and that published executable worlds should be adapted rather than rebuilt. This survey strengthens that policy.

The project now has a sharper burden of proof: **earn value by making calibrated, intervention-grounded predictions and identifiability claims across systems whose competency phenomena already exist independently of us.**
