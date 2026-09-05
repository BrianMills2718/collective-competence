"""Analytic fixed points for effective information, coarse-graining, and capacity.

Every assertion here is a value that can be derived on paper, which is the point:
Q1-008 found two experiments built on a statistic whose null had never been
computed. A measure whose known values have not been checked is not an
instrument.
"""

from __future__ import annotations

import numpy as np
import pytest

from src.experiments.q1_information.measures import (
    blahut_arimoto,
    coarse_grain,
    effective_information,
    tpm_from_transitions,
)


def test_deterministic_bijection_reaches_the_maximum():
    """A permutation matrix: every state fixes its successor. EI = log2(n)."""
    for n in (2, 4, 8, 16):
        perm = np.eye(n)[np.random.default_rng(n).permutation(n)]
        assert effective_information(perm) == pytest.approx(np.log2(n))


def test_uniform_rows_carry_nothing():
    """No state constrains its successor. EI = 0."""
    for n in (2, 5, 9):
        assert effective_information(np.full((n, n), 1.0 / n)) == pytest.approx(0.0)


def test_determinism_alone_is_not_structure():
    """Every state maps to one fixed state: fully deterministic, EI = 0.

    The non-obvious fixed point. A successor that is certain regardless of the
    predecessor carries no information about it, so EI measures constraint, not
    predictability -- which is exactly why it can disagree with the prediction-
    based statistics used elsewhere in this repository.
    """
    for n in (3, 6):
        allto = np.zeros((n, n))
        allto[:, 1] = 1.0
        assert effective_information(allto) == pytest.approx(0.0)


def test_binary_symmetric_channel_matches_its_closed_form():
    """Capacity of a BSC with crossover p is 1 - H(p) bits."""
    for p in (0.01, 0.1, 0.25):
        h = -p * np.log2(p) - (1 - p) * np.log2(1 - p)
        chan = np.array([[1 - p, p], [p, 1 - p]])
        assert blahut_arimoto(chan) == pytest.approx(1.0 - h, abs=1e-6)


def test_a_channel_that_ignores_its_input_has_zero_capacity():
    assert blahut_arimoto(np.array([[0.5, 0.5], [0.5, 0.5]])) == pytest.approx(0.0)


def test_identity_grouping_changes_nothing():
    """Coarse-graining each state into its own group must be a no-op."""
    rng = np.random.default_rng(7)
    tpm = rng.dirichlet(np.ones(5), size=5)
    macro, seen = coarse_grain(tpm, np.arange(5))
    assert np.allclose(macro, tpm)
    assert effective_information(macro, rows_seen=seen) == pytest.approx(
        effective_information(tpm)
    )


def test_grouping_everything_into_one_state_destroys_all_information():
    rng = np.random.default_rng(11)
    tpm = rng.dirichlet(np.ones(6), size=6)
    macro, seen = coarse_grain(tpm, np.zeros(6, dtype=int))
    assert effective_information(macro, rows_seen=seen) == pytest.approx(0.0)


def test_macro_rows_are_uniform_not_frequency_weighted_averages():
    """The intervention forces group members equiprobably.

    Weighting by how often a micro state is *observed* would put the
    observational distribution back into an interventional measure, which is the
    error this whole module exists to avoid.
    """
    tpm = np.array([[1.0, 0.0], [0.0, 1.0]])
    macro, _ = coarse_grain(tpm, np.array([0, 0]))
    assert macro[0, 0] == pytest.approx(1.0)


def test_equal_sized_groups_can_never_show_emergence():
    """A constraint on the measure, found by searching for a counterexample.

    When every group has the same size, a uniform intervention on micro states
    induces a uniform distribution on macro states, and macro is a deterministic
    function of micro on both sides. Data processing then bounds
    I(M;M') <= I(S;S'), so EI cannot rise. Measured: across 80,000 random
    4-state systems at four concentrations, the best macro-minus-micro gain was
    negative in every regime.

    This is why Q1-009 coarse-grains by *count of units acting*, whose group
    sizes are the binomial coefficients and therefore strongly unequal. A
    balanced coarse-graining would have made the experiment unable to report the
    phenomenon it was run to look for.
    """
    rng = np.random.default_rng(0)
    groups = np.array([0, 0, 1, 1])
    best = -np.inf
    for alpha in (0.1, 1.0):
        for _ in range(5000):
            tpm = rng.dirichlet(np.ones(4) * alpha, size=4)
            macro, seen = coarse_grain(tpm, groups)
            best = max(
                best,
                effective_information(macro, rows_seen=seen) - effective_information(tpm),
            )
    assert best <= 0.0, f"equal groups produced emergence of {best}"


