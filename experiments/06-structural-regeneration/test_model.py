from model import (
    TARGET, TARGET_LEFT, TARGET_RIGHT, TARGET_SIZE,
    amputate, edge_signature, grow, policy_gate, ratio_accepts, relative_position, seed_state,
)


def test_target_is_24_site_central_band():
    assert TARGET_SIZE == 24
    assert (TARGET_LEFT, TARGET_RIGHT) == (20, 43)


def test_ratio_formation_is_common_mode_invariant():
    for amplitude in (0.75, 1.0, 1.25):
        final, _ = grow(seed_state(), policy_gate("ratio", amplitude, amplitude))
        assert final == TARGET


def test_single_gradient_matches_only_at_calibration_amplitude():
    baseline, _ = grow(seed_state(), policy_gate("single", 1.0, 1.0))
    low, _ = grow(seed_state(), policy_gate("single", 0.75, 0.75))
    high, _ = grow(seed_state(), policy_gate("single", 1.25, 1.25))
    assert baseline == TARGET
    assert low != TARGET
    assert high != TARGET


def test_ratio_repairs_all_declared_amputations_under_common_mode_change():
    for amplitude in (0.75, 1.0, 1.25):
        for kind in ("left", "right", "middle"):
            for width in (4, 8, 12):
                final, births = grow(amputate(kind, width), policy_gate("ratio", amplitude, amplitude))
                assert final == TARGET
                assert births == width


def test_local_occupancy_cannot_distinguish_normal_edge_from_wound_edge():
    normal = edge_signature(TARGET, TARGET_RIGHT)
    wounded = amputate("right", 8)
    wound = edge_signature(wounded, TARGET_RIGHT - 8)
    assert normal == wound == (1, 1, 0)


def test_ungated_growth_cannot_stop_at_target_boundary():
    final, _ = grow(amputate("right", 8), policy_gate("ungated"))
    assert len(final) == 64
    assert final != TARGET


def test_ratio_encoding_has_differential_source_boundary():
    balanced, _ = grow(amputate("right", 8), policy_gate("ratio", 1.0, 1.0))
    imbalanced, _ = grow(amputate("right", 8), policy_gate("ratio", 1.0, 2.0))
    ablated, _ = grow(amputate("right", 8), policy_gate("ratio", 1.0, 0.0))
    assert balanced == TARGET
    assert imbalanced != TARGET
    assert ablated != TARGET


def test_no_signal_does_not_mean_middle():
    assert relative_position(32, 0.0, 0.0) is None
    assert not ratio_accepts(32, 0.0, 0.0)


def test_any_single_surviving_target_cell_can_regenerate_but_zero_cells_cannot():
    gate = policy_gate("ratio", 1.0, 1.0)
    for survivor in TARGET:
        final, births = grow({survivor}, gate)
        assert final == TARGET
        assert births == TARGET_SIZE - 1
    final, births = grow(set(), gate)
    assert final == frozenset()
    assert births == 0
