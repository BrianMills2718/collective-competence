from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.experiments.relational_flocking.analysis import VECTOR_COLUMNS, add_readouts, discover, evaluate


def _discovery_fixture(relational: bool = True) -> pd.DataFrame:
    rows = []
    for run in range(1, 13):
        state = np.array([0.2 + run / 100, 0.8, -0.1, 0.9 - run / 200], dtype=float)
        for tick in range(201):
            rows.append({"arm": "discovery", "run_number": run, "tick": tick, **dict(zip(VECTOR_COLUMNS, state))})
            if relational:
                state = np.array(
                    [
                        0.96 * state[0] + 0.03 * state[2],
                        0.96 * state[1] + 0.03 * state[3],
                        0.02 * state[0] + 0.97 * state[2],
                        0.02 * state[1] + 0.97 * state[3],
                    ]
                )
            else:
                state = state.copy()
    return pd.DataFrame(rows)


def test_discovery_selects_transferable_relational_law() -> None:
    candidate = discover(_discovery_fixture())
    assert candidate["proposal_adequate"] is True
    assert candidate["selected_family"] == "relational_affine"
    assert candidate["relational_holdout_wins"] >= 5


def test_discovery_rejects_invariant_fixture() -> None:
    candidate = discover(_discovery_fixture(relational=False))
    assert candidate["proposal_adequate"] is False
    assert candidate["selected_family"] == "none"


def test_readouts_use_fixed_cohorts_and_absolute_heading() -> None:
    frame = pd.DataFrame(
        [{"a_dx": 1.0, "a_dy": 0.0, "b_dx": -1.0, "b_dy": 0.0, "all_dx": 0.0, "all_dy": 1.0}]
    )
    result = add_readouts(frame)
    assert result.loc[0, "cohort_gap"] == pytest.approx(180)
    assert result.loc[0, "absolute_heading"] == pytest.approx(0)


def test_evaluation_refuses_failed_candidate() -> None:
    with pytest.raises(ValueError, match="proposal failed"):
        evaluate(pd.DataFrame(), {"proposal_adequate": False})
