---
doc-role: current-working-status
authority: working-priority-summary
lifecycle: active
sources:
  - questions.md
  - findings.md
  - reference/research-landscape.md
  - ../experiments/11-learned-composition-memory/README.md
---
# Current work

[Wiki home](index.md) · [Questions](questions.md) · [Findings](findings.md) · [Laboratory](laboratory.md)

This is the only hot page that owns **current priority and next action**.

## Where we are

The project has completed enough primitive/calibration work to change phases. Small systems have separated several quantities that are easy to conflate: desired-state information, observation of current state, maintenance/recovery, compensation, retained history, plasticity/reachability, reporter integrity, and memory. The latest analysis also gives an explicit observability limit: after a primary reporter is known to be broken, exact repair requires some independent information about current amount or lost amount.

Those distinctions are useful, but most of the individual ingredients have mature neighboring literatures in control, fault diagnosis, self-stabilization, inverse objective inference, and regenerative biology. The scientific burden has therefore moved from **inventing another clean toy** to testing whether the decomposition continues to explain and predict behavior as system complexity increases.

This is also the original project strategy. The retained Robinson-Crusoe brief called for one reusable experimental discipline, progressively richer systems, thin slices, and maximum reuse of existing tooling. The custom `Lattice` remains useful apparatus for the systems that naturally fit it, but the more important reusable substrate is the Dynamical Laboratory contract: reproducible trajectories, declared observations, interventions, matched comparisons, evidence custody, and separable black-box/white-box analysis.

## Next action

**Adopt the published Growing Neural Cellular Automata system as the first phase-2 external specimen.**

Do not rewrite NCA inside the custom lattice and do not begin with a new Goal Discovery analyzer. First reproduce a published trained local-rule system and wrap it as an external laboratory backend.

The canonical starting point is Mordvintsev, Randazzo, Niklasson & Levin, *Growing Neural Cellular Automata* (Distill, 2020, DOI `10.23915/distill.00023`). Its cells have vector-valued local state, a shared learned local update rule, asynchronous/stochastic updates, development from a seed, persistence, and damage/regeneration. A 2026 review identifies NCA as a current model class for multiscale biological self-organization and highlights interpretability and scaling as major open problems.

### Phase-2 gate 1 — faithful reproduction

Before making project-specific claims:

1. pin the upstream implementation/model provenance and license;
2. reproduce at least one published growth/persistence/regeneration behavior from an upstream or independently validated implementation;
3. preserve the upstream model rather than retraining it to make our preferred interpretation easier;
4. record enough state/seed/update metadata to make intervention arms reproducible;
5. expose observations/interventions through a thin adapter rather than converting the NCA into `Lattice` semantics.

### Phase-2 gate 2 — preregistered mechanistic questions

Only after reproduction, test a small set of predictions derived from the existing programme:

1. **Attainment is not maintenance.** Growing, persistent, and regeneration-trained variants should be compared under delayed damage, not only endpoint similarity.
2. **Repair has a basin/boundary.** Vary lesion size, geometry, location, timing, and update interruption to find where recovery ceases or changes qualitatively.
3. **Current-state information is distributed.** Visible morphology and hidden channels should be perturbed separately where the model permits it; recovery differences can test whether latent cell state carries load-bearing repair information.
4. **Desired state and current-state evidence are distinct.** The learned update rule/weights encode training history and target-related structure, while the evolving cell state carries current information. Do not assume either is a literal explicit goal representation.
5. **Action repertoire matters.** Local update disabling, spatially restricted updates, or channel-specific interventions should be used only when they test whether a failure is informational versus unreachable under the remaining local dynamics.
6. **Fault diagnosis matters only when observation channels can fail independently.** Do not manufacture a second reporter unless its failure mode is actually distinct.

These are hypotheses and intervention targets, not conclusions.

### Phase-2 gate 3 — discovery only after construction

After the white-box NCA behavior and intervention boundaries are understood, create an opaque observation/intervention package and ask what candidate morphology/maintenance criterion and competence profile can be inferred without the training target, semantic channel names, or implementation. Existing discovery machinery should be reused first; extend it only for a concrete failure.

## What not to do next

- Do not create Experiment 12 as another hand-authored one-purpose scalar/1-D controller.
- Do not generalize `Lattice` to 2-D neural state merely to preserve one-container purity.
- Do not retrain an NCA until an upstream pretrained/reproducible baseline has been characterized.
- Do not call familiar observability, controllability, fault-diagnosis, or self-stabilization results novel.
- Do not treat NCA as biological ground truth; it is the **mesoscopic externally specified rung** between our transparent primitives and richer multicellular/biological models.

## Working rules

- Optimize for **prediction/explanation gained per unit effort**, not specimen count.
- Increase complexity by composing/reusing mechanisms and external systems, not by adding infrastructure preemptively.
- Keep desired-state memory, current-state observation, action repertoire, plasticity, and fault diagnosis distinct until evidence links them.
- Treat symmetries/equivalence classes as part of the criterion definition.
- Use analytic arguments when a result is derivable; use experiments where trajectories/interactions make the answer genuinely nontrivial.
- Preserve negative results and surprises; they are especially valuable in systems we did not design.
- Keep the hot wiki compact; exact upstream provenance and phase-2 evidence belong with the native external-specimen record.

## Secondary direction

If NCA proves too opaque or operationally brittle for clean intervention work, the next external rung should be an established multicellular platform/model rather than retreating automatically to another hand-authored toy. Morpheus and PhysiCell are candidate platforms; planarian regeneration remains a strong medium-term biological anchor. See [research landscape](reference/research-landscape.md).
