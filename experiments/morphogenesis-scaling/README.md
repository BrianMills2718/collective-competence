# Morphogenesis scaling law — a retained reference result

**Status: retained reference. Not an experiment record, and not a rung of the
founding ladder.** Promoted out of `misc/` quarantine on 2026-09-04, where it
would otherwise have expired on 2026-09-17.

## What it is

A one-off computational result answering a question raised on a *different*
repository — `levin-wiki`'s living document on Platonic ingression, whose
"what's next" section names this exact computation.

`scaling_law.py` numerically integrates a 1-D reaction-diffusion PDE for two
opposing morphogen fields and computes how **N_max** — the largest tissue size
solvable at ≥95% classification accuracy at the hardest cell — scales with
decay length λ, sensor SNR, and equilibration time. It replaces the idealized
exact-arithmetic assumption (which implies unbounded N_max) with a real noise
floor and a real integrator.

`boundary_comparison.py` tests whether the same case's ingress classification
survives redrawing the agent/system boundary.

## Why it is not registered as an experiment

[`roadmap/experiments.json`](../../roadmap/experiments.json)'s own rule is that
every record outside its **closed** legacy inventory must declare an ontology
contract in a frozen native protocol. This work was never preregistered here —
it was imported — so registering it would require either backfilling a contract
speculatively or writing a "frozen protocol" after the fact. Both would
misrepresent its provenance. Its own prior `INTENT.md` reached the same
conclusion independently, listing "standalone reference result with no further
claim" among its candidate destinations.

It sits beside [`01-self-sorting/`](../01-self-sorting/) because both are
Collective Competence arm material — mechanism to capability — not because it is
the ladder's rung 02. That rung (a tiny production/specialization world) remains
unstarted.

## Why it was worth keeping

Two things, and the second is the live one.

**The scaling law.** Two findings are explicitly reported as findings rather
than artifacts: N_max is **non-monotonic in λ** and collapses below the smallest
testable tissue past a threshold, because at fixed absolute sensor noise a
longer decay length flattens both fields; and the equilibration-time curve has a
genuine **interior maximum** rather than "more equilibration is always better."

**The boundary test, which bears on an open question in this repository.**
[`ontology.md`'s free-lunch section](../../wiki/ontology.md) records boundary
arbitrariness as a *load-bearing* weakness: "free relative to the agent
boundary" holds there only because every worked example's boundary happens to
track real physical structure, with no principled rule against gerrymandering.
`BOUNDARY_RESULTS.md` is a direct probe of exactly that. It finds that expanding
the boundary to include mere sensing apparatus leaves the classification
unchanged, while expanding it to include baseline access to the same information
source shifts the classification **smoothly and continuously, with no
pathological jump**. That is a partial answer to a weakness this repository
documented as open, arrived at independently.

## Limits, from the work's own account

- The λ curve has **only 3 usable data points**; N_max is undefined at λ=8 and
  λ=16 for the tested SNR.
- **Neither curve has been independently reproduced.**
- Boundary B's result is a logical argument, not a new simulation.
- Not a benchmark result to cite without reading `RESULTS.md` first.

Two regression checks gate the sweep: the exact closed-form sign identity
`R_i ≥ L_i ⟺ i ≥ (N-1)/2`, and that identity reproduced by the numerical
integrator. The second caught a real timestep-stability bug that had been
producing alternating-sign garbage at small λ.

## Running it

`.venv/` is untracked. Recreate with
`python3 -m venv .venv && .venv/bin/pip install numpy scipy matplotlib`,
then `.venv/bin/python3 scaling_law.py`.
