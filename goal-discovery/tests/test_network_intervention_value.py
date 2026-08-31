from __future__ import annotations

import pandas as pd
import pytest

from src.experiments.network_intervention_value.audit import SOURCE, analyze, evaluate


def _pairs(degree_burden: int) -> pd.DataFrame:
    rows = []
    for budget in (10, 20):
        for index, run in enumerate((*range(1, 9), *range(14, 22))):
            rows.append(
                {
                    "run": run,
                    "seed": 10000 + run,
                    "split": "discovery" if index < 8 else "confirmation",
                    "budget": budget,
                    "random_burden": 100,
                    "degree_burden": degree_burden,
                    "paired_effect": 100 - degree_burden,
                    "random_extinct": False,
                    "degree_extinct": True,
                }
            )
    return pd.DataFrame(rows)


def test_frozen_gate_promotes_consistent_large_causal_value() -> None:
    summary = evaluate(_pairs(70), {"complete": True})
    assert summary["decision"] == "measured-retrospective-pass"
    assert summary["causal_gate"]
    assert summary["degree_seed_wins"] == {"10": 16, "20": 16}


def test_frozen_gate_evidence_closes_small_or_inconsistent_value() -> None:
    pairs = _pairs(90)
    pairs.loc[(pairs["budget"] == 20) & (pairs["split"] == "confirmation"), "paired_effect"] = -1
    summary = evaluate(pairs, {"complete": True})
    assert summary["decision"] == "evidence-closed-no-go"
    assert not summary["causal_gate"]


def test_integrity_failure_stops_even_if_effect_gate_would_pass() -> None:
    summary = evaluate(_pairs(50), {"complete": False})
    assert summary["decision"] == "integrity-stop"
    assert not summary["integrity_pass"]


def test_finalized_audit_refuses_a_second_contrast(tmp_path) -> None:
    (tmp_path / "summary.json").write_text("{}", encoding="utf-8")
    with pytest.raises(FileExistsError, match="already finalized"):
        analyze(source=SOURCE, output=tmp_path)
