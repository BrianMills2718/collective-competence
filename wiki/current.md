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

The regeneration sequence now separates several information requirements instead of treating “regeneration” as one scalar ability. Experiment 06 supplies external positional information; Experiment 07 shows that a tissue-generated field can restore total size without position; Experiment 08 adds one local sealed/unsealed state per boundary and composes the two.

For unilateral end damage, endogenous size plus boundary integrity is sufficient in the declared toy: exact position and size return in every tested trial, and the repaired boundary reseals for later damage. Ablating either channel separates their jobs cleanly—size without boundary memory loses location; boundary memory without a changing size signal cannot know when to grow or stop.

The remaining failure is now specific. Under simultaneous bilateral damage, both boundaries say “wounded” and the inhibitor says the total amount missing, but neither says how that deficit should be apportioned between the two sides. Size returns; anatomy need not.

## Next action

**Do not add another mechanism until we can state the minimal bilateral-allocation question sharply.**

The next constructive experiment should ask what additional information is sufficient to divide a known total repair deficit across multiple wounded boundaries **without** restoring a full site-by-site coordinate map. Candidate ideas include side-specific accumulated deficit, persistent boundary-specific history, or a locally propagating wound signal, but none is yet preferred.

The questions to resolve before implementation are:

1. What must each wounded boundary know beyond “I am wounded” and “the tissue is undersized”?
2. Can a purely local history of growth or injury encode the required allocation, or is some longer-range comparison unavoidable?
3. What is the weakest cue that solves asymmetric bilateral damage as well as symmetric damage?
4. Does that cue also handle an internal deletion, or does internal repair require a qualitatively different representation?
5. Which ablation would distinguish true per-wound allocation information from a hidden coordinate map?

This is a scientific design choice, not an apparatus gap. Keep the current code unchanged until that question is clearer.

## Working rules

- Optimize for **different phenomena learned per unit effort**.
- Prefer minimal, inspectable biological analogues over realism for its own sake.
- Construction and mechanism first; discovery analysis second.
- Keep pattern, size, location, per-wound allocation, function, and exact microstate distinct.
- State which information is external, tissue-generated, inherited, local, shared, or historical.
- Treat successful composition as a statement about specific challenges, not a scalar competence ranking.
- Add apparatus only when a concrete experiment requires it.
- Negative results and information/feasibility boundaries count as progress.

## Secondary follow-ups

The size and boundary-memory cases could support later blind-analysis tests, but their white-box information structure is currently more scientifically useful than another classifier result. The immediate value is to understand the bilateral allocation gap before adding more discovery machinery or biological detail.
