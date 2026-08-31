---
doc-role: experiment-protocol
authority: experiment
lifecycle: frozen
---
# P14 — blind ant–field relational proposal and prospective challenge

[Wiki](../../../roadmap/README.md) · [Current plan](../plans/current_research_plan.md)

## Decision and claim boundary

Can a modest observation-only grammar propose a relation among moving agents,
an opaque internal mode, and a shared environmental field in the installed,
unmodified NetLogo Ants system? Can a prospective field intervention distinguish
that relation from kinematic persistence and common radial geometry?

This is the first interacting-system calibration after P13. It does not ask
whether ants collect food well and it does not supply food, nest, source,
carrying, collection, or authored-goal variables to the learner. The coordinate
frame, persistent opaque identity, one opaque binary mode, position, heading,
and three local chemical samples are supplied. The linear family grammar,
radial-band menu, intervention family, thresholds, and controls are also
supplied. A passing result is not an unexpected goal, competency, agency, or
general discovery demonstration.

Reuse the installed NetLogo 7.0.4 Models Library `Ants.nlogox` unchanged.
Reuse the P13 candidate -> frozen forecast -> outcome lineage and the P7 Ants
BehaviorSpace adapter. Do not add a simulator, generic representation system,
adaptive selector, task-performance target, or dashboard.

## Observation contract

Each observed tick contains only:

- opaque run ID and tick;
- opaque persistent agent ID and opaque binary mode;
- agent x/y and heading;
- chemical at the occupied patch and at one patch ahead, right45 degrees, and
  left45 degrees.

The learner rejects any extra field. NetLogo color is converted to an unlabeled
mode bit at export; its meaning is evaluator-only. Food, nest scent, patch food,
food-source number, source code, intervention arm, random state, collection,
and future observations never cross the learner boundary.

For each transition, predict the next displacement unit vector. Derive current
heading vector, normalized vector toward coordinate origin, and a normalized
local chemical vector from the three oriented samples. World-boundary or absent
next observations are excluded by a frozen integrity rule, not imputed.

## Frozen proposal grammar

Discovery uses seeds7101–7108, population125, the standard diffusion50 and
evaporation10 settings, and ticks251–300 from otherwise standard runs. Leave one
whole seed out at a time. Fit fixed-alpha ridge regressions (`alpha=1e-6`) for
two outputs (next dx/dy), standardizing within each training fold:

1. `persistence`: current heading vector;
2. `radial_geometry`: persistence plus vector toward origin;
3. `shared_field`: persistence plus local chemical vector;
4. `role_relational`: persistence, radial and field vectors, plus opaque-mode
   interactions with radial and field vectors.

Score mean cosine loss after normalizing predictions. Select
`role_relational` only if it:

- improves mean held-seed loss by at least15% over persistence;
- improves mean loss by at least5% over both single-relation families; and
- beats each other family on at least6/8 held-out seeds.

Otherwise abstain and stop before intervention generation. Do not add a family,
change the feature grammar, inspect task variables, or weaken gates.

Refit the selected family on all discovery transitions. For each mode, measure
the median predicted-direction change when its field vector is replaced by zero
while all other inputs remain fixed. The mode with the larger effect is the
candidate field-coupled role. Require its median field effect >=0.03 cosine
distance and >=1.5 times the other mode; otherwise classify the result as a
non-specific supplied-mode restatement and stop.

Choose an intervention band only from `[5,10)`, `[10,15)`, `[15,20)`, and
`[20,25)`. For each band, compute the candidate's median field effect over
field-coupled-role discovery transitions starting in that band. Require at
least100 transitions from at least6 seeds. Select the greatest median effect,
breaking ties toward the inner band. If no band qualifies, abstain. Candidate,
fold scores, selected role/band, raw discovery observations, source revision,
and hashes must be committed before forecasts or untouched outcomes.

## Prospective intervention and frozen predictions

Evaluation uses untouched seeds7201–7208 and matched standard-model arms through
tick330. Both arms are identical through tick300. At tick300, after the standard
step, the intervention arm sets chemical to zero in the selected band. After
each standard step through tick310 it zeros the same band again, so the recorded
post-operation state—not a later rebuilt field—is the integrity boundary. The
sham arm makes no field change. No model procedure is edited.

Before executing either full evaluation arm, freeze these predictions:

1. the selected field-coupled role will show greater matched same-ID heading
   divergence between erase and sham than the other role during ticks301–305;
2. among agents of the selected role that started inside the band at tick300,
   median paired heading divergence will reach at least20 degrees in at least
   6/8 seeds by tick305;
3. the selected-role median divergence advantage over the other role will be
   at least10 degrees in at least6/8 seeds;
4. positions, headings, modes, and population are exactly paired through
   tick300, and recorded band chemical is at least95% lower than matched sham
   at every tick300–310 with nonzero sham chemical.

Require at least three selected-role and three other-role agents in the frozen
tick300 band cohort for at least6/8 seeds. A cohort or intervention-integrity
failure invalidates the experiment; it is not negative causal evidence.

## Alternatives and stopping rules

- **Kinematic persistence:** motion remains predictable without environmental
  relation; selected relational family must beat it prospectively in discovery.
- **Common radial geometry / measurement artifact:** both field and motion may
  covary with radius; matched field erasure should not selectively separate
  roles under this explanation.
- **Interaction mechanism / invariant relation:** one opaque role's motion is
  conditionally coupled to the shared field; selective matched divergence after
  field erasure supports this bounded interpretation.
- **Competency / defended goal:** not established by relation recovery or field
  following. No task outcome is observed, and no compensation or resource-bound
  success criterion is tested.

Stop immediately if the candidate fails selection, merely reproduces the opaque
mode without a distinct field contribution, lacks a qualifying intervention
band, has no discriminating prediction, requires model edits or new generic
infrastructure, or fails integrity. Preserve abstention and negative results.
Do not rerun with more seeds, different bands, new features, post-outcome
thresholds, or an authored food-performance target.

## Inspectable result

After evidence only, produce the smallest useful readout: candidate-family
held-seed losses, learned per-mode field effects and selected band, paired
heading-divergence trajectories by role, integrity gates, and a terse claim
boundary. Reuse existing plotting components; no new cockpit tab is required.

