import random

from model import (
    TARGET_SIZE, Tissue, add_right, amputate_right, discrimination_margin,
    inhibitor, reference_tissue, relax, thresholds,
)


def test_target_size_is_unique_quiet_size():
    low, high = thresholds()
    assert inhibitor(TARGET_SIZE - 1) < low
    assert low < inhibitor(TARGET_SIZE) < high
    assert inhibitor(TARGET_SIZE + 1) > high


def test_development_from_one_cell_stops_at_target_size():
    final, operations = relax(Tissue(100, 100), random.Random(0))
    assert final.size == TARGET_SIZE
    assert operations == TARGET_SIZE - 1


def test_loss_and_excess_both_return_to_target_size():
    for width in (1, 4, 8, 12, 18):
        repaired, births = relax(amputate_right(width), random.Random(width))
        reduced, deaths = relax(add_right(width), random.Random(width))
        assert repaired.size == TARGET_SIZE
        assert reduced.size == TARGET_SIZE
        assert births == deaths == width


def test_size_recovery_does_not_imply_position_recovery():
    final, _ = relax(amputate_right(8), random.Random(0))
    assert final.size == TARGET_SIZE
    assert final != reference_tissue()


def test_pre_damage_signal_clamp_prevents_regrowth():
    amputated = amputate_right(8)
    clamped, operations = relax(
        amputated, random.Random(0), clamp_signal=inhibitor(TARGET_SIZE),
    )
    assert clamped == amputated
    assert operations == 0


def test_inhibitor_ablation_loses_growth_stop():
    final, operations = relax(
        amputate_right(8), random.Random(0), secretion=0.0, max_steps=50,
    )
    assert operations == 50
    assert final.size == TARGET_SIZE - 8 + 50


def test_longer_decay_length_increases_target_discrimination_margin():
    margins = [discrimination_margin(lam) for lam in (4.0, 6.0, 8.0, 12.0, 18.0)]
    assert margins == sorted(margins)
