"""Passive relaxation and negative-feedback regulation on the shared lattice.

This is the smallest D4 contrast: both arms can occupy the same desirable state,
but for different reasons. The passive arm relaxes toward an environmental
ambient; the feedback arm adds an authored setpoint controller. A displacement
or persistent load exposes the difference.

The one-site lattice is deliberate. It uses the substrate's non-conserving
local-state mode: the site payload is temperature, not an entity identity, and
there are no entity records. This specimen calibrates passive convergence versus
regulation; it does not make a collective-competence claim.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from ..core import Lattice, Window, build, step_synchronous

Arm = Literal["passive", "feedback"]


@dataclass(frozen=True)
class Config:
    """Integer-valued analogue of the earlier scalar thermostat calibration."""

    ambient: int = 100
    setpoint: int = 100
    relaxation_divisor: int = 4
    controller_divisor: int = 2


def make(initial_temperature: int = 100) -> Lattice:
    """One scalar local-state site on the shared Lattice.

    `radius=0`, `centred=True`, `conserving=False` means one synchronous rule
    evaluation rewrites the single site's state. `build` creates no entity
    records in this mode. Nothing in the substrate knows the setpoint; it lives
    only in the feedback rule closure.
    """
    return build(
        [initial_temperature], radius=0, ring=True,
        conserving=False, centred=True,
    )


def _relaxation(temp: int, ambient: int, divisor: int) -> int:
    if divisor <= 0:
        raise ValueError("relaxation_divisor must be positive")
    return int((ambient - temp) / divisor)


def _control(sensed: int, setpoint: int, divisor: int) -> int:
    if divisor <= 0:
        raise ValueError("controller_divisor must be positive")
    return int((setpoint - sensed) / divisor)


def rule(
    arm: Arm,
    config: Config = Config(),
    *,
    load: int = 0,
    sensor_blocked: bool = False,
    actuator_disabled: bool = False,
):
    """Return one transition rule for a matched passive/feedback arm.

    A blocked sensor is pinned to the setpoint, so the feedback term is zero.
    A disabled actuator likewise suppresses control. In either case the feedback
    arm should become behaviorally identical to its passive pair.
    """
    if arm not in ("passive", "feedback"):
        raise ValueError(f"unknown arm: {arm}")

    def update(before: Window, initiator: int) -> Window:
        (raw_temp,) = before
        if raw_temp is None:
            raise ValueError("regulation specimen requires an occupied site")
        temp = int(raw_temp)
        passive = _relaxation(temp, config.ambient, config.relaxation_divisor)
        sensed = config.setpoint if sensor_blocked else temp
        control = 0
        if arm == "feedback" and not actuator_disabled:
            control = _control(sensed, config.setpoint, config.controller_divisor)
        return (temp + passive + control + load,)

    return update


def step(lat: Lattice, transition) -> bool:
    return step_synchronous(lat, transition)


def evolve(lat: Lattice, transition, steps: int) -> list[int]:
    """Return the scalar trajectory, including the initial value."""
    out = [temperature(lat)]
    for _ in range(steps):
        step(lat, transition)
        out.append(temperature(lat))
    return out


def temperature(lat: Lattice) -> int:
    value = lat.occupants[0]
    if value is None:
        raise ValueError("regulation specimen has no temperature state")
    return int(value)


def displace(lat: Lattice, amount: int) -> None:
    """Apply a state perturbation without charging a rule evaluation."""
    lat.occupants[0] = temperature(lat) + amount


def absolute_error(lat: Lattice, setpoint: int = 100) -> int:
    return abs(temperature(lat) - setpoint)


def recovery_time(
    lat: Lattice,
    transition,
    *,
    setpoint: int = 100,
    tolerance: int = 3,
    max_steps: int = 200,
) -> int | None:
    """First step whose state lies inside the declared tolerance band."""
    if absolute_error(lat, setpoint) <= tolerance:
        return 0
    for tick in range(1, max_steps + 1):
        step(lat, transition)
        if absolute_error(lat, setpoint) <= tolerance:
            return tick
    return None
