from __future__ import annotations

import pandas as pd

from src.experiments.distributed_prediction.analyze import (
    MODEL_FAMILIES,
    cross_validated_predictions,
    cross_validated_scores,
    error_audit,
)
from src.experiments.distributed_prediction.batch import (
    DISCOVERY,
    HOLDOUT,
    BatchDesign,
    generate_batch,
)
from src.experiments.distributed_prediction.reachability import (
    barrier_feasible,
    moveable_order_feasible,
    selected_positions_cross_an_inversion,
)
from src.experiments.distributed_prediction.reachability import (
    decide as decide_reachability,
)
from src.experiments.distributed_prediction.reachability import (
    generate_cases as generate_reachability_cases,
)
from src.experiments.distributed_prediction.relational import (
    RELATIONAL_FEATURES,
    relational_features,
)
from src.experiments.distributed_prediction.targeted import (
    DAMAGE_CONDITIONS,
    TARGETED_DISCOVERY,
    TARGETED_HOLDOUT,
    eligibility,
)


def test_frozen_batches_have_144_branches_and_new_size_and_seeds() -> None:
    assert DISCOVERY.branches == 144
    assert HOLDOUT.branches == 144
    assert DISCOVERY.n == 12
    assert HOLDOUT.n == 24
    assert set(DISCOVERY.seeds).isdisjoint(HOLDOUT.seeds)
    assert DISCOVERY.schedules == HOLDOUT.schedules == ("index", "shuffled")


def test_targeted_batches_have_72_branches_and_only_ambiguous_damage() -> None:
    assert TARGETED_DISCOVERY.branches == 72
    assert TARGETED_HOLDOUT.branches == 72
    assert TARGETED_DISCOVERY.damage_pairs == DAMAGE_CONDITIONS
    assert TARGETED_HOLDOUT.damage_pairs == DAMAGE_CONDITIONS
    assert set(TARGETED_DISCOVERY.seeds).isdisjoint(DISCOVERY.seeds)
    assert set(TARGETED_HOLDOUT.seeds).isdisjoint(TARGETED_DISCOVERY.seeds)


def test_targeted_eligibility_requires_both_outcomes_in_all_six_strata() -> None:
    rows = []
    for schedule in ("index", "shuffled"):
        for mode, count in DAMAGE_CONDITIONS:
            for outcome in (False, True):
                rows.append(
                    {
                        "activation_schedule": schedule,
                        "freeze_mode": mode,
                        "freeze_count": count,
                        "reached_goal": outcome,
                        "pre_sorted": False,
                    }
                )
    passed = eligibility(pd.DataFrame(rows))
    assert passed["passed"]
    rows[-1]["reached_goal"] = False
    failed = eligibility(pd.DataFrame(rows))
    assert not failed["passed"]
    assert not failed["criteria"]["all_six_strata_mixed"]


def test_small_crossed_batch_is_deterministic_and_observation_complete() -> None:
    design = BatchDesign(
        "test",
        8,
        (11, 12),
        schedules=("index",),
        branch_fractions=(0.0,),
        freeze_modes=("moveable", "immovable"),
        freeze_counts=(1,),
        horizon_ticks=80,
    )
    first_runs, first_traces = generate_batch(design)
    second_runs, second_traces = generate_batch(design)
    pd.testing.assert_frame_equal(first_runs, second_runs)
    pd.testing.assert_frame_equal(first_traces, second_traces)

    assert len(first_runs) == 4
    assert first_runs["run_id"].is_unique
    assert not first_runs["pre_sorted"].any()
    assert (
        first_traces.groupby("run_id")["phase"]
        .agg(set)
        .map(lambda phases: {"pre_branch", "post_branch"} <= phases)
        .all()
    )
    assert first_runs["values_json"].str.startswith("[").all()
    assert first_runs["freeze_modes_json"].str.contains("moveable|immovable").all()


def test_model_contract_is_compact_and_contains_no_future_features() -> None:
    capability = MODEL_FAMILIES["Capability-aware macro"]
    micro = MODEL_FAMILIES["Observable-micro baseline"]
    assert len(capability) == 9
    assert len(micro) == 36
    assert len(capability) <= len(micro) / 4
    for features in MODEL_FAMILIES.values():
        assert not any(
            token in feature
            for feature in features
            for token in ("final", "outcome", "reached_goal", "time_to_goal")
        )


def test_relational_candidate_is_compact_and_detects_blocked_inversions() -> None:
    features = relational_features([2, 1, 0], ["none", "immovable", "none"])
    assert len(RELATIONAL_FEATURES) == 9
    assert features["rel_frozen_displacement_mean"] == 0
    assert features["rel_largest_frozen_block_fraction"] == 1 / 3
    assert features["rel_active_frozen_interface_fraction"] == 1
    assert features["rel_immovable_crossing_inversion_fraction"] == 1

    moveable = relational_features([2, 1, 0], ["moveable", "moveable", "none"])
    assert moveable["rel_largest_frozen_block_fraction"] == 2 / 3
    assert moveable["rel_immovable_crossing_inversion_fraction"] == 0


def test_barrier_rule_detects_exactly_when_an_inversion_crosses_a_barrier() -> None:
    assert barrier_feasible([0, 1, 2], ["none", "immovable", "none"])
    assert not barrier_feasible([2, 1, 0], ["none", "immovable", "none"])
    assert barrier_feasible([1, 0, 2], ["none", "none", "immovable"])
    assert selected_positions_cross_an_inversion([1, 0, 2], [0])
    assert not selected_positions_cross_an_inversion([1, 0, 2], [2])


def test_moveable_rule_detects_inverted_passive_subsequence() -> None:
    assert moveable_order_feasible([2, 0, 1], [1, 2])
    assert not moveable_order_feasible([2, 0, 1], [0, 2])
    assert moveable_order_feasible([2, 0, 1], [0])


def test_size_three_exhaustive_barrier_screen_passes() -> None:
    frame = generate_reachability_cases(n=3, horizon_per_cell=30)
    assert len(frame) == 6 * 7 * 2 * 2
    decision = decide_reachability(frame)
    assert decision["passed"]
    assert decision["immovable_accuracy"] == 1.0
    assert decision["moveable_specificity_cases"] > 0


def test_grouped_model_screen_returns_finite_scores_for_every_family() -> None:
    records = []
    all_features = sorted({feature for features in MODEL_FAMILIES.values() for feature in features})
    for seed in range(1, 7):
        for outcome in (False, True):
            row = {
                "run_id": f"synthetic-{seed}-{int(outcome)}",
                "seed": seed,
                "activation_schedule": "index",
                "branch_tick": 0,
                "freeze_mode": "moveable",
                "freeze_count": 1,
                "reached_goal": outcome,
                "time_to_goal_per_cell": 1.0 + seed / 100 if outcome else float("nan"),
            }
            row.update(
                {
                    feature: float(outcome) + seed * 0.001 + index * 0.00001
                    for index, feature in enumerate(all_features)
                }
            )
            records.append(row)
    scores = cross_validated_scores(pd.DataFrame(records))
    assert set(scores["representation"]) == set(MODEL_FAMILIES)
    assert scores[["log_loss", "brier_loss", "balanced_accuracy"]].notna().all().all()
    assert scores["n_runs"].eq(12).all()
    predictions = cross_validated_predictions(pd.DataFrame(records))
    assert len(predictions) == 12 * len(MODEL_FAMILIES)
    audit = error_audit(predictions)
    assert len(audit) == 1
    assert "capability_gain" in audit
