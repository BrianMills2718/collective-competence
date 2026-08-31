# P9 sorting UI — blind goal-discovery calibration

**Status:** P9-C1 complete; checkpoint passed on 2026-08-30.  
**Target:** one runnable desktop UI version and a bounded checkpoint audit.  
**Scientific status:** calibration against sealed known ground truth; no new
goal-discovery claim is authorized.

## Why this version exists

P8 proved that the sorting system can be configured, replayed, branched,
perturbed, and viewed through synchronized representations. User review then
exposed two deeper problems:

1. the interface still assumes and narrates the sorting goal instead of testing
   whether a discovery process could recover it; and
2. “state damage versus mechanism damage” is too narrow and makes the world,
   system boundary, environment, and intervention target implicit.

P9 turns sorting into a blind calibration case and makes those modeling choices
explicit without claiming that the current substrate already represents a
general dynamic environment.

## First-principles model

The UI must distinguish:

- **world:** the coupled modeled situation;
- **focal system:** the cells and their internal state/capabilities;
- **environment/context:** the one-dimensional slots and activation scheduler;
- **boundary:** the investigator's declared inside/outside split;
- **observation contract:** what goal discovery may inspect;
- **competency hypothesis:** an outcome or relationship the focal system may
  reliably achieve over a stated challenge family; and
- **intervention:** a typed change to world state, rules, structure, interface,
  environment, demand, or noise.

The current sorting world has a static line geometry and a scheduler. It does
not have an independently evolving reciprocal environment. P9 may change the
scheduler at a branch boundary as a real environment-dynamics intervention,
but must state this limitation prominently.

## Deliverables

### P9-V0 — declared world and boundary

- Add a compact world-declaration region before the experiment controls.
- Name what is inside the focal system, outside in the environment/context,
  crossing the boundary, and available to the observer.
- Label the current environment support as limited rather than general.
- Change cell cards from an unlabeled number to explicit `VALUE n`, `ID n`, and
  capability text.

### P9-V1 — typed intervention composer

- Rename damage to intervention.
- Support three real intervention families:
  - internal state: block swap;
  - capability/mechanism: moveable or immovable freeze; and
  - environment dynamics: change activation schedule at the branch.
- Display target, operation, scope, timing, persistence, and matched
  counterfactual.
- Show structural, interface, demand/context, and noise interventions as
  currently unsupported—not as fake controls.
- Preserve exact common-past and deterministic replay guarantees.

### P9-V2 — blind goal-discovery calibration

- Default to a sealed discovery mode in which authored goal and rule internals
  are excluded from the discovery observation contract.
- Hide rule and internal-target fields from cell tooltips/tables until the
  ground-truth reveal is enabled.
- Generate a sourced candidate ledger from allowed trajectory observations:
  global-order, local-boundary, final-position, ordered-prefix, value-preserving,
  and active-capability hypotheses.
- Distinguish candidate goal, progress representation, subgoal/mechanism,
  invariant, and competency interpretations.
- Show supporting observations, counterevidence, and the next intervention
  needed to distinguish observationally equivalent hypotheses.
- Reveal the authored sorting target only in a clearly separated calibration
  panel; explain which candidates were the goal, proxies, mechanisms,
  invariants, or capabilities.

### P9-C1 — checkpoint

Audit:

- scientific and model fidelity;
- truthfulness of the declared boundary/environment;
- deterministic replay and intervention isolation;
- whether the blind mode actually withholds sealed fields;
- whether the candidate ledger avoids calling every regularity a goal;
- comprehension of `VALUE`, identity, capability, system, and environment;
- reuse versus new custom machinery; and
- whether a genuinely dynamic-environment substrate is now earned.

## Stop rules

- Do not add a new simulator or scientific generator.
- Do not invent a reciprocal environment for sorting.
- Do not promote a candidate goal from one trajectory or a hand-authored score.
- Do not claim the heuristic candidate ledger is automated goal discovery.
- Do not generalize the substrate before a second concrete system requires the
  same boundary.
- Stop after P9-C1 and select one next branch: repair comprehension, formalize a
  blinded held-out discovery experiment, test the runtime boundary on the bowl,
  or retain the UI as calibration only.

## Verification contract

- Same configuration and seed reproduce every baseline and branch frame.
- Every intervention family has a test proving exactly what changes at the
  boundary.
- Environment-schedule intervention changes scheduler dynamics but not cells,
  counters, or RNG at the boundary.
- Pre-intervention histories are identical.
- Sealed mode removes authored rule/internal-target fields from rendered
  tooltips and tables.
- Candidate evidence is computed from real frames and labels underdetermination.
- The live Panel route loads, configuration changes rebuild, the shared
  timeline synchronizes all views, and reveal/hide interaction works.

## P9-C1 result

- P9-V0 through P9-V2 are complete in one seven-region desktop workspace.
- The default view seals authored rule, internal target, and authored outcome.
- Candidate interpretations are computed from observed trajectories and remain
  explicitly underdetermined; the ledger is not an automated goal detector.
- Matched interventions now cover internal state, component capability, and the
  external activation scheduler. Unsupported families are visible as limits.
- The sorting environment is correctly described as limited and one-way, not a
  reciprocal dynamic environment or a general simulation substrate.
- The checkpoint passed 153 tests with 16 optional NetLogo checks skipped.
- Selected branch: retain this as calibration UI, then formalize one held-out
  blinded sorting-discovery protocol before making any goal-discovery claim.

See `docs/audits/2026-08-30_p9_c1_blind_sorting_ui.md` for the audit.
