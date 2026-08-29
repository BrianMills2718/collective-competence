import numpy as np
import pandas as pd

from src.spikes.netlogo_slime_network.analyze import Field, field_to_network
from src.spikes.netlogo_slime_network.analyze_p5_002 import _contrasts


def test_field_to_network_recovers_a_connected_food_path() -> None:
    cp = np.zeros((201, 201), dtype=float)
    wall = np.zeros_like(cp, dtype=bool)
    food = np.zeros_like(cp, dtype=bool)
    cp[98:103, 30:171] = 1.0
    food[99:102, 28:31] = True
    food[99:102, 170:173] = True

    surface = field_to_network(Field(cp=cp, wall=wall, food=food))

    assert surface.metrics["food_components"] == 2
    assert surface.metrics["connected"] is True
    assert surface.metrics["organization_score"] > 0.8
    assert surface.metrics["skeleton_length"] > 100


def test_field_to_network_reports_disconnected_food() -> None:
    cp = np.zeros((201, 201), dtype=float)
    wall = np.zeros_like(cp, dtype=bool)
    food = np.zeros_like(cp, dtype=bool)
    cp[98:103, 30:70] = 1.0
    cp[98:103, 130:171] = 1.0
    food[99:102, 28:31] = True
    food[99:102, 170:173] = True

    surface = field_to_network(Field(cp=cp, wall=wall, food=food))

    assert surface.metrics["connected"] is False
    assert surface.metrics["organization_score"] == 0.0


def test_p5_002_gate_recognizes_stability_plasticity_tradeoff() -> None:
    records = []
    for seed in range(801, 807):
        for boost, sham, near, far in (
            (0, 0.30, 0.30, 0.30),
            (40, 0.65, 0.45, 0.40),
            (80, 0.85, 0.35, 0.30),
        ):
            for arm, score in (("sham", sham), ("near", near), ("far", far)):
                records.append(
                    {
                        "arm": arm,
                        "boost": boost,
                        "seed": seed,
                        "organization_score": score,
                        "skeleton_length": 100,
                        "food_components": 2,
                    }
                )
    _, summary = _contrasts(pd.DataFrame(records))

    assert summary["confirmed"] is True
    assert summary["stability_gate"] is True
    assert summary["geometries"]["near"]["geometry_gate"] is True
    assert summary["geometries"]["far"]["geometry_gate"] is True
