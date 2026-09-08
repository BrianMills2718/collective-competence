from model import Config, allocation, run


def final_backlog(policy, demand, fail):
    rows = run(policy, Config(demand=demand), fail=fail)
    return rows[-1]["backlog"], rows


def test_intact_policies_match_at_compensable_demand():
    for policy in ("reroute", "fixed"):
        backlog, _ = final_backlog(policy, 2, "none")
        assert backlog == 0


def test_rerouting_compensates_for_either_single_route_cut():
    for fail in ("a", "b"):
        backlog, rows = final_backlog("reroute", 2, fail)
        assert backlog == 0
        post = rows[20:]
        survivor = "flow_b" if fail == "a" else "flow_a"
        failed = "flow_a" if fail == "a" else "flow_b"
        assert all(r[failed] == 0 for r in post)
        assert all(r[survivor] == 2 for r in post)


def test_fixed_assignment_does_not_compensate():
    for fail in ("a", "b"):
        backlog, rows = final_backlog("fixed", 2, fail)
        assert backlog == 40
        assert all(r["flow_a"] + r["flow_b"] == 1 for r in rows[20:])


def test_both_routes_are_causally_needed():
    backlog, rows = final_backlog("reroute", 2, "both")
    assert backlog == 80
    assert all(r["flow_a"] + r["flow_b"] == 0 for r in rows[20:])


def test_compensation_has_a_capacity_boundary():
    for fail in ("a", "b"):
        backlog, rows = final_backlog("reroute", 4, fail)
        assert backlog == 80
        assert all(r["flow_a"] + r["flow_b"] == 2 for r in rows[20:])


def test_fixed_and_rerouting_have_identical_hardware_capacity():
    assert allocation("reroute", 2, 2, a_up=True, b_up=True) == (1, 1)
    assert allocation("fixed", 2, 2, a_up=True, b_up=True) == (1, 1)
