"""Characterize passive relaxation versus negative-feedback regulation."""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO / "goal-discovery"))

from src.lattice.core import restore, snapshot  # noqa: E402
from src.lattice.specimens import regulation  # noqa: E402


CFG = regulation.Config()
DISPLACEMENTS = (-40, -20, 20, 40)
LOADS = (-4, -2, 2, 4)


def late_error(arm: regulation.Arm, load: int, *, blocked=False, disabled=False) -> float:
    base = regulation.make(CFG.setpoint)
    lat = restore(snapshot(base))
    transition = regulation.rule(
        arm, CFG, load=load,
        sensor_blocked=blocked,
        actuator_disabled=disabled,
    )
    trace = regulation.evolve(lat, transition, 100)
    return sum(abs(x - CFG.setpoint) for x in trace[-20:]) / 20


def characterize() -> dict:
    base = regulation.make(CFG.setpoint)
    snap = snapshot(base)

    displacement = []
    for amount in DISPLACEMENTS:
        row = {"amount": amount}
        for arm in ("passive", "feedback"):
            lat = restore(snap)
            regulation.displace(lat, amount)
            row[arm] = regulation.recovery_time(
                lat, regulation.rule(arm, CFG), setpoint=CFG.setpoint,
            )
        displacement.append(row)

    loads = []
    for load in LOADS:
        loads.append({
            "load": load,
            "passive_late_error": late_error("passive", load),
            "feedback_late_error": late_error("feedback", load),
            "sensor_blocked_late_error": late_error("feedback", load, blocked=True),
            "actuator_disabled_late_error": late_error("feedback", load, disabled=True),
        })

    return {
        "config": CFG.__dict__,
        "criterion": {"setpoint": CFG.setpoint, "tolerance": 3},
        "displacement_recovery": displacement,
        "persistent_load": loads,
    }


def main() -> None:
    result = characterize()
    out = HERE / "results" / "characterization.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
