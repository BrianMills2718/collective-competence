---
doc-role: experiment-result
authority: experiment
lifecycle: active
artifact_intent:
  concern_id: q1-010-determinism-control
  creation_justification: "Record the measured disposition of the frozen Q1-010 gates, including the falsification of the analyst's recorded prediction."
  separate_file_reason: A result must stay inspectable beside, and distinct from, its preregistration.
  retirement_condition: Archive only after clause 2 is validly tested or the statistic is withdrawn.
experiment_declaration:
  contract_version: 1
  primary_research_purpose: calibration
  secondary_research_purposes:
    - goal_competence_discovery
  specimen_origin: constructed
  evidence:
    provenance: observed
    claim_assessment: tested
    review_status: not_reviewed
    result_source: goal-discovery/results/q1-010-determinism-control/result.json
---
# Q1-010 result — the statistic survives on the slot, and my prediction did not

[Protocol](q1_010_determinism_control.md) ·
[Q1-009](q1_009_information_measures_results.md) ·
[Current plan](../plans/current_research_plan.md) ·
[Audit that motivated this](../audits/2026-09-05b_prose_vs_code_audit.md)

> Run at `daba7f0` from a clean worktree; package
> `results/q1-010-determinism-control/result.json`. Gates read once, thresholds
> taken from `null_calibration.json` committed in `4f09f00` before the protocol
> named them.

## Decision

**G-A fails, G-B passes** — the second row of the frozen disposition table.

> *The statistic does separate shared-period coordination from private-period
> independence. The critique is narrowed to the commons family, where `frozen`'s
> +0.198 then needs its own explanation, and the queued re-run may proceed with
> that limit recorded.*

**I predicted G-A would pass, and wrote that prediction into the protocol before
running. It did not.** The suspicion that EI-above-shuffle-null is a determinism
detector rather than a coordination detector is **not supported on the slot
family.**

| arm | EI micro | shuffle null | above null | in null sd | satisfaction | duty |
|---|---|---|---|---|---|---|
| `derived_phase` (coordinated) | 0.3502 | 0.1766 | **+0.1736** | **+6.3** | 0.3929 | 0.0865 |
| `private_period` (deterministic, independent) | 0.2373 | 0.1704 | **+0.0670** | **+1.7** | 0.2863 | 0.0902 |
| `private_period_primes` (declared, ungated) | 0.1127 | 0.2680 | −0.1553 | −1.7 | 0.1652 | 0.0578 |

| gate | required | actual | |
|---|---|---|---|
| G-A — statistic reports structure | ≥ 0.1217 above null | **+0.0670** | **fail** |
| G-B — coordination performance absent | ≤ 0.80 relative | **0.7287** | **pass** |

G-B passing is what makes G-A's failure informative. Removing the shared period
cost the population 27% of its need-satisfaction on a duty cycle matched to 4.3%,
so this really is a population that lost its coordination — and the statistic
correctly declined to report it as structured at the frozen bar.

## What this does not rescue, and it is not a small remainder

Three things stand, and two of them are the reason the concern was raised.

**1. The response is graded, not binary.** `private_period` is not *at* its null
the way `random_attempt` is (−0.040 in Q1-009). It is +1.7 null sd, and
+0.0670 is **39% of the coordinated arm's +0.1736**. Determinism with no shared
period buys about two fifths of the effect that Q1-009's summary attributes to
coordination. It falls under the frozen two-sd bar, which is the honest reading
of the gate, but "essentially nothing where it is absent" is not what this
family shows either.

**2. The commons counterexample is untouched.** This experiment did not re-run
the commons and does not bear on it. Q1-009's own committed table still reports
commons `frozen` — a deterministic arm which coordinates nothing and whose
satisfaction C1-001 measures at 0.000 — at **+0.198 above null with a null sd of
0.037, which is 5.4 sd**, against `random`'s +0.006. On the commons the
statistic reports strong structure for an uncoordinated population, and nothing
here explains that. Q1-009's 2026-09-05 correction section presents a summary
table of `live` against `random` only and concludes the statistic "reports
structure where coordination is present and reports essentially nothing where it
is absent, **on two families**." That conclusion is not supported on the commons
by Q1-009's own numbers, and this experiment does not supply it.

**3. The response across deterministic arms is non-monotonic.** Two deterministic
arms now score *below* their own nulls: `constant_phase` at −0.118 (Q1-009) and
`private_period_primes` at −0.1553 here. The primes arm carries no gate because
its duty cycle is 0.0578 against 0.0865 and sparser rows inflate its null, which
is the likely mechanism — but the same explanation is available for
`constant_phase`, and neither has been tested. A statistic whose sign depends on
duty-driven null inflation is not yet characterised.

## What I got wrong, and what it cost

The audit that commissioned this experiment
([2026-09-05b](../audits/2026-09-05b_prose_vs_code_audit.md), finding 3)
advised **not** running the queued Q1-006 re-run, on the grounds that it would
inherit a confound and produce a clause-2 pass on an instrument that had not been
shown to detect coordination. On the slot family — which is the family Q1-006 and
its re-run are on — that advice was wrong. The frozen gate says so, and the
advice is superseded rather than softened.

The reasoning error is worth naming because it is cheap to repeat: I read two
numbers from the commons (`frozen` +0.198) and one from the slot
(`constant_phase` −0.118), inferred a common mechanism, and generalised it to a
family where the deterministic-independent arm had never been measured. The
mechanism may still be right on the commons. It was not established anywhere.

## Two defects this apparatus found in itself, before the run

Recorded because both passed a smaller check first, which is the pattern the
current plan's debt 3 names.

- The first robustness arm drew periods from 2..14. At seed 6 those had a least
  common multiple of exactly 120 — the horizon — so the population still tiled a
  common cycle and would not have been an independent control. A 16-seed test
  passed while that was true. Replaced with prime periods, where any two distinct
  members have an LCM of at least 143.
- The primary arm is inadmissible on 7 of 1600 seeds for the same reason; seed
  557 draws only periods 10 and 11, LCM 110. Found by checking all 1600 rather
  than a sample. Those seeds are excluded from every arm including
  `derived_phase`, so the needs distribution stays matched — mean need 8.0120 to
  8.0131, mean distinct-need count 7.121 to 7.127.

The first version of the freeze guard matched the substring `observed` and fired
on its own `observed_units` dimension constant. It is now an exact-key walk with
a negative control in `tests/test_q1_010_control.py`.

`results/*` is still ignore-everything-plus-allowlist. This package was invisible
to Git until its entry was added by hand — the mechanism behind finding 1 of the
2026-09-05 assessment is unrepaired, and it caught the next new experiment.

## Evidence limits

- One family, one coarse-graining, one observation contract, 1593 seeds.
- This is not a clause-2 test. These arms are not the completion condition's
  matched pair and nothing here was blind.
- `private_period_primes` is not duty-matched and carries no gate. Its negative
  value is a direction, not a measurement of anything.
- The commons was not re-run. Every commons number cited here is Q1-009's.
- Whether some other null or statistic separates determinism from coordination
  is untested.
