from model import (
    TARGET,
    damage,
    oracle_lineage_repair,
    oracle_plastic_repair,
    total_only_exact_probability,
)


def test_partial_single_side_repairs_with_lineage():
    assert oracle_lineage_repair(damage(4, 0)).cells == TARGET
    assert oracle_lineage_repair(damage(0, 8)).cells == TARGET


def test_partial_bilateral_repairs_with_perfect_composition_information():
    for left, right in ((2, 6), (4, 4), (4, 8), (7, 8)):
        assert oracle_lineage_repair(damage(left, right)).cells == TARGET


def test_total_only_probability_is_nontrivial_for_partial_bilateral_damage():
    assert total_only_exact_probability(damage(2, 6)) == 28 / 256
    assert total_only_exact_probability(damage(4, 4)) == 70 / 256


def test_perfect_information_cannot_restore_extinct_lineage_without_plasticity():
    for left, right in ((8, 0), (0, 16), (8, 4), (4, 16)):
        assert oracle_lineage_repair(damage(left, right)).cells != TARGET
        assert oracle_plastic_repair(damage(left, right)).cells == TARGET


def test_zero_survivors_blocks_parent_dependent_regrowth_even_with_plasticity():
    state = damage(8, 16)
    assert state.cells == ()
    assert oracle_plastic_repair(state).cells == ()


def test_target_is_translation_free_internal_pattern():
    assert TARGET == ("A",) * 8 + ("B",) * 16
