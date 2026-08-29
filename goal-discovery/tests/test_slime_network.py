import numpy as np

from src.spikes.netlogo_slime_network.analyze import Field, field_to_network


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
