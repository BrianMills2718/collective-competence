import random
from model import conflicts, hamming, lesion, random_state, settle, step


def test_aware_update_never_increases_global_conflicts():
    for seed in range(30):
        rng=random.Random(seed); colors=random_state(24,rng)
        for _ in range(200):
            before=conflicts(colors); step(colors,rng,"aware"); assert conflicts(colors) <= before


def test_formation_converges_from_random_states():
    for seed in range(50):
        rng=random.Random(seed); colors=random_state(48,rng)
        assert settle(colors,rng,budget=1000) is not None
        assert conflicts(colors) == 0


def test_lesion_is_real_and_repairs():
    rng=random.Random(17); colors=random_state(24,rng); assert settle(colors,rng) is not None
    lesion(colors,5,8); assert conflicts(colors) >= 8
    assert settle(colors,rng) is not None; assert conflicts(colors) == 0


def test_repair_need_not_restore_original_microstate():
    rng=random.Random(0); colors=random_state(24,rng); assert settle(colors,rng) is not None
    original=colors.copy(); lesion(colors,3,8); assert settle(colors,rng) is not None
    assert conflicts(colors) == 0; assert hamming(colors,original) > 0


def test_one_frozen_bad_cell_can_be_routed_around():
    rng=random.Random(3); colors=random_state(24,rng); assert settle(colors,rng) is not None
    i=7; colors[i]=colors[i-1]
    assert settle(colors,rng,frozen=frozenset({i})) is not None


def test_two_adjacent_frozen_equal_cells_make_criterion_impossible():
    rng=random.Random(4); colors=random_state(24,rng); assert settle(colors,rng) is not None
    colors[7]=colors[8]=0
    assert settle(colors,rng,budget=2000,frozen=frozenset({7,8})) is None
    assert colors[7] == colors[8]
