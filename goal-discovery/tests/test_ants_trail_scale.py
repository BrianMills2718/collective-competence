from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree

import numpy as np
import pandas as pd

from src.experiments.ants_trail_scale.analyze import (
    SCALE_FEATURES,
    PatchField,
    score,
    trail_metrics,
)


def test_trail_metrics_distinguish_connected_and_cut_paths() -> None:
    chemical = np.zeros((7, 7), dtype=float)
    chemical[3, :] = 1.0
    food = np.zeros((7, 7), dtype=float)
    food[3, 6] = 1.0
    nest = np.zeros((7, 7), dtype=bool)
    nest[3, 0] = True
    source = np.zeros((7, 7), dtype=int)
    source[3, 6] = 1
    connected = trail_metrics(PatchField(chemical, food, nest, source, 0, 6))

    chemical[3, 3] = 0
    cut = trail_metrics(PatchField(chemical, food, nest, source, 0, 6))

    assert connected["source_connection_fraction_330"] == 1.0
    assert cut["source_connection_fraction_330"] == 0.0
    assert connected["mean_source_path_330"] < cut["mean_source_path_330"]


def test_frozen_behaviorspace_has_only_the_declared_field_cut() -> None:
    path = Path("src/experiments/ants_trail_scale/behaviorspace.xml")
    root = ElementTree.parse(path).getroot()
    experiments = {item.attrib["name"]: item for item in root.findall("experiment")}

    assert set(experiments) == {"p7-004-sham", "p7-004-trail-cut"}
    assert all(item.attrib["repetitions"] == "8" for item in experiments.values())
    assert all(item.attrib["timeLimit"] == "600" for item in experiments.values())
    sham_go = experiments["p7-004-sham"].findtext("go")
    cut_go = experiments["p7-004-trail-cut"].findtext("go")
    assert sham_go == "go"
    assert cut_go is not None
    assert cut_go.count("set chemical 0") == 1
    assert "distancexy 0 0 >= 8 and distancexy 0 0 < 13" in cut_go


def test_frozen_score_can_promote_only_the_decisive_scale() -> None:
    rows = []
    for seed_index, seed in enumerate(range(1101, 1109)):
        for arm in ("sham", "trail_cut"):
            signal = float(seed_index + (arm == "trail_cut") * 0.25)
            row = {
                "arm": arm,
                "seed": seed,
                "arm_cut": float(arm == "trail_cut"),
                "food_300": 100.0,
                "food_330": 100.0,
                "future_collection": 5.0 + 8.0 * signal,
                "persistence_prediction": 20.0,
            }
            for column in SCALE_FEATURES["local"] + SCALE_FEATURES["colony"]:
                row[column] = float((seed_index * 3 + len(column)) % 2)
            row[SCALE_FEATURES["trail"][0]] = signal
            for column in SCALE_FEATURES["trail"][1:]:
                row[column] = 0.0
            rows.append(row)

    predictions, seed_errors, summary = score(pd.DataFrame(rows))

    assert predictions.notna().all().all()
    assert len(seed_errors) == 8
    assert summary["decision"] == "promote-mesoscopic-trail"
    assert summary["mesoscopic_pass"] is True
