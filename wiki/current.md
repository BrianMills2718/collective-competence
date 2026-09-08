---
doc-role: current-working-status
authority: working-priority-summary
lifecycle: active
sources:
  - questions.md
  - findings.md
  - ../experiments/09-composition-lineage/README.md
---
# Current work

[Wiki home](index.md) · [Questions](questions.md) · [Findings](findings.md) · [Laboratory](laboratory.md)

This is the only hot page that owns **current priority and next action**.

## Where we are

The regeneration sequence now separates several requirements that were easy to conflate. Experiments 06–08 separated external position, endogenous amount/size, and wound-boundary state. A correction to Experiment 08 also removed an artificial target: in a homogeneous interval, different size-24 translations are the same modeled morphology unless an external frame is declared.

Experiment 09 therefore makes morphology intrinsically non-translation-equivalent by giving the tissue two ordered compartments, `A^8 B^16`. It then uses perfect A/B target counts as an **oracle control**, not a proposed biological mechanism, so information can be separated from generative capability.

With both lineages still present, perfect composition information plus lineage-preserving local growth restores all **6/6** declared partial-loss cases. When one compartment is completely removed, the same controller repairs **0/4** declared extinction cases even though it knows exactly which type is missing. Adding daughter-fate plasticity repairs **4/4**. Removing every cell still prevents repair because the system has no surviving parent from which local proliferation can start.

So the current result is sharper than “another allocation signal is needed”: **goal information and reachable action repertoire are separate requirements.** A system can know what state would satisfy the criterion and still be unable to generate it.

## Next action

**Replace the composition oracle with the smallest tissue-generated information channel that can support composition repair.**

Do not add a blind-analysis layer to the oracle toy. The next constructive experiment should ask how surviving cells could estimate compartment amount/proportion themselves, while preserving the lineage-extinction challenge as a capability control.

A leading candidate is a compartment-specific endogenous signal analogous to Experiment 07's size inhibitor: A and B cells contribute distinguishable local/global signals, and wounded boundaries use those signals to determine whether their compartment is deficient. The mechanism should be kept minimal enough to expose whether it actually carries composition information rather than hiding target counts in controller code.

The questions to resolve are:

1. Can tissue-generated signals restore A/B composition after partial asymmetric bilateral damage without an external coordinate map?
2. Is one independent composition statistic, together with total-size information, sufficient for the declared two-compartment target?
3. What happens as signal range/noise makes adjacent compartment amounts hard to distinguish?
4. When a lineage is extinct, does information remain available, and what additional plasticity or persistent source is required to recreate the missing type?
5. Can the same information support repair after internal compartment damage, or only end amputation?

## Working rules

- Optimize for **different phenomena learned per unit effort**.
- Prefer minimal, inspectable biological analogues over realism for its own sake.
- Construction and mechanism first; discovery analysis second.
- Keep pattern, size, location, composition, information, plasticity, and exact microstate distinct.
- Treat translations or other symmetries as equivalent unless the experiment explicitly supplies a reason not to.
- State which information is external, tissue-generated, inherited, local, shared, historical, or supplied by oracle.
- Treat successful composition as a statement about specific challenges, not a scalar competence ranking.
- Do not simulate a claim whose decisive content is already derivable on paper; use analytic controls where possible.
- Add apparatus only when a concrete experiment requires it.
- Negative results, corrections, and information/feasibility boundaries count as progress.

## Secondary follow-ups

The historical-position problem from Experiment 08 remains available if a future specimen introduces a meaningful external landmark. Experiment 09's oracle composition controller should remain a calibration/control surface rather than becoming a benchmark; its role is to make the next endogenous-information question clean.
