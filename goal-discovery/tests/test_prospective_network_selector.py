from pathlib import Path

import pytest

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
