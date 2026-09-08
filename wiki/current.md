---
doc-role: current-working-status
authority: working-priority-summary
lifecycle: active
sources:
  - questions.md
  - findings.md
  - ../experiments/08-boundary-memory/README.md
---
# Current work

[Wiki home](index.md) · [Questions](questions.md) · [Findings](findings.md) · [Laboratory](laboratory.md)

This is the only hot page that owns **current priority and next action**.

## Where we are

The regeneration sequence now separates several information requirements instead of treating “regeneration” as one scalar ability. Experiment 06 supplies external positional information; Experiment 07 shows that a tissue-generated field can restore total size; Experiment 08 adds a local sealed/unsealed state at each boundary and composes wound identity with the endogenous size cue.

For unilateral end damage, size plus boundary integrity restores the pre-damage interval in every declared trial, and the repaired boundary reseals for later damage. Ablating either channel separates their jobs cleanly: the size signal supplies whether/how long structural change is needed, while the boundary state marks which exposed edge may act.

The bilateral trials initially looked like a further “allocation” failure: size returned, but births were not always divided between the two edges in the same proportions as the cells previously removed. On review, that interpretation over-constrained the goal. This tissue is internally homogeneous and contiguous, so **every 24-cell interval is the same modeled morphology up to translation**. The bilateral controller restores that translation-equivalence class in every declared trial. What it sometimes fails to recover is only the historical arena position.

That correction is important. A missing allocation statistic is scientifically meaningful only after the target criterion distinguishes the alternative allocations.

## Next action

**Make multi-wound allocation matter intrinsically before adding another repair mechanism.**

Do not add side-specific deficit memory merely to recover a privileged historical translation. First construct the smallest morphology in which a wrong left/right repair split changes an internal relation or function even after allowing translation.

The leading minimal candidate is a **two-compartment one-dimensional tissue**: left and right regions have distinct identities and declared target amounts/proportions. Bilateral end damage then removes different compartment types. Restoring total size with the wrong birth allocation changes composition, so the failure is no longer removable by translating the whole tissue.

Before implementation, keep the question explicit:

1. What is the weakest non-translation-equivalent morphology that makes per-wound allocation observable as a real criterion failure?
2. Does the existing size + boundary-memory controller restore total size while systematically failing compartment amount/proportion under asymmetric bilateral damage?
3. Once that failure is demonstrated, what additional information is actually necessary—one composition/asymmetry statistic, compartment-specific local signals, inherited positional state, or something else?
4. Can the needed information be generated and maintained by the tissue, rather than handed in as the missing answer?
5. Which ablation distinguishes a genuine composition/allocation cue from a disguised absolute coordinate map?

A useful analytic constraint is already clear: if total missing amount is `D` and exact historical left/right allocation is required, then `D` alone leaves multiple possible splits. An extra independent allocation statistic is necessary. But a real-valued “one scalar” is not automatically minimal information—it can encode arbitrarily many bits. Minimality must be stated relative to the finite challenge set and the precision available.

## Working rules

- Optimize for **different phenomena learned per unit effort**.
- Prefer minimal, inspectable biological analogues over realism for its own sake.
- Construction and mechanism first; discovery analysis second.
- Keep pattern, size, location, composition, per-wound allocation, function, and exact microstate distinct.
- Treat translations or other symmetries as equivalent unless the experiment explicitly supplies a reason not to.
- State which information is external, tissue-generated, inherited, local, shared, or historical.
- Treat successful composition as a statement about specific challenges, not a scalar competence ranking.
- Do not simulate a claim whose decisive content is already derivable on paper.
- Add apparatus only when a concrete experiment requires it.
- Negative results, corrections, and information/feasibility boundaries count as progress.

## Secondary follow-ups

If absolute location relative to an environment becomes biologically or functionally meaningful, the bilateral historical-position problem can be reopened with that external frame declared. The present priority is stronger: create an internally distinguishable morphology so that allocation has consequences independent of arena coordinates.
