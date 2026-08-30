# P3-002 Flocking representation discrimination — results

## Decision

**No-go. Stop Flocking and do not repair the candidate after inspection.** All
five integrity gates passed on 32 complete new trajectories. Neither frozen
candidate representation passed.

The quarter rotation produced the required local shock in all eight seeds.
Late local disagreement returned within 2 degrees of baseline in six seeds and
full interaction beat the vision-off polarization null in all eight. However,
late polarization reached 90% of baseline in only four seeds, below the frozen
six-seed gate.

The absolute-heading hypothesis failed decisively. Whole-flock rotation created
the intended roughly 90-degree displacement in all seeds; late heading errors
remained between 82.6 and 106.6 degrees, and none closed half of its error.

## What was learned

Flocking actively restores local alignment, but the tested global organization
is not stable enough across seeds to define the promoted alignment-plus-
polarization manifold. The system also shows no evidence of defending its prior
absolute heading. The standard model is a useful visual example of emergent
coordination, but it did not earn a goal-representation confirmation batch.

This no-go is not a visualization failure. It is the consequence of separating
local, global-strength, and absolute-direction observables before using the word
“recovery.”

## Next decision

Follow the frozen fallback to the installed NetLogo Fireflies model. It adds
explicit internal phase state and a crisp population synchrony observable while
retaining local interaction, movement, standard visualization, and an
unmodified off-the-shelf generator.

Artifacts are in `results/p3-002-flocking-representation-discrimination/`.
