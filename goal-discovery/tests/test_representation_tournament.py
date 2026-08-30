from pathlib import Path

import pytest

from src.experiments.representation_tournament.tournament import (
    classify_tournament,
    load_scores,
    run,
    score_decision,
)


def test_frozen_decision_statistics() -> None:
    improvement, action = score_decision(
        candidate=0.4, null=0.5, threshold=0.20, metric_direction="lower"
    )
    assert improvement == pytest.approx(0.20)
    assert action == "select"

    improvement, action = score_decision(
        candidate=0.71, null=0.56, threshold=0.10, metric_direction="higher"
    )
    assert improvement == pytest.approx(0.15)
    assert action == "select"


@pytest.mark.parametrize(
    ("correct", "expected"), [(4, "pass"), (3, "partial"), (2, "partial"), (1, "fail")]
)
def test_tournament_classification(correct: int, expected: str) -> None:
    assert classify_tournament(correct) == expected


def test_repository_compact_evidence_has_four_decisions() -> None:
    try:
        scores, hashes = load_scores()
    except FileNotFoundError:
        pytest.skip("Regenerable compact results are absent from this checkout")

    assert list(scores["family"]) == [
        "temporal", "relational", "identity-conditioned", "network"
    ]
    assert len(hashes) == 4


def test_runner_writes_decision_surface(tmp_path: Path) -> None:
    try:
        summary = run(tmp_path)
    except FileNotFoundError:
        pytest.skip("Regenerable compact results are absent from this checkout")

    assert summary["n_tasks"] == 4
    assert (tmp_path / "scores.csv").is_file()
    assert (tmp_path / "summary.json").is_file()
    assert (tmp_path / "decision.png").is_file()