def test_the_emergence_measure_is_capable_of_reporting_emergence():
    """Negative control: a measure that can never fire is decoration.

    Uses unequal group sizes, which is the regime where the bound above does not
    apply. If this ever fails, coarse_grain or effective_information has become
    structurally unable to report the phenomenon Q1-009 exists to detect.
    """
    rng = np.random.default_rng(0)
    groups = np.array([0, 1, 1, 1])
    best = -np.inf
    for _ in range(5000):
        tpm = rng.dirichlet(np.ones(4) * 0.1, size=4)
        macro, seen = coarse_grain(tpm, groups)
        best = max(
            best,
            effective_information(macro, rows_seen=seen) - effective_information(tpm),
        )
        if best > 0:
            break
    assert best > 0, f"no unequal coarse-graining raised EI; best was {best}"


def test_estimated_tpm_counts_transitions_and_flags_unvisited_rows():
    pairs = np.array([[0, 1], [0, 1], [1, 0], [1, 1]])
    tpm, seen, totals = tpm_from_transitions(pairs, n_states=3)
    assert tpm[0, 1] == pytest.approx(1.0)
    assert tpm[1, 0] == pytest.approx(0.5)
    assert seen.tolist() == [True, True, False]
    assert totals.tolist() == [2.0, 2.0, 0.0]


@pytest.mark.parametrize(
    "n_pairs,at_least,at_most",
    [(200, 2.0, 3.5), (1000, 0.5, 1.2), (8000, 0.02, 0.2), (40000, 0.001, 0.05)],
)
def test_finite_sample_effective_information_is_biased_upward(n_pairs, at_least, at_most):
    """The reason no absolute EI threshold in Q1-009 is interpretable.

    A structureless independent process has true EI = 0. The estimate does not,
    for the same reason mean |r| of independent series is positive at finite
    sample (Q1-008): sparsely-visited rows look deterministic. Measured on 32
    states, the bias is *half the theoretical maximum* at 6 transitions per row:

        transitions/row      6.2    15.6    31.2    62.5    250    1250
        estimated EI        2.49    1.41    0.79    0.39    0.08   0.017
        (true value 0, maximum log2(32) = 5.0)

    So an EI number is meaningless without its sample density, and Q1-009 must
    both run enough transitions per row and measure the null anyway. This test
    pins the decay so a future change that quietly reduces sample density cannot
    pass unnoticed.
    """
    rng = np.random.default_rng(23)
    n_states = 32
    pairs = rng.integers(0, n_states, size=(n_pairs, 2))
    tpm, seen, _ = tpm_from_transitions(pairs, n_states)
    estimated = effective_information(tpm, rows_seen=seen)
    assert at_least <= estimated <= at_most, (n_pairs, estimated)


def test_capacity_refuses_a_channel_with_an_unobserved_input():
    """An all-zero row used to inflate capacity above its true value.

    Left in, an unobserved input's unnormalised weight is exp(0) = 1 -- the
    maximum -- so it dominates the capacity-achieving distribution. Measured
    before the guard: [[1,0],[0,1],[0,0]] returned 1.0566 bits against a true
    capacity of log2(2) = 1.0 over the two usable inputs.
    """
    with pytest.raises(ValueError, match="no observations"):
        blahut_arimoto(np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]]))
    assert blahut_arimoto(np.array([[1.0, 0.0], [0.0, 1.0]])) == pytest.approx(1.0)


def test_effective_information_refuses_an_unvisited_row_rather_than_scoring_it_zero():
    """In an estimated TPM an all-zero row is an unvisited state, not a dead end.

    Averaging it into pbar and scoring it 0 returns a quietly wrong number.
    Measured before the guard: a 3-state TPM whose state 2 was never visited
    returned 1.0566 instead of the correct 1.0.
    """
    tpm = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 0.0]])
    with pytest.raises(ValueError, match="no outgoing mass"):
        effective_information(tpm)
    seen = np.array([True, True, False])
    assert effective_information(tpm, rows_seen=seen) == pytest.approx(1.0)
