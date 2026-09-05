"""Effective information, causal emergence, and interventional empowerment.

Both measures are defined on an *interventional* distribution, not an observed
one. That is the whole point of using them here: this repository's existing
statistics are observational, and Q1-005 and Q1-008 both found observational
statistics measuring something other than what they were chosen for.

Effective information (Hoel; Albantakis; Rosas)
-----------------------------------------------
For a transition probability matrix `T` over `n` states, EI is the mutual
information between successive states when the earlier state is *forced* to the
maximum-entropy distribution rather than observed in its stationary one:

    EI(T) = (1/n) * sum_i D_KL( T[i,:] || pbar )      with pbar = (1/n) sum_i T[i,:]

in bits. Three analytic fixed points pin the implementation, and all three are
asserted in `tests/test_information_measures.py`:

  * a deterministic bijection (permutation matrix) gives EI = log2(n), the
    maximum: every state is perfectly informative about its successor;
  * a matrix whose every row is uniform gives EI = 0: no state constrains its
    successor;
  * a matrix that maps every state to one fixed state gives EI = 0 as well,
    which is the non-obvious one -- determinism alone is not structure, because
    a successor that is certain regardless of the predecessor carries nothing.

Causal emergence is EI(macro) - EI(micro) for a coarse-graining of the same
system. The macro TPM is built by averaging rows uniformly within each group,
which is what the maximum-entropy intervention requires: group members are
forced equiprobably.

Finite-sample warning, which is the reason the null arm exists
--------------------------------------------------------------
EI estimated from a sampled TPM is biased *upward*, for the same reason the mean
absolute correlation of independent series is positive at finite sample
(Q1-008). Sparsely-visited rows look deterministic. An absolute EI value from an
estimated TPM therefore means nothing on its own, and no threshold in this module
is interpretable except against a null estimated at matched dimensions, matched
sample size, and matched sparsity.

Empowerment (Klyubin, Polani, Nehaniv)
--------------------------------------
The channel capacity from a unit's own action to its own later observation,

    E = max_{p(a)} I(A ; O)

which requires no goal criterion at all. Estimating `p(o|a)` from observed play
would be circular, because the policy chooses the action: the channel is measured
here by *forcing* the action at a tick and reading the unit's own next
observation, then taking the capacity of the resulting channel by Blahut-Arimoto.
"""

from __future__ import annotations

import numpy as np

LOG2 = np.log(2.0)


def _safe_row_normalise(counts: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    totals = counts.sum(axis=1, keepdims=True)
    out = np.zeros_like(counts, dtype=float)
    seen = totals[:, 0] > 0
    out[seen] = counts[seen] / totals[seen]
    return out, seen


def effective_information(tpm: np.ndarray, *, rows_seen: np.ndarray | None = None,
                          _allow_unvisited: bool = False) -> float:
    """EI in bits under a uniform intervention on the earlier state.

    `rows_seen` restricts the intervention distribution to states the estimate
    actually covers. Forcing the system into a state never observed would assert
    a transition row that was never measured, so unvisited rows are excluded and
    the exclusion is reported by the caller rather than hidden here.
    """
    tpm = np.asarray(tpm, dtype=float)
    if rows_seen is None:
        # An all-zero row in an ESTIMATED tpm is an unvisited state, not a state
        # with no successors. Averaging it into pbar and scoring it 0 returns a
        # quietly wrong number, so refuse rather than answer.
        empty = ~(tpm > 0).any(axis=1)
        if empty.any() and not _allow_unvisited:
            raise ValueError(
                f"rows {np.flatnonzero(empty).tolist()} have no outgoing mass; pass "
                "rows_seen to exclude unvisited states rather than scoring them as 0"
            )
        rows_seen = np.ones(tpm.shape[0], dtype=bool)
    rows = tpm[rows_seen]
    if rows.shape[0] == 0:
        return 0.0
    pbar = rows.mean(axis=0)
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio = np.where((rows > 0) & (pbar > 0), rows / np.where(pbar > 0, pbar, 1.0), 1.0)
        terms = np.where(rows > 0, rows * np.log(ratio), 0.0)
    return float(terms.sum(axis=1).mean() / LOG2)


def coarse_grain(tpm: np.ndarray, groups: np.ndarray, *,
                 rows_seen: np.ndarray | None = None) -> tuple[np.ndarray, np.ndarray]:
    """Macro TPM by uniform averaging within each group.

    Uniform, not stationary-weighted: the intervention forces group members
    equiprobably, so the macro row must be their unweighted mean. Weighting by
    observed frequency would smuggle the observational distribution back into an
    interventional measure.
    """
    tpm = np.asarray(tpm, dtype=float)
    groups = np.asarray(groups)
    if rows_seen is None:
        rows_seen = np.ones(tpm.shape[0], dtype=bool)
    labels = np.unique(groups)
    macro = np.zeros((labels.size, labels.size))
    macro_seen = np.zeros(labels.size, dtype=bool)
    for a, la in enumerate(labels):
        members = (groups == la) & rows_seen
        if not members.any():
            continue
        macro_seen[a] = True
        rows = tpm[members].mean(axis=0)
        for b, lb in enumerate(labels):
            macro[a, b] = rows[groups == lb].sum()
    return macro, macro_seen


def tpm_from_transitions(pairs: np.ndarray, n_states: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Estimate a TPM by counting. Returns (tpm, rows_seen, row_counts)."""
    counts = np.zeros((n_states, n_states), dtype=float)
    for a, b in pairs:
        counts[int(a), int(b)] += 1.0
    tpm, seen = _safe_row_normalise(counts)
    return tpm, seen, counts.sum(axis=1)


def blahut_arimoto(channel: np.ndarray, *, tol: float = 1e-10, max_iter: int = 5000) -> float:
    """Channel capacity in bits for p(o|a) given as rows indexed by action."""
    channel = np.asarray(channel, dtype=float)
    usable = (channel > 0).any(axis=1)
    if not usable.all():
        # An all-zero row is an input that was never observed. Left in, its
        # unnormalised weight is exp(0) = 1 -- the maximum -- so a never-used action
        # dominates the capacity-achieving distribution and the result can exceed
        # the true capacity over the usable inputs.
        raise ValueError(
            f"channel rows {np.flatnonzero(~usable).tolist()} have no observations; "
            "drop unobserved inputs before taking capacity"
        )
    n_in = channel.shape[0]
    r = np.full(n_in, 1.0 / n_in)
    for _ in range(max_iter):
        q = r[:, None] * channel
        denom = q.sum(axis=0, keepdims=True)
        q = np.divide(q, denom, out=np.zeros_like(q), where=denom > 0)
        with np.errstate(divide="ignore", invalid="ignore"):
            logs = np.where((channel > 0) & (q > 0), channel * np.log(np.where(q > 0, q, 1.0)), 0.0)
        r_new = np.exp(logs.sum(axis=1))
        total = r_new.sum()
        if total <= 0:  # unreachable given the usable-row guard; fail loud, do not fake a capacity
            raise ValueError("Blahut-Arimoto lost all input mass; channel is degenerate")
        r_new /= total
        if np.max(np.abs(r_new - r)) < tol:
            r = r_new
            break
        r = r_new
    py = (r[:, None] * channel).sum(axis=0)
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio = np.where((channel > 0) & (py > 0), channel / np.where(py > 0, py, 1.0), 1.0)
        terms = np.where(channel > 0, channel * np.log(ratio), 0.0)
    return float((r * terms.sum(axis=1)).sum() / LOG2)
