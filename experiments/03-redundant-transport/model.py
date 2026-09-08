"""Minimal two-route transport system for compensation/repair experiments.

A source receives a fixed number of jobs each tick. Two physically distinct
routes can deliver jobs to a sink. A route has finite capacity and can be cut.
The adaptive policy reassigns jobs to routes that remain available; the fixed
policy keeps the original split even when one route is unavailable.

The external macro criterion is zero backlog. The model contains no goal label,
reward, or authored target beyond the transport policy's instruction to dispatch
newly arriving jobs.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Policy = Literal["reroute", "fixed"]


@dataclass(frozen=True)
class Config:
    demand: int = 2
    route_capacity: int = 2
    fault_tick: int = 20
    horizon: int = 60


@dataclass
class State:
    tick: int = 0
    backlog: int = 0
    delivered: int = 0
    flow_a: int = 0
    flow_b: int = 0


def _split_evenly(amount: int) -> tuple[int, int]:
    """Deterministic symmetric split for the even demands used here."""
    if amount % 2:
        raise ValueError("this calibration uses even demand for route symmetry")
    return amount // 2, amount // 2


def allocation(policy: Policy, demand: int, capacity: int, *, a_up: bool, b_up: bool) -> tuple[int, int]:
    """Allocate this tick's new jobs; backlog is outcome, not extra hidden demand."""
    if demand < 0 or capacity < 0:
        raise ValueError("demand and capacity must be non-negative")
    if policy == "fixed":
        a, b = _split_evenly(demand)
        return (min(a, capacity) if a_up else 0,
                min(b, capacity) if b_up else 0)
    if policy != "reroute":
        raise ValueError(f"unknown policy: {policy}")

    active = [name for name, up in (("a", a_up), ("b", b_up)) if up]
    remaining = demand
    sent = {"a": 0, "b": 0}
    # Split when both routes exist; if one is cut, the survivor receives the
    # whole dispatch up to its physical capacity.
    if len(active) == 2:
        a, b = _split_evenly(demand)
        sent["a"], sent["b"] = min(a, capacity), min(b, capacity)
    elif len(active) == 1:
        sent[active[0]] = min(remaining, capacity)
    return sent["a"], sent["b"]


def step(state: State, policy: Policy, cfg: Config, *, a_up: bool = True, b_up: bool = True) -> State:
    a, b = allocation(policy, cfg.demand, cfg.route_capacity, a_up=a_up, b_up=b_up)
    delivered_now = a + b
    state.backlog += cfg.demand - delivered_now
    state.delivered += delivered_now
    state.flow_a = a
    state.flow_b = b
    state.tick += 1
    return state


def run(policy: Policy, cfg: Config = Config(), *, fail: Literal["none", "a", "b", "both"] = "none") -> list[dict]:
    state = State()
    rows = []
    for _ in range(cfg.horizon):
        fault_active = state.tick >= cfg.fault_tick
        a_up = not (fault_active and fail in {"a", "both"})
        b_up = not (fault_active and fail in {"b", "both"})
        step(state, policy, cfg, a_up=a_up, b_up=b_up)
        rows.append({
            "tick": state.tick,
            "backlog": state.backlog,
            "delivered": state.delivered,
            "flow_a": state.flow_a,
            "flow_b": state.flow_b,
            "a_up": a_up,
            "b_up": b_up,
        })
    return rows
