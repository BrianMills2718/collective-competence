from __future__ import annotations

import pandas as pd
import pytest

from src.spikes.morpheus_neuromast.analyze import SEEDS, score
from src.spikes.morpheus_neuromast.model import transform_model


@pytest.fixture
def miniature_model() -> str:
    return """<MorpheusModel version="4">
<Global>
<Variable symbol="pm" value="0.0001"/>
<Variable symbol="ps" value="0.00015"/>
</Global>
<CellTypes>
<CellType name="mantle"><CellDivision><Condition>Mantle_Neighbours &lt; umbral</Condition></CellDivision></CellType>
<CellType name="sustentacular">
<CellDivision><Condition>Sustentacular_Neighbours &lt; umbral</Condition></CellDivision>
<CellDivision><Condition>Sustentacular_Neighbours &lt; umbral</Condition></CellDivision>
</CellType>
</CellTypes>
<Analysis>
<Gnuplotter><Plot/></Gnuplotter>
<ModelGraph format="dot"/>
        <Logger time-step="1" name="number_cell_vs_time">
            <Input><Symbol symbol-ref="total_cells"/></Input>
</Logger>
</Analysis>
</MorpheusModel>"""


def test_active_transform_only_instruments(miniature_model: str) -> None:
    transformed, report = transform_model(miniature_model, "active")
    assert 'time-step="5000"' in transformed
    assert 'symbol-ref="cell.center.x"' in transformed
    assert "Gnuplotter" not in transformed
    assert "ModelGraph" not in transformed
    assert "Mantle_Neighbours &lt; umbral" in transformed
    assert 'symbol="pm" value="0.0001"' in transformed
    assert report.feedback_terms_disabled == 0
    assert report.probabilities_disabled == 0


def test_feedback_disabled_transform_changes_three_predicates(miniature_model: str) -> None:
    transformed, report = transform_model(miniature_model, "feedback_disabled")
    assert "Neighbours &lt; umbral" not in transformed
    assert transformed.count("1 == 1") == 3
    assert report.feedback_terms_disabled == 3


def test_proliferation_disabled_transform_changes_two_probabilities(
    miniature_model: str,
) -> None:
    transformed, report = transform_model(miniature_model, "proliferation_disabled")
    assert 'symbol="pm" value="0"' in transformed
    assert 'symbol="ps" value="0"' in transformed
    assert report.probabilities_disabled == 2


def _passing_metrics() -> pd.DataFrame:
    rows = []
    for seed in SEEDS:
        rows.extend(
            [
                {
                    "condition": "active",
                    "seed": seed,
                    "initial_total": 5,
                    "final_total": 52,
                    "final_macro_distance": 0.08,
                    "late_growth": 0.04,
                    "final_radial_order": 0.82,
                },
                {
                    "condition": "feedback_disabled",
                    "seed": seed,
                    "initial_total": 5,
                    "final_total": 80,
                    "final_macro_distance": 0.70,
                    "late_growth": 0.30,
                    "final_radial_order": 0.60,
                },
                {
                    "condition": "proliferation_disabled",
                    "seed": seed,
                    "initial_total": 5,
                    "final_total": 5,
                    "final_macro_distance": 0.95,
                    "late_growth": 0.00,
                    "final_radial_order": 0.75,
                },
            ]
        )
    return pd.DataFrame(rows)


def test_score_promotes_only_when_all_frozen_checks_pass() -> None:
    decision = score(_passing_metrics())
    assert decision["decision"] == "promote"
    assert all(decision["checks"].values())


def test_score_rejects_endpoint_hit_without_boundedness() -> None:
    metrics = _passing_metrics()
    metrics.loc[metrics.condition == "active", "late_growth"] = 0.25
    decision = score(metrics)
    assert decision["decision"] == "no-go"
    assert decision["checks"]["active_distance_advantage"]
    assert not decision["checks"]["active_late_growth"]
