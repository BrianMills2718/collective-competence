from model import State, damage, inhibitor, repair, train_memory


def test_memory_is_learned_from_healthy_signals_not_target_counts():
    for a, b in ((6, 18), (8, 16), (10, 14)):
        memory = train_memory(State(a, b))
        assert abs(memory.a_signal - inhibitor(a)) / inhibitor(a) < 1e-8
        assert abs(memory.b_signal - inhibitor(b)) / inhibitor(b) < 1e-8


def test_persistent_learned_memory_repairs_multiple_compositions():
    for a, b in ((6, 18), (8, 16), (10, 14)):
        healthy = State(a, b)
        memory = train_memory(healthy)
        challenges = (
            (2, 4),
            (a, 0),
            (0, b),
            (max(1, a // 2), max(1, b // 2)),
        )
        for remove_a, remove_b in challenges:
            final, _, _ = repair(
                damage(healthy, remove_a, remove_b),
                memory,
                plastic=True,
                retention=1.0,
            )
            assert (final.a, final.b) == (a, b)


def test_lineage_extinction_still_needs_plasticity():
    healthy = State(8, 16)
    memory = train_memory(healthy)
    assert repair(damage(healthy, 8, 0), memory, plastic=False)[0].a == 0
    assert repair(damage(healthy, 8, 0), memory, plastic=True)[0].a == 8


def test_memory_decay_creates_a_retention_horizon():
    exact = {}
    for retention in (1.0, 0.9995, 0.999, 0.998, 0.995):
        successes = 0
        for a, b in ((6, 18), (8, 16), (10, 14)):
            healthy = State(a, b)
            memory = train_memory(healthy)
            challenges = (
                (2, 4),
                (a, 0),
                (0, b),
                (max(1, a // 2), max(1, b // 2)),
            )
            for remove_a, remove_b in challenges:
                final, _, _ = repair(
                    damage(healthy, remove_a, remove_b),
                    memory,
                    plastic=True,
                    retention=retention,
                )
                successes += (final.a, final.b) == (a, b)
        exact[retention] = successes

    assert exact == {1.0: 12, 0.9995: 12, 0.999: 11, 0.998: 8, 0.995: 4}


def test_reporter_loss_without_wound_does_not_trigger_growth():
    healthy = State(8, 16)
    memory = train_memory(healthy)
    final, _, operations = repair(
        healthy,
        memory,
        secretion_a=0.0,
        max_steps=40,
    )
    assert (final.a, final.b) == (8, 16)
    assert operations == 0


def test_reporter_loss_coincident_with_wound_remains_ambiguous():
    healthy = State(8, 16)
    memory = train_memory(healthy)
    final, _, operations = repair(
        damage(healthy, 4, 0),
        memory,
        secretion_a=0.0,
        max_steps=40,
    )
    assert (final.a, final.b) == (44, 16)
    assert operations == 40
