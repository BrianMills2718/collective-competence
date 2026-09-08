---
doc-role: current-working-status
authority: working-priority-summary
lifecycle: active
sources:
  - questions.md
  - findings.md
  - ../experiments/07-endogenous-size-control/README.md
---
# Current work

[Wiki home](index.md) · [Questions](questions.md) · [Findings](findings.md) · [Laboratory](laboratory.md)

This is the only hot page that owns **current priority and next action**.

## Where we are

Structural regeneration has now exposed two different information problems. Experiment 06 shows that local occupancy alone cannot distinguish a wound edge from a normal boundary; an external positional code supplies “where.” Experiment 07 moves the stopping cue into the tissue: a self-produced inhibitor supplies “how much.”

The endogenous size controller is genuinely causal in the declared toy. Cell loss lowers the signal and reopens growth; clamping the pre-loss signal prevents regrowth; eliminating secretion removes the stop. It restores size 24 after every declared loss/excess challenge, but exact position rapidly disappears because either edge can act.

The noise sweep adds a capacity boundary: short-range signals make adjacent sizes nearly indistinguishable at the edge, so fixed sensing noise destabilizes size control. These results are still engineered analogues, but they now separate size, position, and pattern as experimentally different competencies.

## Next action

**Find the weakest additional cue that lets endogenous size control recover position after one-sided damage.**

Do not solve this by restoring a complete external coordinate map. The next experiment should ask how little extra information is sufficient to tell the two tissue edges apart or identify which boundary has been damaged, while the endogenous inhibitor continues to determine how much total structure should exist.

Candidate mechanisms worth comparing before choosing one include a persistent left/right polarity carried by cells, boundary-specific organizer identity, or a wound-history marker. The mechanism should be chosen for the question it makes testable, not because it is easy to code.

The first questions are:

1. Can “how much” and “where” be composed so one-sided amputation restores both size and position?
2. What is the minimal information needed to break the left/right ambiguity?
3. Does the added cue generalize to both left and right amputations without encoding every target site?
4. What happens when size information is intact but polarity/location information is removed, and vice versa?
5. Does combining the capabilities create new failure modes under internal lesions, noise, or organizer damage?

## Working rules

- Optimize for **different phenomena learned per unit effort**.
- Prefer minimal, inspectable biological analogues over realism for its own sake.
- Construction and mechanism first; discovery analysis second.
- Keep size, position, pattern, function, and exact microstate restoration separate.
- State clearly which information is external, tissue-generated, inherited, or locally sensed.
- Do not call a composed controller “more competent”; report which challenges each capability actually solves.
- Add apparatus only when a concrete experiment requires it.
- Negative results and information/feasibility boundaries count as progress.

## Secondary follow-ups

A blind Goal Discovery pass on the size controller may eventually be useful for asking whether size is inferred as a family-level criterion despite positional variation, but that is not the immediate scientific front. The more valuable next result is constructive: determine what extra information is actually required to compose size and position recovery without reintroducing a full target map.
