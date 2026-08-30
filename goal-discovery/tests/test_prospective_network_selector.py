from pathlib import Path

import pandas as pd
import pytest

from src.experiments.prospective_network_selector.audit import (
    EQUAL_CAPACITY_FEATURES,
    _design,
    evaluate,
)
from src.experiments.prospective_network_selector.data import (
    load_dataset,
    parse_edges,
    parse_nodes,
    validate_matched_preintervention,
)


def test_netlogo_node_and_edge_reporters_parse() -> None:
    nodes = parse_nodes("[[0 1.5 -2 true false 3] [1 0 4 false true 1]]")
    assert list(nodes["who"]) == [0, 1]
    assert list(nodes["infected"]) == [True, False]
    assert list(nodes["resistant"]) == [False, True]

    assert parse_edges("[[1 2] [0] [0]]") == [(0, 1), (0, 2)]


def test_real_feasibility_trajectories_are_matched() -> None:
    directory = Path("results/p7-002-network-feasibility")
    if not directory.is_dir():
        pytest.skip("Regenerable Level 0 P7-002 trajectories are absent")
    dataset = load_dataset(
        directory,
        {"baseline": "baseline.csv", "random 10%": "random.csv", "high-degree 10%": "degree.csv"},
    )
    validate_matched_preintervention(dataset)
    assert dataset.max_tick == 100
    assert len(dataset.snapshot("baseline", 1, 20)) == 150


def test_sparse_story_snapshots_never_substitute_a_different_tick() -> None:
    directory = Path("results/p7-002-network-level2")
    if not directory.is_dir():
        pytest.skip("Regenerable Level 2 P7-002 trajectories are absent")
    dataset = load_dataset(
        directory,
        {"baseline": "baseline.csv"},
        run_indices=[1],
        snapshot_stride=5,
    )

    assert 20 in dataset.available_ticks("baseline", 1)
    assert 22 not in dataset.available_ticks("baseline", 1)
    with pytest.raises(KeyError, match="exact snapshot"):
        dataset.snapshot("baseline", 1, 22)


def test_equal_capacity_design_has_four_summaries_and_common_interactions() -> None:
    row = {"fraction": 0.1, "is_random": 1, "is_degree": 0}
    for features in EQUAL_CAPACITY_FEATURES.values():
        row.update({feature: 1.0 for feature in features})
    frame = pd.DataFrame([row])

    assert {len(features) for features in EQUAL_CAPACITY_FEATURES.values()} == {4}
    for family in EQUAL_CAPACITY_FEATURES:
        design = _design(frame, family)
        assert len(design.columns) == 19
        assert list(design.columns[:3]) == ["fraction", "is_random", "is_degree"]


def test_real_p7_003_gate_stops_unstable_generic_selection() -> None:
    source = Path("results/p7-002-network-level2/feature_table.csv")
    if not source.is_file():
        pytest.skip("Regenerable P7-002 feature table is absent")

    summary, outputs = evaluate(pd.read_csv(source))

    assert summary["winner_counts"] == {
        "identity-conditioned": 3,
        "network": 3,
        "temporal": 2,
    }
    assert summary["stable_winner"] is None
    assert summary["gate_passed"] is False
    assert summary["decision"] == "stop-generic-family-selection"
    assert len(outputs["fold_winners"]) == 8
