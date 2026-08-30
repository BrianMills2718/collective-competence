# OB-001 delivery review — V0 through V2

**Status:** V0, V1, and V2 implemented; V3 closed by an evidence-backed no-go.
This is an interface and planning-method review, not a new scientific result.

## Mature outcome supported

The cockpit now connects the north star and frontier to the claim, observation
boundary, real behavior, representations, perturbation evidence,
black-box/white-box comparison, provenance, uncertainty, and next experiment.
The outcome map contains twelve sections. Every section records its question,
evidence requirement, capability, provenance state, repository source when
non-hypothetical, first maturity version, and next test or retirement path.
Scale/control and competence remain prominently hypothetical.

## Version decisions

### V0 — mature outcome hypothesis — implemented

The default cockpit view renders the full question-to-evidence ledger and V0–V6
maturity ladder from docs/research_state.yaml. Filters expose provenance and
target version. No imagined numerical result is displayed.

### V1 — one real evidence chain — implemented

P7-002 connects real network trajectories, the tick-20 boundary, synchronized
baseline/intervention views, four representation lenses, split-labeled seeds,
scores against the intervention-only null, every prediction and failure, the
8.4% result against the frozen 10% gate, the diagnostic-only 14.4% ablation,
the mechanically excluded seed, the claim boundary, and the P7-003 decision.

The viewer no longer substitutes a nearby stored snapshot for a requested tick.
History lenses now state that they count stored snapshots. Score values are
derived from result tables and the frozen analysis threshold.

### V2 — blind calibration — implemented

The Heatbugs view joins the completed black-box calibration without opening a
new experiment. It displays, by seed and identity, the target inferred from
allowed probes beside the authored ideal temperature joined only after
inference. It compares 71.5% held-out prediction with the 55.5% identity-free
midpoint null and exposes the 2.0° median target error.

This validates recovery of authored heterogeneous micro-targets. It does not
establish an emergent collective goal.

### V3 — prospective transfer — closed no-go

P7-002 missed its prospective gate. P7-003 equalized descriptive capacity and
still produced held-seed winner counts of 3 identity, 3 network, 2 temporal,
and 0 relational against a required 6/8. Generic automated family selection is
retired. The mature artifact was revised instead of filling a planned
leaderboard with a post-hoc winner.

## Required audits

### Goal alignment

Retained views answer programme decisions: where the frontier is, what evidence
supports or contradicts a claim, which boundary was frozen, and what experiment
is licensed next. No UI element is counted as scientific progress.

### Scientific integrity

- hypothetical sections contain no invented outcomes;
- non-hypothetical sections require a repository source;
- discovery, confirmation, retrospective, and authored-truth boundaries remain
  distinct;
- individual failures and null comparisons remain visible;
- opened-data diagnostics are not presented as prospective evidence;
- Heatbugs truth is scoring truth, not an inference input.

### Reuse versus custom code

The implementation reuses Panel, Bokeh, Tabulator, NetLogo output, and existing
validated tables. It adds thin adapters and composition only. No visualization
framework, simulator, database, or generalized evidence platform was created.

### UI comprehension and responsive behavior

Live checks exercised the outcome map and evidence-split interaction. At 1280px
and 390px viewport widths, the page had zero document-level horizontal overflow.
Heavy tabs load on demand. The question, provenance warning, filters, ledger,
and evidence controls remain available on phone; wide tables retain bounded
internal scrolling.

The question, evidence, uncertainty, conclusion, and next decision are available
as visible text without relying on plot hover or color.

### Correctness and verification

The state loader validates outcome completeness, provenance, maturity status,
and source existence. Tests cover missing provenance, exact snapshots,
P7-003's frozen no-go, and Heatbugs result agreement. The full suite and lint
are rerun at each checkpoint.

## Planning-method learning

P7-003 shows a concrete benefit: the mature artifact preserved an abstention
route and prevented a strong-looking retrospective score from filling the
generic-selector box. Learning also removed a planned capability rather than
treating the first mock as fixed.

Work avoided:

- no new generator for V0–V3;
- no custom visualization framework;
- no rerun or tuning of closed Virus and Heatbugs outcomes;
- no false pass from the better P7-002 ablation;
- no generic selector leaderboard after P7-003.

Planning overhead and time-to-first-evidence were not instrumented for P7-003
and remain unmeasured. P7-004 must record start, first-artifact, and decision
timestamps. This is sprint observation one of three; company-planning
generalization remains locked.

## Next conditional decision

P7-004 asks whether a mesoscopic pheromone-trail representation predicts
post-cut food delivery better than equally small local and colony descriptions
in the unmodified NetLogo Ants model. V4 remains hypothetical until that frozen
experiment passes, selects a simpler scale, abstains, or closes by integrity
no-go.
