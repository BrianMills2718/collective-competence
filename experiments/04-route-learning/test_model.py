from model import A_GOOD, B_GOOD, reversal, run, stationary


def test_adaptive_improves_in_both_stationary_environments():
    for env in (A_GOOD, B_GOOD):
        rows = run("adaptive", stationary(env))
        assert rows[-1]["delivered"] == 95.0
        assert rows[-1]["delivered"] > rows[0]["delivered"] == 75.0


def test_frozen_and_reset_are_behaviorally_identical():
    for envs in (stationary(A_GOOD), stationary(B_GOOD), reversal(A_GOOD, B_GOOD)):
        frozen = run("frozen", envs)
        reset = run("reset", envs)
        assert [r["delivered"] for r in frozen] == [r["delivered"] for r in reset]
        assert [r["preference_a_start"] for r in frozen] == [r["preference_a_start"] for r in reset] == [0.5] * len(envs)


def test_all_arms_share_the_first_episode_baseline():
    envs=stationary(A_GOOD)
    first=[run(p, envs)[0]["delivered"] for p in ("adaptive","frozen","reset")]
    assert first == [75.0,75.0,75.0]


def test_reversal_causes_loss_then_relearning():
    rows=run("adaptive", reversal(A_GOOD,B_GOOD))
    assert rows[2]["delivered"] == 95.0
    assert rows[3]["delivered"] == 55.0
    assert rows[-1]["delivered"] == 95.0
    assert rows[3]["preference_a_start"] == 0.9
    assert rows[-1]["preference_a_start"] == 0.1


def test_same_current_environment_has_history_dependent_action():
    switched=run("adaptive", reversal(A_GOOD,B_GOOD))
    trained_b=run("adaptive", stationary(B_GOOD, episodes=8))
    # Episode 4 sees B_GOOD in both histories; only prior experience differs.
    assert switched[3]["quality_a"] == trained_b[3]["quality_a"] == 0.5
    assert switched[3]["quality_b"] == trained_b[3]["quality_b"] == 1.0
    assert switched[3]["allocated_a"] == 90.0
    assert trained_b[3]["allocated_a"] == 10.0


def test_no_policy_can_exceed_the_authored_preference_bounds():
    for envs in (stationary(A_GOOD,20),stationary(B_GOOD,20)):
        for r in run("adaptive",envs):
            assert 0.1 <= r["preference_a_start"] <= 0.9
