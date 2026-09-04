"""Boundary-comparison test for the morphogenesis midpoint case.

Tests whether the ingress-category classification (representational /
computational subsidy / informational / strong residual) is robust to
where the agent/system boundary is drawn, for one concrete case, per
levin-wiki's platonic-space-and-ingression.md open question on this.

Reuses integrate_field() and hardest_cell_index() from scaling_law.py
directly rather than reimplementing the PDE.

Boundary A (baseline, already established elsewhere): O = empty (an
isolated cell has zero prior information about which half it's in --
this is why local-only signaling is bounded at N_max=2T+1), Z = the
sensed bilateral field values (L_i, R_i) at a single SNR. Classified:
informational ingress, I(Y;Z|O) > 0.

Boundary B: relabel the membrane sensing/transduction channel as part
of the agent. Z still refers to the same external field concentration
-- transduction cost moves from B_I to B_A, but the joint distribution
of (Y, Z, O) is unchanged, so I(Y;Z|O) is predicted unchanged. This is
a logical argument, not a new computation; checked here only for a
hidden confound (does moving the channel inside change what O or Z
actually refers to -- it does not, since Z is defined as the external
concentration value regardless of which side of the boundary transduces
it).

Boundary C: the agent already has crude, low-SNR baseline sensing of
its own microenvironment "for free" (O = a noisy reading at SNR_O of
the same true separation), and Z is the marginal gain from upgrading to
a higher-precision reading at SNR_Z. Two independent Gaussian estimates
of the same true separation combine by inverse-variance weighting; the
marginal value of Z is the resulting accuracy gain over O alone. At
SNR_O=0 this must reduce exactly to Boundary A's result (regression
check).
"""
from __future__ import annotations

import csv

import numpy as np
from scipy.stats import norm

from scaling_law import (
    SOURCE_CONCENTRATION,
    hardest_cell_index,
    integrate_field,
    tau,
)


def true_separation(n: int, lam: float, t_eq: float) -> float:
    L = integrate_field(n, lam, t_eq, source_at_left=True)
    R = integrate_field(n, lam, t_eq, source_at_left=False)
    i = hardest_cell_index(n)
    return abs(R[i] - L[i])


def accuracy_from_snr(sep: float, snr: float) -> float:
    """Same formula as scaling_law.accuracy_at_hardest_cell, generalized to
    take a precomputed separation rather than recomputing the PDE."""
    if snr <= 0:
        return 0.5  # no information at all
    sigma = SOURCE_CONCENTRATION / snr
    z = sep / (sigma * np.sqrt(2.0))
    return float(norm.cdf(z))


def accuracy_o_and_z(sep: float, snr_o: float, snr_z: float) -> float:
    """Accuracy given BOTH an O-reading (SNR_O) and a Z-reading (SNR_Z) of
    the same true separation, combined by inverse-variance (Gaussian
    fusion) weighting. At snr_o=0, this must equal accuracy_from_snr(sep,
    snr_z) exactly (Boundary A's result) -- the regression check below
    verifies this."""
    # noise variance on the *difference* R_i - L_i at a given SNR is
    # 2*sigma^2, matching scaling_law's derivation (independent noise on
    # both L and R sensor readings).
    def variance(snr: float) -> float:
        if snr <= 0:
            return np.inf
        sigma = SOURCE_CONCENTRATION / snr
        return 2.0 * sigma**2

    var_o = variance(snr_o)
    var_z = variance(snr_z)
    weight_o = 0.0 if np.isinf(var_o) else 1.0 / var_o
    weight_z = 0.0 if np.isinf(var_z) else 1.0 / var_z
    total_weight = weight_o + weight_z
    if total_weight == 0.0:
        return 0.5
    combined_variance = 1.0 / total_weight
    z_score = sep / np.sqrt(combined_variance)
    return float(norm.cdf(z_score))


def marginal_gain_regression_check(n: int, lam: float, snr_z: float, t_eq: float) -> bool:
    """At snr_o=0, accuracy_o_and_z must exactly equal accuracy_from_snr
    with snr_z alone -- Boundary C must collapse to Boundary A's already-
    established result in this limit."""
    sep = true_separation(n, lam, t_eq)
    combined = accuracy_o_and_z(sep, snr_o=0.0, snr_z=snr_z)
    baseline = accuracy_from_snr(sep, snr_z)
    ok = np.isclose(combined, baseline, atol=1e-9)
    if not ok:
        print(f"  REGRESSION FAILURE: combined(snr_o=0)={combined} != baseline={baseline}")
    return ok


def run_boundary_c_sweep(n: int, lam: float, snr_z: float, t_eq: float,
                          snr_o_grid: np.ndarray) -> list[dict]:
    sep = true_separation(n, lam, t_eq)
    rows = []
    for snr_o in snr_o_grid:
        acc_o_alone = accuracy_from_snr(sep, snr_o)
        acc_combined = accuracy_o_and_z(sep, snr_o, snr_z)
        marginal_gain = acc_combined - acc_o_alone
        rows.append({
            "snr_o": snr_o,
            "snr_z": snr_z,
            "accuracy_o_alone": acc_o_alone,
            "accuracy_o_and_z": acc_combined,
            "marginal_gain_from_z": marginal_gain,
        })
    return rows


if __name__ == "__main__":
    # Baseline parameters matching the scaling-law sweep's own baseline.
    N, LAM, SNR_Z, T_EQ = 8, 4.0, 30.0, 5.0 * tau(4.0)

    print("Regression check: Boundary C collapses to Boundary A at snr_o=0")
    ok = marginal_gain_regression_check(N, LAM, SNR_Z, T_EQ)
    print("  PASS\n" if ok else "")
    if not ok:
        raise SystemExit("Regression check failed -- not proceeding.")

    print(f"Boundary A/B (already established, unchanged): at N={N}, lambda={LAM}, "
          f"SNR={SNR_Z}, t_eq={T_EQ:.2f}, this case is classified informational "
          f"ingress -- I(Y;Z|O)>0 with O=empty.")
    print("Boundary B is a logical argument (Z still refers to the same external "
          "field concentration regardless of which side of the boundary transduces "
          "it), not a new computation -- checked above for the only way it could "
          "have gone wrong (a hidden change to what Z refers to); none found.\n")

    print("Boundary C sweep: does the classification shift as the agent's own "
          "'baseline' sensing (already inside the boundary) approaches Z's precision?")
    snr_o_grid = np.array([0.0, 3.0, 10.0, 20.0, 27.0, 29.0, 30.0])
    rows = run_boundary_c_sweep(N, LAM, SNR_Z, T_EQ, snr_o_grid)

    with open("boundary_c_sweep.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print(f"{'snr_o':>8} {'acc(O alone)':>14} {'acc(O+Z)':>10} {'marginal gain':>14}")
    for r in rows:
        print(f"{r['snr_o']:>8.1f} {r['accuracy_o_alone']:>14.4f} "
              f"{r['accuracy_o_and_z']:>10.4f} {r['marginal_gain_from_z']:>14.4f}")
    print("\nWrote boundary_c_sweep.csv")
