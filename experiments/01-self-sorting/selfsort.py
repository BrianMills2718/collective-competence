#!/usr/bin/env python3
"""Experiment 1: Levin-style self-sorting with defective local agents.

An array of N integers is a line of local agents. An agent can only inspect
itself and one adjacent neighbour, and its only action is "attempt to exchange
with that neighbour". The global target is the sorted array. Distance to the
target is the inversion count.

Everything is measured in one common currency: an *attempted local
compare-exchange operation*. Centralized, decentralized and random controllers
all spend the same primitive, so op counts are directly comparable. The only
difference between them is who decides which pair is touched next, and whether
anyone is still watching after the goal is first reached.

Fault model (a local action can fail):
  p_fail        every attempted action fails with this probability
  unreliable[v] agent holding value v fails to initiate with this probability
  frozen[v]     agent v never initiates, but a neighbour can still move it
  dead[v]       agent v never initiates and cannot be moved (blocks the line)

Usage:
  python selfsort.py test
  python selfsort.py faults
  python selfsort.py recovery
  python selfsort.py hetero
  python selfsort.py single-point
  python selfsort.py all
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import statistics
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterator

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"

# ----------------------------------------------------------------------------
# State, goal, distance
# ----------------------------------------------------------------------------


def inversions(a: list[int]) -> int:
    """Distance to the sorted attractor. 0 iff sorted ascending."""
    n = len(a)
    return sum(1 for i in range(n) for j in range(i + 1, n) if a[i] > a[j])


@dataclass
class Faults:
    p_fail: float = 0.0
    unreliable: dict[int, float] = field(default_factory=dict)
    frozen: set[int] = field(default_factory=set)
    dead: set[int] = field(default_factory=set)

    def copy(self) -> "Faults":
        return Faults(self.p_fail, dict(self.unreliable), set(self.frozen), set(self.dead))


# Local rules. Each takes (left_value, right_value) and returns True to exchange.
RULE_ASCEND: Callable[[int, int], bool] = lambda lo, hi: lo > hi
RULE_DESCEND: Callable[[int, int], bool] = lambda lo, hi: lo < hi
RULE_ALWAYS: Callable[[int, int], bool] = lambda lo, hi: True


@dataclass
class World:
    """The substrate: an array plus per-agent rules and defects."""

    a: list[int]
    rules: dict[int, Callable[[int, int], bool]]  # value -> local rule
    faults: Faults
    rng: random.Random
    ops: int = 0
    inv: int = -1  # inversion count, maintained incrementally

    def __post_init__(self) -> None:
        self.inv = inversions(self.a)

    def resync(self) -> None:
        """Recompute from scratch after an external change to the array."""
        self.inv = inversions(self.a)

    def scan(self, i: int) -> bool:
        """A coordinator reads the adjacent pair at i. Costs one op, because
        looking is the same primitive an agent uses. Charging for this is what
        makes a never-halting watchdog pay for its monitoring."""
        self.ops += 1
        return self.a[i] > self.a[i + 1]

    def attempt(self, i: int, initiator: int | None = None, charge: bool = True) -> bool:
        """One attempted local compare-exchange between positions i and i+1.

        Costs one op unless the caller already paid for the same op with scan().
        Returns True if the array actually changed.
        """
        if charge:
            self.ops += 1
        left, right = self.a[i], self.a[i + 1]
        if left in self.faults.dead or right in self.faults.dead:
            return False
        if initiator is None:
            initiator = left if self.rng.random() < 0.5 else right
        if initiator in self.faults.frozen:
            return False
        q = max(self.faults.p_fail, self.faults.unreliable.get(initiator, 0.0))
        if q > 0.0 and self.rng.random() < q:
            return False
        if not self.rules[initiator](left, right):
            return False
        self.a[i], self.a[i + 1] = right, left
        # An adjacent exchange changes the inversion count by exactly one.
        self.inv += -1 if left > right else 1
        return True


# ----------------------------------------------------------------------------
# Controllers: generators that drive the world until they stop
# ----------------------------------------------------------------------------

Controller = Callable[[World, int], Iterator[None]]


def decentralized(w: World, budget: int) -> Iterator[None]:
    """No coordinator. A random adjacent pair acts; the initiator is one of the
    two agents, applying its own rule. Never halts, never declares victory."""
    n = len(w.a)
    while w.ops < budget:
        w.attempt(w.rng.randrange(n - 1))
        yield


def null_random(w: World, budget: int) -> Iterator[None]:
    """Same locality, no rule: exchange with a random neighbour regardless."""
    n = len(w.a)
    while w.ops < budget:
        i = w.rng.randrange(n - 1)
        w.attempt(i, initiator=None)
        yield


def central_open(w: World, budget: int) -> Iterator[None]:
    """A coordinator running the textbook schedule: n passes, then done. It has
    a plan and no feedback, so an action that silently fails is never noticed."""
    n = len(w.a)
    for _ in range(n):
        for i in range(n - 1):
            if w.ops >= budget:
                return
            if w.scan(i):
                w.attempt(i, charge=False)
            yield


def central_closed(w: World, budget: int) -> Iterator[None]:
    """A coordinator that re-scans and only halts when a full pass finds no
    inversion. Robust to action faults; stops watching once it believes it is
    finished."""
    n = len(w.a)
    while w.ops < budget:
        found = False
        for i in range(n - 1):
            if w.ops >= budget:
                return
            if w.scan(i):
                found = True
                w.attempt(i, charge=False)
            yield
        if not found:
            return


def central_watchdog(w: World, budget: int) -> Iterator[None]:
    """Same coordinator, but it never concludes it is done: it keeps scanning
    forever. The fairest centralized comparator for the decentralized rule."""
    n = len(w.a)
    while w.ops < budget:
        for i in range(n - 1):
            if w.ops >= budget:
                return
            if w.scan(i):
                w.attempt(i, charge=False)
            yield


STYLE = {
    "decentralized": dict(color="C0", ls="-", marker="o", lw=2.4),
    "central_open": dict(color="C1", ls="-", marker="s", lw=1.6),
    "central_closed": dict(color="C2", ls="--", marker="^", lw=2.6),
    "central_watchdog": dict(color="C3", ls=":", marker="v", lw=1.6),
    "null_random": dict(color="C4", ls="-.", marker="x", lw=1.4),
}

CONTROLLERS: dict[str, Controller] = {
    "decentralized": decentralized,
    "central_open": central_open,
    "central_closed": central_closed,
    "central_watchdog": central_watchdog,
    "null_random": null_random,
}

# Controllers that depend on a single coordinating locus.
HAS_COORDINATOR = {"central_open", "central_closed", "central_watchdog"}


# ----------------------------------------------------------------------------
# Perturbations
# ----------------------------------------------------------------------------


def perturb_swap2(w: World) -> str:
    n = len(w.a)
    i, j = w.rng.sample(range(n), 2)
    w.a[i], w.a[j] = w.a[j], w.a[i]
    return f"swap positions {i},{j}"


def perturb_teleport(w: World) -> str:
    n = len(w.a)
    i, j = w.rng.sample(range(n), 2)
    v = w.a.pop(i)
    w.a.insert(j, v)
    return f"move value {v} from {i} to {j}"


def perturb_freeze_one(w: World) -> str:
    v = w.rng.choice(w.a)
    w.faults.frozen.add(v)
    return f"freeze agent {v}"


def perturb_unreliable_one(w: World) -> str:
    v = w.rng.choice(w.a)
    w.faults.unreliable[v] = 0.9
    return f"agent {v} now fails 90% of its actions"


def perturb_dead_one(w: World) -> str:
    v = w.rng.choice(w.a)
    w.faults.dead.add(v)
    return f"agent {v} is dead and blocks exchanges"


def _compound(defect: Callable[[World], str]) -> Callable[[World], str]:
    """Damage a member and the state together. A substrate defect applied to an
    already-sorted array changes nothing, so on its own it cannot be recovered
    from and cannot be measured."""

    def run(w: World) -> str:
        return f"{defect(w)} + {perturb_swap2(w)}"

    return run


PERTURBATIONS = {
    # pure state damage
    "swap2": perturb_swap2,
    "teleport": perturb_teleport,
    # member damage + state damage
    "frozen_member": _compound(perturb_freeze_one),
    "unreliable_member": _compound(perturb_unreliable_one),
    "dead_member": _compound(perturb_dead_one),
}

# Perturbations that are meaningfully divisible into equal units. `swap2` and
# `teleport` damage state only, so k of them is k times the same kind of damage
# and "eight faults" means the same thing however they are delivered. The
# member-damage perturbations are NOT on this list: freezing eight agents at
# once and freezing one agent eight times over are different experiments, and
# the second is not even well defined once the same agent can be chosen twice.
# A delivery comparison that mixed them in would be varying two things.
DIVISIBLE_PERTURBATIONS = ("swap2", "teleport")


def _deliver(perturbation: str, w: World, magnitude: int) -> str:
    """Apply one perturbation `magnitude` times as a single delivery.

    magnitude=1 calls the perturbation function exactly once and draws exactly
    the same random numbers as the pre-2026-09-06 code did, which is what lets
    `check_single_shot_baseline` still reproduce the recorded trials.
    """
    if magnitude < 1:
        raise ValueError("perturb_magnitude must be at least 1")
    fn = PERTURBATIONS[perturbation]
    descs = [fn(w) for _ in range(magnitude)]
    return descs[0] if magnitude == 1 else f"{magnitude}x [" + "; ".join(descs) + "]"


# ----------------------------------------------------------------------------
# Trial runner
# ----------------------------------------------------------------------------


@dataclass
class Episode:
    """One delivered perturbation and what happened after it.

    `recovered` is inversions returning to zero before the op budget ran out.
    `ops_to_recover` is measured from the moment of the disturbance, so it is
    comparable across episodes regardless of when in the run they happened --
    which is the whole point of repeating: a passive attractor should pay the
    same cost every time.
    """

    index: int
    ops_at_perturb: int
    inv_after_perturb: int
    recovered: bool = False
    ops_to_recover: int | None = None


@dataclass
class Trial:
    controller: str
    n: int
    seed: int
    p_fail: float
    ops_used: int
    stopped_early: bool  # controller halted on its own before the op budget
    inv_final: int
    inv_at_stop: int
    ever_sorted: bool
    ops_to_sorted: int | None
    sorted_at_stop: bool
    # perturbation bookkeeping.
    # These five describe the FIRST perturbation only, and are kept because
    # every result recorded before 2026-09-06 is expressed in them. With
    # perturb_repeats=1 they are the whole story; with more, read `episodes`.
    perturbation: str | None = None
    ops_at_perturb: int | None = None
    inv_after_perturb: int | None = None
    recovered: bool = False
    ops_to_recover: int | None = None
    perturbed_after_stop: bool = False
    # One entry per perturbation actually delivered. episodes[0] mirrors the
    # five fields above. Empty when nothing fired.
    episodes: list["Episode"] = field(default_factory=list)
    episodes_requested: int = 1
    # Faults applied per delivery. Total damage in a run is
    # perturb_magnitude * (episodes actually delivered).
    perturb_magnitude: int = 1
    # Why the episode sequence ended: "completed" (all requested delivered),
    # "budget" (ops ran out), "never_sorted" (goal never reached, so nothing to
    # disturb), "no_recovery" (an episode was never recovered from, so the next
    # one could not be armed). A run that stops at one episode because the
    # system never came back is the measurement, not a failure of the harness.
    episode_stop_reason: str = "never_sorted"
    goal_occupancy: float = math.nan  # fraction of the back half of the run spent sorted
    trajectory: list[tuple[int, int]] = field(default_factory=list)


def run_trial(
    controller: str,
    n: int = 10,
    seed: int = 0,
    faults: Faults | None = None,
    budget: int = 20_000,
    rule_b_fraction: float = 0.0,
    n_type_b: int | None = None,
    perturbation: str | None = None,
    perturb_on_sorted: bool = True,
    perturb_at_op: int | None = None,
    perturb_delay: int = 0,
    perturb_repeats: int = 1,
    perturb_magnitude: int = 1,
    stop_on_goal: bool = False,
    sample_every: int = 5,
    record_trajectory: bool = False,
) -> Trial:
    rng = random.Random(seed)
    a = list(range(n))
    rng.shuffle(a)

    n_b = n_type_b if n_type_b is not None else int(round(rule_b_fraction * n))
    type_b = set(rng.sample(range(n), n_b)) if n_b else set()
    rules = {v: (RULE_DESCEND if v in type_b else RULE_ASCEND) for v in range(n)}
    if controller == "null_random":
        rules = {v: RULE_ALWAYS for v in range(n)}

    w = World(a=a, rules=rules, faults=(faults.copy() if faults else Faults()), rng=rng)

    t = Trial(
        controller=controller,
        n=n,
        seed=seed,
        p_fail=w.faults.p_fail,
        ops_used=0,
        stopped_early=False,
        inv_final=0,
        inv_at_stop=0,
        ever_sorted=False,
        ops_to_sorted=None,
        sorted_at_stop=False,
        perturbation=perturbation,
    )

    if perturb_repeats < 1:
        raise ValueError("perturb_repeats must be at least 1")
    if perturb_magnitude < 1:
        raise ValueError("perturb_magnitude must be at least 1")
    t.episodes_requested = perturb_repeats
    t.perturb_magnitude = perturb_magnitude

    # `armed` means a perturbation is pending and will fire at the next trigger.
    # `delivered` counts episodes already fired. The pre-2026-09-06 behaviour is
    # exactly perturb_repeats=1: arm once, fire once, never re-arm.
    armed = perturbation is not None
    delivered = 0
    fired = perturbation is None      # kept: read as "nothing left to deliver"
    arm_from_op: int | None = None    # first sort, then each recovery
    goal_op: int | None = None
    occ_hits = 0
    occ_samples = 0
    inv = w.inv
    if record_trajectory:
        t.trajectory.append((0, inv))

    gen = CONTROLLERS[controller](w, budget)
    last_sample = 0
    for _ in gen:
        inv = w.inv

        if not t.ever_sorted and inv == 0:
            t.ever_sorted = True
            t.ops_to_sorted = w.ops
            goal_op = w.ops
            arm_from_op = w.ops

        if w.ops * 2 >= budget:
            occ_samples += 1
            occ_hits += 1 if inv == 0 else 0

        if record_trajectory and w.ops - last_sample >= sample_every:
            t.trajectory.append((w.ops, inv))
            last_sample = w.ops

        if armed:
            trigger = (
                (arm_from_op is not None and w.ops >= arm_from_op + perturb_delay)
                if perturb_on_sorted
                else (w.ops >= (perturb_at_op or 0))
            )
            if trigger:
                desc = _deliver(perturbation, w, perturb_magnitude)
                w.resync()
                armed = False
                episode = Episode(
                    index=delivered,
                    ops_at_perturb=w.ops,
                    inv_after_perturb=w.inv,
                )
                t.episodes.append(episode)
                delivered += 1
                if delivered >= perturb_repeats:
                    # Nothing further will be armed; the run is now in its
                    # final recovery window.
                    fired = True
                if episode.index == 0:
                    t.perturbation = f"{perturbation}: {desc}"
                    t.ops_at_perturb = episode.ops_at_perturb
                    t.inv_after_perturb = episode.inv_after_perturb
                if record_trajectory:
                    t.trajectory.append((w.ops, episode.inv_after_perturb))
        elif t.episodes and not t.episodes[-1].recovered and inv == 0:
            episode = t.episodes[-1]
            episode.recovered = True
            episode.ops_to_recover = w.ops - episode.ops_at_perturb
            if episode.index == 0:
                t.recovered = True
                t.ops_to_recover = episode.ops_to_recover
            if delivered < perturb_repeats:
                # Re-arm from this recovery, so perturb_delay means the same
                # thing for every episode: ops of undisturbed goal-holding
                # before the next disturbance.
                armed = True
                arm_from_op = w.ops

        # Instrumentation-side stop: an observer halts the clock once the goal
        # is reached and every requested perturbation has been delivered and
        # settled. This is not the controller halting -- `stopped_early` still
        # records that separately.
        if stop_on_goal and inv == 0 and fired and not armed and (
            not t.episodes or t.episodes[-1].recovered
        ):
            t.episode_stop_reason = "completed"
            break
    else:
        t.stopped_early = w.ops < budget
        if armed and perturbation is not None and t.ever_sorted:
            # The controller halted or the budget ran out while a perturbation
            # was still pending. Deliver it anyway, so a controller cannot dodge
            # the disturbance by stopping first.
            desc = _deliver(perturbation, w, perturb_magnitude)
            w.resync()
            armed = False
            episode = Episode(
                index=delivered,
                ops_at_perturb=w.ops,
                inv_after_perturb=w.inv,
            )
            t.episodes.append(episode)
            delivered += 1
            if delivered >= perturb_repeats:
                fired = True
            if episode.index == 0:
                t.perturbation = f"{perturbation}: {desc} (after controller stopped)"
                t.ops_at_perturb = episode.ops_at_perturb
                t.inv_after_perturb = episode.inv_after_perturb
                t.perturbed_after_stop = True
            else:
                t.perturbation = f"{t.perturbation} (+ episode {episode.index} after controller stopped)"

    # Why the sequence ended, recorded rather than inferred. "no_recovery" and
    # "budget" are both real measurements about the specimen: a controller that
    # never comes back cannot be perturbed a second time, and that IS its
    # robustness profile, not a gap in it.
    if t.episode_stop_reason != "completed":
        if not t.episodes:
            t.episode_stop_reason = "never_sorted" if not t.ever_sorted else "never_armed"
        elif delivered >= perturb_repeats:
            t.episode_stop_reason = (
                "completed" if t.episodes[-1].recovered else "no_recovery"
            )
        elif not t.episodes[-1].recovered:
            t.episode_stop_reason = "no_recovery"
        else:
            t.episode_stop_reason = "budget"

    inv = w.inv
    if record_trajectory:
        t.trajectory.append((w.ops, inv))
    t.ops_used = w.ops
    t.goal_occupancy = (occ_hits / occ_samples) if occ_samples else math.nan
    t.inv_final = inv
    t.inv_at_stop = inv
    t.sorted_at_stop = inv == 0
    if not t.ever_sorted and inv == 0:
        t.ever_sorted = True
        t.ops_to_sorted = w.ops
    return t


# ----------------------------------------------------------------------------
# Reporting helpers
# ----------------------------------------------------------------------------


def _mean(xs: list[float]) -> float:
    return statistics.fmean(xs) if xs else math.nan


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        wr.writeheader()
        wr.writerows(rows)
    print(f"  wrote {path}")


def _plt():
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    return plt


# ----------------------------------------------------------------------------
# Experiment 1: fault sweep
# ----------------------------------------------------------------------------

P_GRID = [0.0, 0.05, 0.10, 0.20, 0.30, 0.50, 0.70]


def exp_faults(n: int = 10, trials: int = 200, budget: int = 20_000) -> list[dict]:
    print("\n=== fault sweep: does local action failure destroy goal achievement? ===")
    rows = []
    for name in CONTROLLERS:
        for p in P_GRID:
            ts = [
                run_trial(name, n=n, seed=1000 * k + 7, faults=Faults(p_fail=p), budget=budget,
                          stop_on_goal=True)
                for k in range(trials)
            ]
            ok = [t for t in ts if t.sorted_at_stop]
            rows.append(
                dict(
                    controller=name,
                    p_fail=p,
                    success_rate=len(ok) / len(ts),
                    median_ops_success=(
                        statistics.median([t.ops_to_sorted for t in ok]) if ok else math.nan
                    ),
                    mean_inv_at_stop=_mean([t.inv_at_stop for t in ts]),
                    frac_halted_early=_mean([1.0 if t.stopped_early else 0.0 for t in ts]),
                )
            )
        print(
            f"  {name:<18} success@p=0 {rows[-len(P_GRID)]['success_rate']:.2f}"
            f"   success@p=0.3 {rows[-len(P_GRID) + 4]['success_rate']:.2f}"
            f"   success@p=0.7 {rows[-1]['success_rate']:.2f}"
        )
    write_csv(RESULTS / "faults.csv", rows)

    plt = _plt()
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    for name in CONTROLLERS:
        sub = [r for r in rows if r["controller"] == name]
        axes[0].plot([r["p_fail"] for r in sub], [r["success_rate"] for r in sub],
                     label=name, **STYLE[name])
        axes[1].plot([r["p_fail"] for r in sub], [r["median_ops_success"] for r in sub],
                     label=name, **STYLE[name])
    axes[0].set(xlabel="local action failure probability p", ylabel="P(sorted when controller stops)",
                title=f"Goal achievement under local faults (N={n}, {trials} trials)")
    axes[0].set_ylim(-0.05, 1.05)
    axes[1].set(xlabel="local action failure probability p", ylabel="median ops to sorted",
                title="Cost of reaching the goal")
    axes[1].set_yscale("log")
    for ax in axes:
        ax.grid(alpha=0.3)
    axes[0].legend(fontsize=8)
    fig.tight_layout()
    out = RESULTS / "01_faults.png"
    fig.savefig(out, dpi=140)
    print(f"  wrote {out}")
    return rows


# ----------------------------------------------------------------------------
# Experiment 2: perturbation and recovery
# ----------------------------------------------------------------------------


def exp_recovery(n: int = 10, trials: int = 200, budget: int = 20_000) -> list[dict]:
    print("\n=== perturbation: does the collective return to the attractor? ===")
    rows = []
    controllers = ["decentralized", "central_closed", "central_watchdog"]
    for pert in PERTURBATIONS:
        for name in controllers:
            for p in (0.0, 0.10, 0.30):
                ts = [
                    run_trial(
                        name, n=n, seed=1000 * k + 13, faults=Faults(p_fail=p), budget=budget,
                        perturbation=pert, perturb_on_sorted=True, stop_on_goal=True,
                    )
                    for k in range(trials)
                ]
                hit = [t for t in ts if t.ops_at_perturb is not None]
                rec = [t for t in hit if t.recovered]
                rows.append(
                    dict(
                        perturbation=pert,
                        controller=name,
                        p_fail=p,
                        reached_goal_first=len(hit) / len(ts),
                        recovery_rate=(len(rec) / len(hit)) if hit else math.nan,
                        median_ops_to_recover=(
                            statistics.median([t.ops_to_recover for t in rec]) if rec else math.nan
                        ),
                        mean_damage_inv=_mean([t.inv_after_perturb for t in hit]),
                    )
                )
        for name in controllers:
            r = next(r for r in rows if r["perturbation"] == pert and r["controller"] == name and r["p_fail"] == 0.0)
            print(f"  {pert:<16} {name:<18} recovery {r['recovery_rate']:.2f}"
                  f"  median ops {r['median_ops_to_recover']}")
    write_csv(RESULTS / "recovery.csv", rows)

    # Trajectory figure: one representative run per controller under swap2.
    plt = _plt()
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.2), sharey=True, sharex=True)
    for ax, name in zip(axes, controllers):
        for p, colour in zip((0.0, 0.10, 0.30), ("C0", "C1", "C3")):
            for k in range(6):
                t = run_trial(
                    name, n=n, seed=500 + k, faults=Faults(p_fail=p), budget=4000,
                    perturbation="swap2", perturb_on_sorted=True, stop_on_goal=True,
                    record_trajectory=True, sample_every=1,
                )
                xs = [x for x, _ in t.trajectory]
                ys = [y for _, y in t.trajectory]
                ax.plot(xs, ys, colour, alpha=0.55, lw=1.0,
                        label=f"p={p}" if k == 0 else None)
                if t.ops_at_perturb is not None:
                    ax.axvline(t.ops_at_perturb, color=colour, ls=":", alpha=0.35)
        ax.set(title=name, xlabel="attempted local operations")
        ax.grid(alpha=0.3)
    axes[0].set_ylabel("inversions (distance to goal)")
    axes[0].legend(fontsize=8)
    fig.suptitle("Recovery after a perturbation applied the moment the goal is first reached")
    fig.tight_layout()
    out = RESULTS / "02_recovery.png"
    fig.savefig(out, dpi=140)
    print(f"  wrote {out}")
    return rows


REPEAT_EPISODES = 8


def exp_repeat(n: int = 10, trials: int = 200, budget: int = 20_000) -> list[dict]:
    """Disturb repeatedly, and read the profile across episodes rather than one number.

    D2. The ontology defines robustness as performance *across* perturbations and
    adaptation as change that restores performance *after loss*. A schedule that
    fires once can express neither: it yields one recovery, so "recovery rate"
    is a rate over trials, never over repeated demands on the same system.

    Two quantities only a repeated schedule can produce.

    **How many disturbances the system absorbs.** Delivered at D=20 operations
    after the goal is reached, with `stop_on_goal=False`, a controller that halts
    on "no inversion found" is not present for the second disturbance -- it is
    not present for the first either, which is why it is perturbed after
    stopping. Its episode count is therefore pinned at one *by its own design*,
    and that ceiling is a robustness measurement, not a gap in the data.

    **Whether the cost of recovery is stationary.** A passive attractor pays the
    same price every time, because its basin does not change. A rising cost
    across episodes means something is accumulating; a falling cost would be the
    adaptation row, and is not expected here.

    The compound perturbations (frozen/unreliable/dead member) damage a member
    permanently, so their episode sequences terminate early by construction. That
    is reported as `episode_stop_reason`, not silently dropped.

    **Read `trials_reaching_episode` before reading `median_ops_to_recover`.**
    Episode i is only faced by trials that recovered from episode i-1, so where
    attrition is heavy the later cost figures are conditioned on continued
    success and will trend *down* for that reason alone. Measured here at
    p_fail=0.30: `swap2`, `teleport` and `unreliable_member` keep all 200 trials
    through episode 7, so their cost columns are unbiased; `frozen_member` falls
    to 13 trials with recovery rate decaying 1.00 -> 0.42, so its apparent late
    cost *improvement* is survivorship and must not be read as adaptation. The
    per-episode recovery rate is always computed over the at-risk population and
    is unbiased in both cases.
    """
    print("\n=== repeated disturbance: how many, and does the cost hold? ===")
    rows: list[dict] = []
    summary: list[dict] = []
    controllers = ["decentralized", "central_closed", "central_watchdog"]
    for pert in PERTURBATIONS:
        for name in controllers:
            for p in (0.0, 0.10, 0.30):
                ts = [
                    run_trial(
                        name, n=n, seed=1000 * k + 29, faults=Faults(p_fail=p),
                        budget=budget, perturbation=pert, perturb_on_sorted=True,
                        perturb_delay=20, perturb_repeats=REPEAT_EPISODES,
                        stop_on_goal=False,
                    )
                    for k in range(trials)
                ]
                reached = [t for t in ts if t.ever_sorted]
                # Per-episode profile. `at_risk` is the number of trials that got
                # this far, so a recovery rate is always over the population that
                # actually faced that episode -- never over the whole trial count,
                # which would silently read "never got here" as "did not recover".
                for i in range(REPEAT_EPISODES):
                    at_risk = [t for t in ts if len(t.episodes) > i]
                    if not at_risk:
                        continue
                    rec = [t.episodes[i] for t in at_risk if t.episodes[i].recovered]
                    rows.append(dict(
                        perturbation=pert, controller=name, p_fail=p,
                        episode=i,
                        trials_reaching_episode=len(at_risk),
                        recovery_rate=len(rec) / len(at_risk),
                        median_ops_to_recover=(
                            statistics.median([e.ops_to_recover for e in rec])
                            if rec else math.nan),
                        mean_damage_inv=_mean(
                            [t.episodes[i].inv_after_perturb for t in at_risk]),
                    ))
                summary.append(dict(
                    perturbation=pert, controller=name, p_fail=p,
                    trials=len(ts),
                    trials_reaching_goal=len(reached),
                    mean_episodes_absorbed=_mean([float(len(t.episodes)) for t in ts]),
                    max_episodes_absorbed=max((len(t.episodes) for t in ts), default=0),
                    stop_completed=_mean(
                        [1.0 if t.episode_stop_reason == "completed" else 0.0 for t in ts]),
                    stop_no_recovery=_mean(
                        [1.0 if t.episode_stop_reason == "no_recovery" else 0.0 for t in ts]),
                    stop_never_sorted=_mean(
                        [1.0 if t.episode_stop_reason == "never_sorted" else 0.0 for t in ts]),
                ))
        for name in controllers:
            s = next(r for r in summary if r["perturbation"] == pert
                     and r["controller"] == name and r["p_fail"] == 0.0)
            print(f"  {pert:<16} {name:<18} episodes absorbed "
                  f"mean {s['mean_episodes_absorbed']:.2f} max {s['max_episodes_absorbed']}")
    write_csv(RESULTS / "repeat.csv", rows)
    write_csv(RESULTS / "repeat_summary.csv", summary)

    # Cost against episode index, with the at-risk population drawn underneath,
    # because the second is what licenses reading the first.
    plt = _plt()
    live = ["swap2", "unreliable_member", "frozen_member"]
    fig, axes = plt.subplots(2, len(live), figsize=(13, 6.4), sharex=True,
                             gridspec_kw={"height_ratios": [2, 1]})
    for col, pert in enumerate(live):
        top, bot = axes[0][col], axes[1][col]
        for cname in controllers:
            sub = sorted(
                (r for r in rows if r["perturbation"] == pert
                 and r["controller"] == cname and r["p_fail"] == 0.30
                 and r["episode"] >= 0),
                key=lambda r: r["episode"])
            xs = [r["episode"] for r in sub]
            top.plot(xs, [r["median_ops_to_recover"] for r in sub],
                     label=cname, **STYLE[cname])
            bot.plot(xs, [r["trials_reaching_episode"] for r in sub], **STYLE[cname])
        top.set(title=pert)
        top.grid(alpha=0.3)
        bot.set(xlabel="episode", ylim=(0, trials * 1.05))
        bot.grid(alpha=0.3)
    axes[0][0].set_ylabel("median ops to recover")
    axes[1][0].set_ylabel("trials still at risk")
    axes[0][0].legend(fontsize=8)
    # central_closed draws no line anywhere, and the absence is the result:
    # it halts before the disturbance in 200/200 trials, so it is perturbed
    # after stopping, never recovers, and has no episode 1 to plot.
    axes[0][0].text(0.03, 0.06,
                    "central_closed: no line -- halts before the disturbance in\n"
                    "200/200 trials, so it never recovers and never reaches episode 1",
                    transform=axes[0][0].transAxes, fontsize=7.5, color="0.25")
    fig.suptitle("Repeated disturbance at D=20, p_fail=0.30: cost per episode, "
                 "over the population that actually faced it")
    fig.tight_layout()
    out = RESULTS / "07_repeat.png"
    fig.savefig(out, dpi=140)
    print(f"  wrote {out}")
    return rows


DELAY_GRID = [0, 5, 20, 60, 200]


DELIVERY_TOTAL_DAMAGE = 8


def exp_delivery(n: int = 10, trials: int = 200, budget: int = 20_000) -> list[dict]:
    """Hold total damage fixed; vary only how it is delivered.

    D2's second half. `exp_repeat` established that the cost of recovery is
    stationary across eight episodes with no attrition, which is a passive
    attractor's signature -- but it only ever delivered one fault at a time, so
    it could not separate "delivery does not matter" from "this much damage does
    not matter". This experiment fixes total damage at
    DELIVERY_TOTAL_DAMAGE=8 faults and changes nothing but their arrival:

      * **burst** -- one episode carrying all 8 faults at once.
      * **drip**  -- 8 episodes carrying 1 fault each.

    What each answer would mean.

    **If total recovery cost is about the same either way**, the system is
    paying for displacement and not for disturbance events. That is the passive
    attractor reading, and it is the second, independent piece of evidence for
    it: a basin does not care whether you push it once or eight times, only how
    far.

    **If drip costs materially more**, there is a fixed per-episode price -- a
    re-approach, a re-detection -- that a goal-directed controller would be
    paying and a pure attractor would not.

    **If burst costs disproportionately more than 8x a single fault**, the
    damage is not linear in the number of faults: eight swaps can interact,
    creating a configuration no single swap reaches. That would be a fact about
    the substrate, not about the controllers, and it is why the single-fault
    reference arm below is measured rather than assumed.

    Three arms, not two, for exactly that reason: `single` (one episode, one
    fault) is the unit of account. Without it, "burst costs 340 ops" is a number
    with nothing to divide by.

    Only `swap2` and `teleport` are used. Member damage is not divisible into
    equal units -- freezing eight agents at once and freezing one agent eight
    times are different experiments, and the second is ill-defined once the same
    agent can be drawn twice. See DIVISIBLE_PERTURBATIONS.

    **Eight faults is not eight times the displacement, and this is measured.**
    Swaps partially cancel and inversions saturate (45 is the maximum at n=10),
    so a single swap leaves a mean 5.63 inversions while eight at once leave
    19.0, not 45. Fixing the *fault count* fixes the intervention, not the
    distance from the goal. The drip arm therefore delivers materially more
    cumulative displacement (8 x 5.63) than the burst arm (19.0) for the same
    eight faults, and any reading of the cost comparison has to divide by
    `mean_total_damage_inv`, which is recorded per row for exactly that reason.
    A version of this experiment that compared raw ops and called the difference
    a delivery effect would be reading a displacement difference instead.

    **The comparison metric is total ops spent recovering across the whole run**,
    summed over every episode that was recovered from, plus an explicit count of
    trials that did not recover everything delivered. Reading mean cost alone
    would let an arm look cheap by failing early, which is the survivorship trap
    `exp_repeat` already had to disclose.
    """
    print("\n=== delivery: eight faults at once, or one per episode? ===")
    rows: list[dict] = []
    controllers = ["decentralized", "central_closed", "central_watchdog"]
    arms = (
        ("single", 1, 1),
        ("burst", 1, DELIVERY_TOTAL_DAMAGE),
        ("drip", DELIVERY_TOTAL_DAMAGE, 1),
    )
    for pert in DIVISIBLE_PERTURBATIONS:
        for name in controllers:
            for p in (0.0, 0.30):
                for arm, repeats, magnitude in arms:
                    ts = [
                        run_trial(
                            name, n=n, seed=1000 * k + 71, faults=Faults(p_fail=p),
                            budget=budget, perturbation=pert, perturb_on_sorted=True,
                            perturb_delay=20, perturb_repeats=repeats,
                            perturb_magnitude=magnitude, stop_on_goal=False,
                        )
                        for k in range(trials)
                    ]
                    # Only trials that reached the goal were ever disturbed.
                    faced = [x for x in ts if x.episodes]
                    # A trial "fully recovered" when every episode it was dealt
                    # came back to zero inversions. Delivering fewer episodes
                    # than requested is itself a failure to absorb the damage,
                    # so it is counted here rather than excluded.
                    full = [
                        x for x in faced
                        if len(x.episodes) == repeats
                        and all(e.recovered for e in x.episodes)
                    ]
                    total_ops = [
                        float(sum(e.ops_to_recover for e in x.episodes
                                  if e.ops_to_recover is not None))
                        for x in full
                    ]
                    damage = [
                        float(sum(e.inv_after_perturb for e in x.episodes))
                        for x in faced
                    ]
                    rows.append(dict(
                        perturbation=pert, controller=name, p_fail=p,
                        arm=arm, episodes=repeats, faults_per_episode=magnitude,
                        total_faults=repeats * magnitude,
                        trials=len(ts),
                        trials_disturbed=len(faced),
                        trials_fully_recovered=len(full),
                        full_recovery_rate=(len(full) / len(faced)) if faced else math.nan,
                        median_total_ops_to_recover=(
                            statistics.median(total_ops) if total_ops else math.nan),
                        mean_total_ops_to_recover=_mean(total_ops),
                        mean_total_damage_inv=_mean(damage),
                    ))
        # The comparison this experiment exists to make, printed per perturbation.
        for name in controllers:
            def pick(arm: str) -> dict:
                return next(r for r in rows if r["perturbation"] == pert
                            and r["controller"] == name and r["p_fail"] == 0.0
                            and r["arm"] == arm)
            one, burst, drip = pick("single"), pick("burst"), pick("drip")
            unit = one["median_total_ops_to_recover"]
            print(f"  {pert:<10} {name:<18} "
                  f"single {unit:7.1f}  "
                  f"burst {burst['median_total_ops_to_recover']:7.1f} "
                  f"({burst['median_total_ops_to_recover'] / unit:5.2f}x unit)  "
                  f"drip {drip['median_total_ops_to_recover']:7.1f} "
                  f"({drip['median_total_ops_to_recover'] / unit:5.2f}x unit)  "
                  f"full-recovery burst {burst['full_recovery_rate']:.2f} "
                  f"drip {drip['full_recovery_rate']:.2f}")
    write_csv(RESULTS / "delivery.csv", rows)

    # Total cost against delivery mode, with the eight-fault reference line the
    # passive-attractor reading predicts: 8 x the single-fault cost.
    plt = _plt()
    # Only controllers that actually recovered are drawn. A legend entry with no
    # line reads as missing data; the controllers that never recovered are named
    # in an annotation instead, with their rate, so their absence is a stated
    # result and not a gap.
    drawn = [c for c in controllers
             if any(r["controller"] == c and r["trials_fully_recovered"] > 0 for r in rows)]
    absent = [c for c in controllers if c not in drawn]
    fig, axes = plt.subplots(1, len(DIVISIBLE_PERTURBATIONS),
                             figsize=(10, 4.4), sharey=True)
    for col, pert in enumerate(DIVISIBLE_PERTURBATIONS):
        ax = axes[col]
        xs = [0, 1]
        for cname in drawn:
            def val(arm: str) -> float:
                return next(r["median_total_ops_to_recover"] for r in rows
                            if r["perturbation"] == pert and r["controller"] == cname
                            and r["p_fail"] == 0.0 and r["arm"] == arm)
            ax.plot(xs, [val("burst"), val("drip")], label=cname, **STYLE[cname])
            unit = val("single")
            ax.axhline(DELIVERY_TOTAL_DAMAGE * unit, color=STYLE[cname].get("color", "gray"),
                       alpha=0.30, linestyle=":", linewidth=1)
        ax.set(title=pert, xticks=xs)
        ax.set_xticklabels([f"burst\n({DELIVERY_TOTAL_DAMAGE} at once)",
                            f"drip\n(1 x {DELIVERY_TOTAL_DAMAGE})"])
        ax.grid(alpha=0.3)
    if absent:
        note = "; ".join(
            f"{c}: 0 of {next(r['trials'] for r in rows if r['controller'] == c)} "
            "recovered in any arm (it halts before the disturbance)"
            for c in absent)
        fig.text(0.5, 0.015, f"not plotted -- {note}", ha="center", fontsize=8,
                 color="#555555")
    axes[0].set_ylabel("median total ops to recover")
    axes[0].legend(fontsize=8, title="recovered", title_fontsize=8)
    fig.suptitle(f"Same {DELIVERY_TOTAL_DAMAGE} faults, two deliveries "
                 f"(dotted line = {DELIVERY_TOTAL_DAMAGE} x the single-fault cost)",
                 fontsize=10)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.savefig(RESULTS / "delivery.png", dpi=140)
    plt.close(fig)
    return rows


def exp_window(n: int = 10, trials: int = 300, budget: int = 20_000) -> list[dict]:
    """Disturb the array D operations after the goal is first reached.

    D=0 reproduces the naive test, where every closed-loop controller looks
    equally competent. As D grows, a controller that halts on "no inversion
    found" is no longer present to notice, while one that keeps acting is. The
    measured quantity is the width of the window in which the system is still
    goal-directed rather than merely goal-shaped."""
    print("\n=== how long does the system stay goal-directed after arriving? ===")
    rows = []
    for name in ["decentralized", "central_closed", "central_watchdog"]:
        for d in DELAY_GRID:
            ts = [
                run_trial(name, n=n, seed=1000 * k + 17, budget=budget,
                          perturbation="swap2", perturb_on_sorted=True,
                          perturb_delay=d, stop_on_goal=False)
                for k in range(trials)
            ]
            hit = [t for t in ts if t.ops_at_perturb is not None]
            rows.append(dict(
                controller=name, delay_ops=d,
                perturbed=len(hit) / len(ts),
                perturbed_after_stop=_mean([1.0 if t.perturbed_after_stop else 0.0 for t in hit]),
                goal_held_at_end=_mean([1.0 if t.inv_final == 0 else 0.0 for t in ts]),
                median_ops_to_recover=(
                    statistics.median([t.ops_to_recover for t in hit if t.recovered])
                    if any(t.recovered for t in hit) else math.nan),
            ))
        print(f"  {name:<18} goal held after damage at D=" + "  ".join(
            f"{r['delay_ops']}:{r['goal_held_at_end']:.2f}" for r in rows[-len(DELAY_GRID):]))
    write_csv(RESULTS / "window.csv", rows)

    plt = _plt()
    fig, ax = plt.subplots(figsize=(6.4, 4.4))
    for name in ["decentralized", "central_closed", "central_watchdog"]:
        sub = [r for r in rows if r["controller"] == name]
        ax.plot([r["delay_ops"] for r in sub], [r["goal_held_at_end"] for r in sub],
                label=name, **STYLE[name])
    ax.set(xlabel="operations between reaching the goal and the disturbance",
           ylabel="P(goal restored by the end of the run)",
           title="Being at the goal vs still steering toward it")
    ax.set_ylim(-0.05, 1.05)
    ax.grid(alpha=0.3)
    ax.legend(fontsize=9)
    fig.tight_layout()
    out = RESULTS / "04_window.png"
    fig.savefig(out, dpi=140)
    print(f"  wrote {out}")
    return rows


# ----------------------------------------------------------------------------
# Experiment 3: heterogeneous local rules
# ----------------------------------------------------------------------------

B_GRID = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]


def exp_hetero(n: int = 10, trials: int = 200, budget: int = 20_000) -> list[dict]:
    print("\n=== heterogeneity: where does collective competence break? ===")
    rows = []
    for p in (0.0, 0.20):
        for f in B_GRID:
            ts = [
                run_trial(
                    "decentralized", n=n, seed=1000 * k + 29, faults=Faults(p_fail=p),
                    budget=budget, rule_b_fraction=f,
                )
                for k in range(trials)
            ]
            ok = [t for t in ts if t.sorted_at_stop]
            rows.append(
                dict(
                    p_fail=p,
                    frac_type_b=f,
                    n_type_b=int(round(f * n)),
                    success_rate=len(ok) / len(ts),
                    ever_sorted_rate=_mean([1.0 if t.ever_sorted else 0.0 for t in ts]),
                    mean_inv_final=_mean([t.inv_final for t in ts]),
                    median_ops_success=(
                        statistics.median([t.ops_to_sorted for t in ok]) if ok else math.nan
                    ),
                )
            )
        print(f"  p={p}  reached/held: " + "  ".join(
            f"{r['frac_type_b']:.0%}->{r['ever_sorted_rate']:.2f}/{r['success_rate']:.2f}"
            for r in rows[-len(B_GRID):]))
    write_csv(RESULTS / "hetero.csv", rows)

    plt = _plt()
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    for p, colour in zip((0.0, 0.20), ("C0", "C3")):
        sub = [r for r in rows if r["p_fail"] == p]
        axes[0].plot([r["frac_type_b"] for r in sub], [r["success_rate"] for r in sub],
                     "o-", color=colour, label=f"p_fail={p}")
        axes[0].plot([r["frac_type_b"] for r in sub], [r["ever_sorted_rate"] for r in sub],
                     "s--", color=colour, alpha=0.6, label=f"p_fail={p} (ever reached)")
        axes[1].plot([r["frac_type_b"] for r in sub], [r["mean_inv_final"] for r in sub],
                     "o-", color=colour, label=f"p_fail={p}")
    axes[0].set(xlabel="fraction of agents running the opposing rule",
                ylabel="probability", title="Reaching the goal (dashed) vs holding it (solid)")
    axes[0].set_ylim(-0.05, 1.05)
    axes[1].set(xlabel="fraction of agents running the opposing rule",
                ylabel="mean final inversions", title="Residual distance to goal")
    for ax in axes:
        ax.grid(alpha=0.3)
        ax.legend(fontsize=8)
    fig.tight_layout()
    out = RESULTS / "03_hetero.png"
    fig.savefig(out, dpi=140)
    print(f"  wrote {out}")
    return rows


SCALE_N = [10, 20, 30, 50]
SCALE_K = [0, 1, 2, 3, 4, 6, 8]


def exp_scale(trials: int = 100) -> list[dict]:
    """Is the competence threshold a fraction of the population or a headcount?

    At N=10 one opposing agent is both "one agent" and "10% of the population",
    so the N=10 sweep cannot tell those apart. Hold the count fixed and grow the
    population: if the threshold is a fraction, k=2 stops mattering as N grows;
    if it is a headcount, k=2 breaks the collective at every N."""
    print("\n=== is the threshold a fraction or a headcount? ===")
    rows = []
    for n in SCALE_N:
        budget = 60 * n * n
        for k in SCALE_K:
            if k > n // 2:
                continue
            ts = [
                run_trial("decentralized", n=n, seed=1000 * t + 41, budget=budget,
                          n_type_b=k, stop_on_goal=True)
                for t in range(trials)
            ]
            # A second pass that is never stopped at the goal, so occupancy of
            # the goal state is measurable rather than 0 by construction.
            hold = [
                run_trial("decentralized", n=n, seed=1000 * t + 41, budget=budget,
                          n_type_b=k, stop_on_goal=False)
                for t in range(min(trials, 40))
            ]
            rows.append(dict(
                n=n, k_opposing=k, frac_opposing=k / n, budget=budget,
                ever_reached=_mean([1.0 if t.ever_sorted else 0.0 for t in ts]),
                median_ops=(statistics.median([t.ops_to_sorted for t in ts if t.ever_sorted])
                            if any(t.ever_sorted for t in ts) else math.nan),
                goal_occupancy=_mean([t.goal_occupancy for t in hold]),
                mean_inv_backhalf=_mean([t.inv_final for t in hold]),
            ))
        print(f"  N={n:<4} reached/occupancy: " + "  ".join(
            f"k={r['k_opposing']}:{r['ever_reached']:.2f}/{r['goal_occupancy']:.3f}"
            for r in rows if r["n"] == n))
    write_csv(RESULTS / "scale.csv", rows)

    plt = _plt()
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.4))
    for n in SCALE_N:
        sub = [r for r in rows if r["n"] == n]
        axes[0].plot([r["k_opposing"] for r in sub], [r["ever_reached"] for r in sub],
                     "o-", label=f"N={n}")
        axes[1].plot([r["frac_opposing"] for r in sub], [r["ever_reached"] for r in sub],
                     "o-", label=f"N={n}")
    axes[0].set(xlabel="number of agents running the opposing rule",
                ylabel="P(goal ever reached)", title="Against headcount")
    axes[1].set(xlabel="fraction of agents running the opposing rule",
                ylabel="P(goal ever reached)", title="Against fraction")
    for ax in axes:
        ax.set_ylim(-0.05, 1.05)
        ax.grid(alpha=0.3)
        ax.legend(fontsize=8)
    fig.suptitle("Whichever panel collapses the curves is the quantity that matters")
    fig.tight_layout()
    out = RESULTS / "05_scale.png"
    fig.savefig(out, dpi=140)
    print(f"  wrote {out}")
    return rows


# ----------------------------------------------------------------------------
# Experiment 4: single point of failure
# ----------------------------------------------------------------------------


def exp_single_point(n: int = 10, trials: int = 300, budget: int = 20_000) -> list[dict]:
    """Destroy one randomly chosen unit. For a centralized controller the units
    are the N agents plus the coordinator; for the decentralized one there is no
    coordinator to destroy."""
    print("\n=== single point of failure: kill one unit at random ===")
    rows = []
    for name in ["decentralized", "central_watchdog", "central_closed"]:
        n_units = n + 1 if name in HAS_COORDINATOR else n
        succ = 0
        coord_kills = 0
        for k in range(trials):
            rng = random.Random(90_000 + k)
            unit = rng.randrange(n_units)
            if unit == n:  # the coordinator
                coord_kills += 1
                # coordinator destroyed: no ops are ever issued after the kill.
                # Model the harshest honest case: it dies at the start.
                t = run_trial(name, n=n, seed=1000 * k + 31, budget=0)
            else:
                f = Faults(frozen={unit})
                t = run_trial(name, n=n, seed=1000 * k + 31, faults=f, budget=budget,
                              stop_on_goal=True)
            succ += 1 if t.sorted_at_stop else 0
        rows.append(dict(controller=name, n_units=n_units, trials=trials,
                         coordinator_kills=coord_kills, success_rate=succ / trials))
        print(f"  {name:<18} units={n_units:<3} success {succ / trials:.3f}"
              f"  (coordinator killed {coord_kills}x)")
    write_csv(RESULTS / "single_point.csv", rows)
    return rows


# ----------------------------------------------------------------------------
# Self-test
# ----------------------------------------------------------------------------


def selftest() -> None:
    assert inversions([0, 1, 2]) == 0
    assert inversions([2, 1, 3]) == 1
    assert inversions([3, 2, 1]) == 3
    assert inversions([8, 2, 6, 1, 9, 3, 7, 4, 5, 0]) == 27

    # No faults: every goal-directed controller reaches the goal.
    for name in ["decentralized", "central_open", "central_closed", "central_watchdog"]:
        for seed in range(20):
            t = run_trial(name, n=10, seed=seed, budget=20_000)
            assert t.sorted_at_stop, f"{name} failed to sort at seed {seed}"

    # The null model has the same locality and no rule: it must not sort.
    nulls = [run_trial("null_random", n=10, seed=s, budget=20_000) for s in range(20)]
    assert sum(t.sorted_at_stop for t in nulls) <= 1, "null model is sorting; rule leaked"

    # Ops accounting: every yielded step costs exactly one attempted op.
    t = run_trial("decentralized", n=10, seed=3, budget=137)
    assert t.ops_used == 137, t.ops_used

    # A dead agent partitions the line; a frozen one does not.
    dead = [run_trial("decentralized", n=10, seed=s, faults=Faults(dead={5}), budget=20_000)
            for s in range(20)]
    assert sum(t.sorted_at_stop for t in dead) < 20, "a blocking agent should sometimes prevent sorting"
    froz = [run_trial("decentralized", n=10, seed=s, faults=Faults(frozen={5}), budget=20_000)
            for s in range(20)]
    assert all(t.sorted_at_stop for t in froz), "a passive agent should be routed around"

    # Reproducibility.
    assert run_trial("decentralized", n=10, seed=42).ops_to_sorted == \
        run_trial("decentralized", n=10, seed=42).ops_to_sorted

    check_single_shot_baseline()
    print("selftest: all checks passed")


BASELINE = HERE / "single_shot_baseline.json"
BASELINE_FIELDS = [
    "ops_used", "inv_final", "ever_sorted", "ops_to_sorted", "ops_at_perturb",
    "inv_after_perturb", "recovered", "ops_to_recover", "perturbed_after_stop",
    "stopped_early", "goal_occupancy",
]


def _same(got, want) -> bool:
    if isinstance(got, float) and isinstance(want, float):
        return (math.isnan(got) and math.isnan(want)) or got == want
    return got == want


def check_single_shot_baseline() -> None:
    """Replay the 225 trials recorded before `perturb_repeats` existed.

    `single_shot_baseline.json` was captured from this file on 2026-09-06,
    immediately before the perturbation schedule learned to repeat, across five
    controllers, five perturbations, three fault rates and three seeds. The
    claim it defends is narrow and exact: **perturb_repeats=1 is the old
    behaviour**, not merely similar to it. Every result recorded before that
    date is expressed in these eleven fields, so if any of them moves, those
    results stop meaning what they said.

    Regenerate only when the schedule is deliberately redefined, and say so in
    the development log -- never to make this check pass.
    """
    # The comparator is checked before its verdict is trusted. An earlier
    # version of this replay tested floats only for NaN-ness and reported 60
    # false mismatches of 0.0 against 0.0.
    assert _same(0.0, 0.0) and _same(float("nan"), float("nan")) and _same(3, 3)
    assert not _same(0.0, 1.0) and not _same(float("nan"), 0.0)

    rows = json.loads(BASELINE.read_text())
    assert rows, "baseline is empty; a replay that compares nothing passes vacuously"
    bad = []
    for r in rows:
        t = run_trial(r["controller"], n=10, seed=r["seed"],
                      faults=Faults(p_fail=r["p"]), budget=20_000,
                      perturbation=r["pert"], perturb_on_sorted=True,
                      stop_on_goal=True)
        for f in BASELINE_FIELDS:
            if not _same(getattr(t, f), r[f]):
                bad.append(f"{r['controller']}/{r['pert']}/p={r['p']}/seed={r['seed']}"
                           f": {f} was {r[f]!r}, now {getattr(t, f)!r}")
    assert not bad, (
        f"perturb_repeats=1 no longer reproduces the pre-repeat behaviour "
        f"({len(bad)} of {len(rows) * len(BASELINE_FIELDS)} fields):\n  "
        + "\n  ".join(bad[:10])
    )


# ----------------------------------------------------------------------------


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("experiment",
                    choices=["test", "faults", "recovery", "repeat", "window",
                             "hetero", "scale", "single-point", "delivery",
                             "all"])
    ap.add_argument("-n", type=int, default=10, help="number of agents")
    ap.add_argument("--trials", type=int, default=200)
    ap.add_argument("--budget", type=int, default=20_000, help="op budget per trial")
    args = ap.parse_args()

    RESULTS.mkdir(parents=True, exist_ok=True)
    if args.experiment in ("test", "all"):
        selftest()
    if args.experiment in ("faults", "all"):
        exp_faults(args.n, args.trials, args.budget)
    if args.experiment in ("recovery", "all"):
        exp_recovery(args.n, args.trials, args.budget)
    if args.experiment in ("repeat", "all"):
        exp_repeat(args.n, args.trials, args.budget)
    if args.experiment in ("delivery", "all"):
        exp_delivery(args.n, args.trials, args.budget)
    if args.experiment in ("window", "all"):
        exp_window(args.n, args.trials, args.budget)
    if args.experiment in ("hetero", "all"):
        exp_hetero(args.n, args.trials, args.budget)
    if args.experiment in ("scale", "all"):
        exp_scale(min(args.trials, 100))
    if args.experiment in ("single-point", "all"):
        exp_single_point(args.n, max(args.trials, 300), args.budget)


if __name__ == "__main__":
    main()
