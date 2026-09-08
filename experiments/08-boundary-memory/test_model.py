import random

from model import TARGET_SIZE, Tissue, amputate, inhibitor, reference_tissue, relax


def test_unilateral_boundary_memory_restores_exact_reference():
    reference = reference_tissue()
    for side in ("left", "right"):
        for width in (1, 4, 8, 12, 18):
            final, operations = relax(
                amputate(reference, **{side: width}), random.Random(width),
            )
            assert final == reference
            assert operations == width
            assert final.left_sealed and final.right_sealed


def test_boundary_memory_ablation_preserves_size_not_position():
    reference = reference_tissue()
    final, _ = relax(
        amputate(reference, right=8), random.Random(0), use_boundary_memory=False,
    )
    assert final.size == TARGET_SIZE
    assert final != reference


def test_size_signal_clamp_blocks_regrowth_even_with_wound_memory():
    damaged = amputate(reference_tissue(), right=8)
    final, operations = relax(
        damaged, random.Random(0), clamp_signal=inhibitor(TARGET_SIZE),
    )
    assert final.size == TARGET_SIZE - 8
    assert operations == 0


def test_boundary_memory_without_size_signal_overgrows_wound_side():
    damaged = amputate(reference_tissue(), right=8)
    final, operations = relax(damaged, random.Random(0), secretion=0.0, max_steps=50)
    assert operations == 50
    assert final.size == TARGET_SIZE - 8 + 50
    assert final.left == reference_tissue().left


def test_bilateral_damage_recovers_size_but_not_always_position():
    reference = reference_tissue()
    final, _ = relax(
        amputate(reference, left=2, right=6), random.Random(0),
    )
    assert final.size == TARGET_SIZE
    assert final != reference


def test_resealed_boundary_supports_repeated_opposite_side_damage():
    tissue = reference_tissue()
    for side, width in (("right", 8), ("left", 6), ("right", 12), ("left", 4)):
        tissue = amputate(tissue, **{side: width})
        tissue, _ = relax(tissue, random.Random(1))
        assert tissue == reference_tissue()
        assert tissue.left_sealed and tissue.right_sealed


def test_controller_repairs_translated_tissue_without_reference_coordinate():
    reference = Tissue(40, 63)
    for side in ("left", "right"):
        final, _ = relax(amputate(reference, **{side: 8}), random.Random(0))
        assert final == reference
