---
doc-role: experiment-protocol
authority: experiment
lifecycle: frozen
---
# C1-001 — does a shared scarcity signal have to track scarcity?

[Wiki](../../../wiki/index.md) · [Conjecture register](../../../wiki/conjectures.md) ·
[Ontology](../../../wiki/ontology.md) · [Current plan](../plans/current_research_plan.md)

**Frozen before execution.** This protocol is committed before any run of the
implementation exists. No result, figure, or measurement informed it.

## Decision and claim boundary

[C1](../../../wiki/conjectures.md) claims that for discrete systems whose
subunits hold locally-conflicting objectives over a shared resource, collective
performance varies with how well a shared scalar satisfies the cognitive-glue
properties — and specifically degrades as the signal's coupling to actual
scarcity is weakened, with everything else held fixed.

This experiment tests the decisive part: **is property 1 (the parameter tracks
changes in scarcity) load-bearing, or does any constant threshold do as well?**

Research purpose: **Collective Competence** (constructive/mechanistic). Specimen
origin: **constructed**. Analyst access: **white-box** — the mechanism is
authored and known; this is not a discovery study and cannot produce a
discovered goal. The goal criterion is supplied, not inferred.

What a pass would establish: that on this family, a scarcity-tracking scalar
outperforms the best matched constant, and that performance varies monotonically
with how much of the live signal is retained. What it would **not** establish:
anything about composition in general, any claim about other substrates, or that
this mechanism is how any natural system coordinates.

## Substrate

A discrete state-transition system. State is `(R, {a_i}, p)` where `R` is a
shared renewable stock, `a_i` the accumulation of subunit `i`, and `p` the shared
scalar. One tick is:

1. **Regrow.** `R += g * R * (1 - R / K)`, clipped to `[0, K]`. Depletion is
   absorbing: at `R = 0` regrowth is zero and the commons is dead. This is what
   makes the subunits' objectives genuinely conflicting rather than merely
   simultaneous.
2. **Decide.** Each subunit computes its own urgency `u_i = remaining_quota_i /
   remaining_ticks`, a purely local quantity, and draws iff `u_i >= p`. No
   subunit observes another's quota, accumulation, or decision.
3. **Draw.** Attempted draws are `d_i = min(m, remaining_quota_i)` for deciding
   subunits, served from `R` and rationed equally if `sum(d_i) > R`.
4. **Update the signal.** Per condition, below.

`m` is the per-tick draw cap. Nothing else is shared.

## Conditions

All conditions share seed, initial state, subunit rules, topology, quotas, and
resource parameters. They differ only in how `p` is produced.

| Condition | `p` at each tick |
|---|---|
| `live` | `p = max(0, p + kappa * (D - A) / A_ref)`, where `D` is total attempted draw, `A = g*R*(1-R/K)` the current regrowth, `A_ref = g*K/4` the maximum sustainable yield |
| `frozen` | Held constant at `p_bar`, the **time-average of that seed's own `live` run**. Still read by every subunit, every tick. |
| `none` | `p = 0`. Every subunit always draws. |

The `frozen` condition is the negative control C1 names, and it is deliberately
constructed to be **favorable to the null**: `p_bar` is taken from the live run
itself, so it is close to the best available constant rather than an arbitrary
one. It removes the behaviour (tracking) while keeping every symbol in place —
each subunit still reads a shared scalar and still compares its urgency against
it. A control that deleted `p` would test whether the parameter is read, not
whether tracking matters; `none` is included separately for that weaker question.

**Fidelity sweep.** `p_eff = alpha * p_live + (1 - alpha) * p_bar` for
`alpha in {0.0, 0.25, 0.5, 0.75, 1.0}`. `alpha = 1` is `live`; `alpha = 0` is
`frozen`.

## Measurement

Primary: **quota satisfaction** — the fraction of subunits reaching their quota
by horizon `T`, averaged over seeds. Reported per seed, not only pooled.

Secondary, reported but not gated: final `R` (did the commons survive), and the
tick at which `R` first reaches zero if it does.

**Opportunity accounting.** Per [the ontology](../../../wiki/ontology.md),
reachability is reported separately: a configuration in which total quota exceeds
what the resource can yield over `T` under any policy is infeasible, and failure
there is not a coordination failure. Feasibility is computed analytically from
`g, K, T, N, Q, m` and any infeasible configuration is excluded before scoring.

## Frozen gates

Declared before execution. Eight seeds.

- **G1 — the setup poses a coordination problem at all.** `live` beats `none` by
  at least 20% relative on quota satisfaction, on at least 6 of 8 seeds.
  If G1 fails, this experiment is **invalid, not a refutation of C1**: the
  configuration did not create the conflict C1 is about. Report as invalid and
  do not reinterpret the remaining comparisons.
- **G2 — the actual test.** `live` beats `frozen` by at least 10% relative on
  quota satisfaction, on at least 6 of 8 seeds.
- **G3 — the scaling claim.** Mean quota satisfaction is non-decreasing in
  `alpha` across the swept range, allowing ties.

## What each outcome means

| Result | Disposition |
|---|---|
| G1 fails | Invalid configuration. C1 untested. Do not retune to make G1 pass and then read G2. |
| G1 passes, G2 fails | **Genuine negative for C1 on this family.** The best matched constant is as good as tracking; property 1 is not load-bearing here. Record it, do not search for a configuration where G2 passes. |
| G1, G2 pass, G3 fails | Partial. Tracking helps at the endpoint but the effect is not monotonic in fidelity; C1's scaling form is not supported as stated. |
| All three pass | C1 supported **on this family only**. Earns one narrowing or one transfer test, not a general claim. |

## Stop conditions

Stop and report rather than adjust if: any condition's runs differ in seed or
initial state; `p_bar` is computed from anything but that seed's own live run; a
gate is restated after seeing a number; or the fidelity sweep is truncated to a
range that makes G3 pass.

## Pre-declared limits

Four seeds' worth of intuition went into choosing `g`, `K`, `T`, `N`, `Q`, `m`
and `kappa` so that the commons neither trivially survives greedy harvesting nor
collapses under every policy. That tuning is **authored**, is disclosed here, and
is the main reason a pass would be bounded to this family. The parameters are
frozen in `config.json` alongside the implementation and are not adjusted after
any gate is evaluated.
