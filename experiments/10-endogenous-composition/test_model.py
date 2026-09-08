from model import TARGET, damage, inhibitor, repair


def test_partial_damage_repairs_from_endogenous_type_signals():
    for left, right in ((4, 0), (0, 8), (2, 6), (4, 4), (4, 8), (7, 8)):
        final, _ = repair(damage(left, right))
        assert final.cells == TARGET


def test_lineage_extinction_still_requires_plasticity():
    for left, right in ((8, 0), (0, 16), (8, 4), (4, 16)):
        assert repair(damage(left, right))[0].cells != TARGET
        assert repair(damage(left, right), plastic=True)[0].cells == TARGET


def test_high_clamp_hides_a_real_deficit():
    final, operations = repair(damage(4, 0), clamp_a=inhibitor(8))
    assert final.counts == (4, 16)
    assert operations == 0


def test_secretion_loss_removes_stop_and_causes_overgrowth():
    final, operations = repair(damage(4, 0), secretion_a=0.0, max_steps=40)
    assert final.counts == (44, 16)
    assert operations == 40


def test_extinct_lineage_can_be_recreated_but_source_failure_breaks_stop():
    final, _ = repair(damage(8, 0), plastic=True)
    assert final.cells == TARGET

    bad, operations = repair(
        damage(8, 0),
        plastic=True,
        secretion_a=0.0,
        max_steps=40,
    )
    assert bad.counts == (40, 16)
    assert operations == 40


def test_no_cells_still_means_no_parent_dependent_regrowth():
    final, operations = repair(damage(8, 16), plastic=True)
    assert final.cells == ()
    assert operations == 0
