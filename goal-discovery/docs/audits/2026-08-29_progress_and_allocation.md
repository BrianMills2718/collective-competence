# Progress and allocation audit — 2026-08-29

> **Status: historical audit.** Its outcome remains part of the decision trail;
> the authoritative current allocation is the
> [current research plan](../plans/current_research_plan.md).

## End goal used for the audit

The programme is trying to discover which observable representations and
scales make the organization, capability, prediction, and control of coupled
dynamical systems most legible.  A useful result must change a scientific
decision: provide a measurement, mechanism, threshold, scaling relationship,
theory discrimination, or cross-scale result.

## What the current work has bought

- The reproducible trajectory, snapshot/branch, observation-boundary, and
  intervention apparatus is working.
- Experiments 001–005 calibrated the evidentiary ladder from passive
  convergence through engineered regulation, compensation, and adaptation.
- P2-001 showed that the blind predictive comparison can fail cleanly and then
  pass after a separately frozen redesign.
- X01–X03 settled the software choices: NetLogo is useful for generator-side
  playback; the authoritative sorting generator and stored trajectories remain
  analysis-independent; Panel/HoloViews is adequate for local linked analysis.
- The phone mockup made the intended observe → falsify → decide workflow visible
  without building a new research application.
- The existing-data screen exposed a measurement candidate (retained
  capability) and, more importantly, a confound: every existing freeze case
  fails.  The current screen therefore cannot distinguish capability from the
  intervention label.

## Allocation decision

The visualization objective has reached Level 0/1 confidence.  Another visual
or framework pass would improve presentation but cannot change the next
scientific decision.  It is therefore stopped.

The highest expected goal movement per minute is a crossed sorting batch in
which identical intervention classes contain both success and failure.  It can
discriminate a capability-aware macro description from value-only,
intervention-only, history-aware, and observable-micro alternatives.  It reuses
the existing Python sorting generator, scikit-learn, and the established
trajectory boundary; no simulator or dashboard framework is added.

## Ranked next work

| Work item | Decision unlocked | Time cap | Disposition |
|---|---|---:|---|
| Crossed P2-002 discovery batch | Whether capability-aware prediction is real enough to promote | 45 min | Do now |
| New-size held-out batch | Whether the promoted signal generalizes | 60 min, conditional | Run only after promotion |
| Evidence/dashboard refresh | Make the changed decision legible | 20 min | Only after data changes |
| More dashboard machinery | None at the current evidence boundary | — | Stop |
| Automatic representation search / causal emergence | Premature without a generalizing macro signal | — | Defer |

## Next-version boundary

The next version is not a larger interface.  It is one complete learning loop:

1. freeze the crossed design;
2. generate discovery trajectories at size 12;
3. compare the five declared representation families with held-out seeds;
4. stop if the promotion gate fails;
5. otherwise run the already frozen size-24 batch on unseen seeds;
6. update one evidence surface and the research plan with the result.

Validation remains proportional to this rapid sprint: deterministic replay and
feature-boundary tests, grouped discovery evaluation, and one held-out size.
Broader confirmation is not prepaid.

## Audit outcome

The discovery batch stopped at its gate. Capability-aware prediction reduced
log loss by 18.9% against intervention-only, below the frozen 20% threshold, so
the conditional size-24 spend was avoided. The error audit localized the useful
signal to mixed-outcome boundary regimes; deterministic freeze classes were
already easy for the intervention label. The next allocation is therefore a
short within-condition design sprint using existing evidence, not broader data,
new machinery, or more interface work.
