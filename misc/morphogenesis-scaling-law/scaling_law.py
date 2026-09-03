"""Morphogenesis midpoint-task scaling law: N_max(lambda, SNR, t_eq).

Question: for a 1D tissue of N cells sensing two opposing endogenous
morphogen gradients (L sourced at the left end, R sourced at the right end),
each obeying dC/dt = D*d2C/dx2 - mu*C with a fixed-concentration boundary
source, how does the largest tissue size N_max a locally-bounded controller
can still classify (which half of the tissue it's in) scale with:
  - decay length lambda = sqrt(D/mu)
  - sensor signal-to-noise ratio SNR (noise floor fixed relative to the
    source concentration, not the local decayed signal)
  - equilibration time t_eq (how long the fields are allowed to settle)

Ground truth for cell i in a tissue of size N: right half iff i > (N-1)/2.
The already-proven exact-arithmetic identity (zero noise, full equilibration):
    R_i >= L_i  <=>  i >= (N-1)/2
This script's first job is to reproduce that identity exactly, as a
regression check, before trusting anything noisy or finite-time.

Classification accuracy at the hardest cell (immediately adjacent to the
exact midpoint) is computed in closed form: since the noisy decision is
sign((R_i - L_i) + noise), where noise ~ N(0, 2*sigma^2) is the difference of
two independent Gaussian sensor noises, P(correct) = Phi(sep / (sigma*sqrt(2)))
where sep = |R_i - L_i| (true, noiseless separation) and sigma = 1.0 / SNR.
This avoids Monte Carlo variance in the reported accuracy.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass

import numpy as np
from scipy.stats import norm

SOURCE_CONCENTRATION = 1.0  # fixed Dirichlet boundary value for each field
D = 1.0  # diffusion coefficient; lambda is varied via mu = D / lambda**2
ACCURACY_THRESHOLD = 0.95


def steady_state_profile(n: int, lam: float) -> np.ndarray:
    """Exact steady-state exponential profile for a field sourced at x=0,
    reflecting (zero-flux) far boundary, on a grid of n cells (dx=1)."""
    x = np.arange(n, dtype=float)
    # For a semi-infinite domain this is exactly exp(-x/lam); for a finite
    # domain with a reflecting far end it's a decaying exponential plus a
    # small correction. For lam << n (the interesting regime), exp(-x/lam)
    # is accurate to numerical precision; used only for the exact-arithmetic
    # regression check, not for the noisy/finite-time sweep below.
    return SOURCE_CONCENTRATION * np.exp(-x / lam)


def integrate_field(n: int, lam: float, t_eq: float, source_at_left: bool) -> np.ndarray:
    """Numerically integrate dC/dt = D*d2C/dx2 - mu*C to time t_eq on an
    n-cell 1D grid (dx=1), Dirichlet source at one end, zero-flux (mirrored
    ghost cell) at the other end. Explicit FTCS with a stability-safe dt."""
    mu = D / lam**2
    dx = 1.0
    # FTCS stability for dC/dt = D*Laplacian - mu*C: the right-hand-side
    # operator's eigenvalues lie in [-(4D/dx^2 + mu), 0], so forward Euler
    # needs dt <= 2 / (4D/dx^2 + mu). Ignoring the reaction term here (as an
    # earlier version of this script did) put dt right at the marginal
    # stability boundary for small lambda, producing alternating-sign
    # numerical garbage -- caught by the integrator regression check below.
    max_stable_dt = 2.0 / (4.0 * D / dx**2 + mu)
    dt = 0.5 * max_stable_dt
    n_steps = max(1, int(np.ceil(t_eq / dt)))
    dt = t_eq / n_steps if n_steps > 0 else dt

    c = np.zeros(n, dtype=float)
    src_idx = 0 if source_at_left else n - 1
    c[src_idx] = SOURCE_CONCENTRATION

    for _ in range(n_steps):
        # Ghost cells mirror the edge value (zero-flux/reflecting at both
        # ends); the Dirichlet source is re-imposed right after, which
        # overrides the zero-flux behavior at the source end only.
        padded = np.pad(c, 1, mode="edge")
        laplacian = padded[2:] + padded[:-2] - 2.0 * c
        c = c + dt * (D * laplacian - mu * c)
        c[src_idx] = SOURCE_CONCENTRATION

    return c


def hardest_cell_index(n: int) -> int:
    """Cell immediately adjacent to the exact midpoint (N-1)/2, on the
    'right' side, where ground truth is unambiguous (i > (N-1)/2)."""
    mid = (n - 1) / 2.0
    return int(np.floor(mid)) + 1 if n % 2 == 0 else int(mid) + 1


def exact_arithmetic_regression_check(ns: list[int]) -> bool:
    """Reproduce R_i >= L_i <=> i >= (N-1)/2 exactly, for several N, using
    the exact closed-form steady-state profiles (zero noise, full
    equilibration on a semi-infinite domain) -- checks the identity itself,
    independent of the numerical integrator."""
    all_ok = True
    for n in ns:
        lam = 4.0  # arbitrary; identity must hold regardless of decay constant
        L = steady_state_profile(n, lam)
        R = steady_state_profile(n, lam)[::-1]
        mid = (n - 1) / 2.0
        predicted_right = R >= L
        truth_right = np.arange(n) >= mid
        if not np.array_equal(predicted_right, truth_right):
            print(f"  REGRESSION FAILURE (closed-form) at N={n}: mismatch")
            all_ok = False
    return all_ok


def integrator_regression_check(ns: list[int], lams: list[float]) -> bool:
    """Reproduce the same sign identity using the actual numerical PDE
    integrator (finite domain, reflecting far boundary) at long
    equilibration time -- this is the code path the sweep actually uses,
    and the closed-form check above does not exercise it."""
    all_ok = True
    for lam in lams:
        for n in ns:
            t_eq = 20.0 * tau(lam)  # long enough for finite-domain steady state
            L = integrate_field(n, lam, t_eq, source_at_left=True)
            R = integrate_field(n, lam, t_eq, source_at_left=False)
            mid = (n - 1) / 2.0
            predicted_right = R >= L
            truth_right = np.arange(n) >= mid
            if not np.array_equal(predicted_right, truth_right):
                print(f"  REGRESSION FAILURE (integrator) at N={n}, lambda={lam}: "
                      f"L={L}, R={R}")
                all_ok = False
    return all_ok


def accuracy_at_hardest_cell(n: int, lam: float, snr: float, t_eq: float) -> float:
    L = integrate_field(n, lam, t_eq, source_at_left=True)
    R = integrate_field(n, lam, t_eq, source_at_left=False)
    i = hardest_cell_index(n)
    sep = abs(R[i] - L[i])
    sigma = SOURCE_CONCENTRATION / snr
    if sigma == 0:
        return 1.0 if sep > 0 else 0.5
    z = sep / (sigma * np.sqrt(2.0))
    return float(norm.cdf(z))


def find_n_max(lam: float, snr: float, t_eq: float, n_grid: np.ndarray) -> int | None:
    """Largest N in n_grid at which hardest-cell accuracy >= threshold."""
    best = None
    for n in n_grid:
        acc = accuracy_at_hardest_cell(int(n), lam, snr, t_eq)
        if acc >= ACCURACY_THRESHOLD:
            best = int(n)
        else:
            # accuracy is not perfectly monotonic at very small N (finite
            # equilibration-time edge effects); keep scanning the full grid
            # rather than stopping at the first failure.
            continue
    return best


@dataclass
class SweepPoint:
    varied: str
    value: float
    lam: float
    snr: float
    t_eq: float
    n_max: int | None


def tau(lam: float) -> float:
    """Diffusion time scale D*mu... actually mu = D/lam^2, tau = 1/mu = lam^2/D."""
    return lam**2 / D


def run_sweeps() -> list[SweepPoint]:
    n_grid = np.arange(2, 401, 2)
    results: list[SweepPoint] = []

    baseline_lam, baseline_snr = 4.0, 30.0

    for lam in [1.0, 2.0, 4.0, 8.0, 16.0]:
        t_eq = 5.0 * tau(lam)
        n_max = find_n_max(lam, baseline_snr, t_eq, n_grid)
        results.append(SweepPoint("lambda", lam, lam, baseline_snr, t_eq, n_max))

    for snr in [3.0, 10.0, 30.0, 100.0, 300.0]:
        t_eq = 5.0 * tau(baseline_lam)
        n_max = find_n_max(baseline_lam, snr, t_eq, n_grid)
        results.append(SweepPoint("snr", snr, baseline_lam, snr, t_eq, n_max))

    for frac in [0.1, 0.3, 1.0, 3.0, 10.0]:
        t_eq = frac * tau(baseline_lam)
        n_max = find_n_max(baseline_lam, baseline_snr, t_eq, n_grid)
        results.append(SweepPoint("t_eq_over_tau", frac, baseline_lam, baseline_snr, t_eq, n_max))

    return results


def write_csv(results: list[SweepPoint], path: str) -> None:
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["varied_parameter", "varied_value", "lambda", "snr", "t_eq", "n_max"])
        for r in results:
            w.writerow([r.varied, r.value, r.lam, r.snr, r.t_eq, r.n_max])


def write_plot(results: list[SweepPoint], path: str) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    panels = [
        ("lambda", "decay length (lambda)", axes[0]),
        ("snr", "sensor SNR", axes[1]),
        ("t_eq_over_tau", "equilibration time / tau", axes[2]),
    ]
    for key, label, ax in panels:
        pts = [r for r in results if r.varied == key and r.n_max is not None]
        xs = [r.value for r in pts]
        ys = [r.n_max for r in pts]
        ax.plot(xs, ys, marker="o")
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel(label)
        ax.set_ylabel("N_max (accuracy >= 0.95)")
        ax.set_title(f"N_max vs {label}")
        ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=150)


if __name__ == "__main__":
    print("Regression check 1: closed-form identity R_i >= L_i <=> i >= (N-1)/2")
    ok1 = exact_arithmetic_regression_check([4, 5, 10, 11, 50, 51, 200, 201])
    print("  PASS across all tested N.\n" if ok1 else "")

    print("Regression check 2: same identity via the actual numerical integrator")
    ok2 = integrator_regression_check([4, 5, 10, 11, 50, 51], [1.0, 4.0, 16.0])
    print("  PASS across all tested (N, lambda).\n" if ok2 else "")

    if not (ok1 and ok2):
        raise SystemExit("A regression check failed -- not proceeding to the sweep.")

    print("Diagnostic: why does lambda=8,16 report N_max=None at N=2..10?")
    for lam in [8.0, 16.0]:
        for n in [2, 4, 6, 10]:
            t_eq = 5.0 * tau(lam)
            L = integrate_field(n, lam, t_eq, source_at_left=True)
            R = integrate_field(n, lam, t_eq, source_at_left=False)
            i = hardest_cell_index(n)
            sep = abs(R[i] - L[i])
            acc = accuracy_at_hardest_cell(n, lam, 30.0, t_eq)
            print(f"  lambda={lam}, N={n}: hardest_cell={i}, L={L[i]:.4f}, R={R[i]:.4f}, "
                  f"sep={sep:.4f}, accuracy={acc:.4f}")
    print()

    print("Running parameter sweep (this integrates the PDE many times, may take a bit)...")
    results = run_sweeps()

    write_csv(results, "n_max_scaling.csv")
    write_plot(results, "n_max_scaling.png")

    print("\nResults:")
    for r in results:
        print(f"  {r.varied}={r.value}: lambda={r.lam}, snr={r.snr}, t_eq={r.t_eq:.2f} -> N_max={r.n_max}")
    print("\nWrote n_max_scaling.csv and n_max_scaling.png")
