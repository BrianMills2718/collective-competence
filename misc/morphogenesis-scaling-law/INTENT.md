---
authority: none
owner: collective-competence (Brian)
destination: >
  Undecided pending review. Candidate outcomes: (a) a results reference
  cited from levin-wiki's platonic-space-and-ingression.md (its own
  "what's next" section names this exact computation), (b) folded into
  collective-competence's own research plan if a contributor decides the
  question is worth pursuing further there, or (c) left as a standalone
  reference script/result with no further claim.
reason: >
  A one-off computational result (not a collective-competence experiment)
  answering a specific question raised on a separate, unrelated wiki
  (levin-wiki's living document on Michael Levin's "Platonic ingression"
  framework): how does the maximum solvable tissue size N_max for a
  bilateral-morphogen midpoint-classification task scale with decay
  length, sensor SNR, and equilibration time, once the idealized
  exact-arithmetic assumption (unbounded N_max) is replaced with a real
  noise floor and a real, numerically-integrated reaction-diffusion PDE.
  Placed here rather than in levin-wiki itself (which has no code-running
  convention and an explicit house rule against spending API money or
  running services) and rather than as a claimed collective-competence
  research direction (this repository's own current_research_plan.md
  alone owns active priorities; nothing here claims that status).
expires_at: "2026-09-17T00:00:00Z"
---

# Morphogenesis scaling law — one-off computational result

`scaling_law.py` (run inside the local `.venv/`, not committed — see
below) numerically integrates a 1D reaction-diffusion PDE for two
opposing morphogen fields and computes how N_max (largest tissue size
solvable at ≥95% classification accuracy at the hardest cell) scales
with decay length λ, sensor SNR, and equilibration time t_eq / τ.

Two regression checks must pass before the sweep runs: the known exact
closed-form sign identity `R_i ≥ L_i ⟺ i ≥ (N-1)/2`, and the same
identity reproduced by the actual numerical integrator (finite domain,
reflecting far boundary) — the second check caught a real numerical
instability bug in an earlier version of this script (an incomplete
timestep-stability bound that ignored the reaction term), which produced
alternating-sign floating-point garbage for small λ before being fixed.

See `RESULTS.md` for the actual findings, `n_max_scaling.csv` for the raw
swept data, and `n_max_scaling.png` for the three scaling curves.

**Not a benchmark result to cite without reading `RESULTS.md` first**: the
λ-scaling curve has only 3 usable data points (N_max is undefined, i.e.
below the smallest tested tissue size of 2, at λ=8 and λ=16 for this
fixed SNR) and the t_eq-scaling curve is non-monotonic with a real
interior maximum, not a simple "more equilibration is always better"
relationship — both are reported as genuine findings, not artifacts, but
neither has been independently reproduced.

`.venv/` is untracked (see `.gitignore` added alongside this file) —
recreate with `python3 -m venv .venv && .venv/bin/pip install numpy scipy
matplotlib`, then `.venv/bin/python3 scaling_law.py`.
