---
doc-role: current-working-status
authority: working-priority-summary
lifecycle: active
sources:
  - questions.md
  - findings.md
  - ../experiments/10-endogenous-composition/README.md
---
# Current work

[Wiki home](index.md) · [Questions](questions.md) · [Findings](findings.md) · [Laboratory](laboratory.md)

This is the only hot page that owns **current priority and next action**.

## Where we are

The regeneration sequence now separates several requirements that were easy to conflate. Experiments 06–08 separated external position, endogenous amount/size, and wound-boundary state, then corrected an over-strong exact-position criterion. Experiment 09 introduced a genuinely non-translation-equivalent two-compartment target, `A^8 B^16`, and showed that perfect goal information is not sufficient when the surviving action repertoire cannot recreate an extinct lineage.

Experiment 10 replaces the composition oracle with **tissue-generated, type-specific inhibitor signals**. With both lineages still represented, those endogenous signals restore all **6/6** declared partial composition challenges. Complete loss of one lineage still defeats lineage-conserving repair (**0/4**), while daughter-fate plasticity restores **4/4**.

The causal signal controls expose a new information problem. Clamping the A signal at its healthy target value after A loss suppresses regrowth completely. Eliminating A secretion does the opposite: the controller sees a permanent deficit and grows for the entire fixed window, reaching A=44 after partial loss and A=40 after complete A extinction in the plastic arm. Thus the self-produced signal is both useful and fallible: **source failure can masquerade as extreme tissue loss.**

## Next action

**Determine the weakest way for composition information to survive outside the lineage it describes.**

Do not add another signal reflexively. The next constructive question is whether a missing compartment can be represented redundantly in surviving tissue or a persistent extracellular state, so complete lineage loss does not erase both the structure and the only source of evidence about it.

The mechanism should also address the reporter-failure ambiguity. A controller that treats “signal absent” as proof that a compartment is absent will overreact when secretion itself fails. Any proposed redundancy should therefore be tested against both real lineage loss and signal-source ablation.

Questions to resolve before implementation:

1. What is the smallest information retained outside A that distinguishes “A is gone” from “A is present but its reporter is broken”?
2. Can B cells, a boundary state, or a slow extracellular trace preserve useful A information without storing a complete target map?
3. How long must such memory persist to support regeneration after full lineage extinction?
4. Does redundant information help if plasticity is absent, or does the generative capability boundary remain exactly where Experiment 09 put it?
5. Which ablation cleanly separates redundant memory from an additional hidden composition oracle?

## Working rules

- Optimize for **different phenomena learned per unit effort**.
- Prefer minimal, inspectable biological analogues over realism for its own sake.
- Construction and mechanism first; discovery analysis second.
- Keep pattern, size, location, composition, information, reporter integrity, memory, plasticity, and exact microstate distinct.
- Treat translations or other symmetries as equivalent unless the experiment explicitly supplies a reason not to.
- State which information is external, tissue-generated, inherited, local, shared, historical, persistent, or supplied by oracle.
- Treat successful composition as a statement about specific challenges, not a scalar competence ranking.
- Do not simulate a claim whose decisive content is already derivable on paper; use analytic controls where possible.
- Add apparatus only when a concrete experiment requires it.
- Negative results, corrections, and information/feasibility boundaries count as progress.

## Secondary follow-ups

Noise/range effects on the two compartment signals can be measured later if they become load-bearing; Experiment 07 already establishes the generic adjacent-count discrimination issue. The immediate scientific value is the source-failure/extinction ambiguity, not another signal-resolution sweep.
