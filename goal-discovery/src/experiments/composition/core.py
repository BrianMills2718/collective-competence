"""Compare ordinary validated pipelines with executable DisCoPy diagrams.

The same functions interpret every box in both paths. Immutable JSON snapshots
carry the entire state, including RNG. This is a category of experiment steps,
not cell-level open games, lenses, or a proof of compositional competencies.
"""

from __future__ import annotations

import json
import math
import random
from collections.abc import Callable
from dataclasses import asdict, dataclass, replace
from itertools import pairwise, zip_longest
from typing import Any

from discopy import monoidal as diagram
from discopy import python as semantics

from src.experiments.bowl.model import BowlWorld
from src.experiments.sorting.interventions import Intervention, apply
from src.experiments.sorting.model import ALL_ARMS, Freeze, SortingWorld

SYSTEMS = ("sorting", "bowl")
INTERVENTIONS = ("environment", "state", "freeze")
ORDERS = ("shuffled", "index", "reverse_index")


@dataclass(frozen=True)
class Config:
    system: str = "sorting"
    seed: int = 7
    n: int = 12
    ticks: int = 80
    at: int = 20
    intervention: str = "environment"
    algotype: str = "bubble"
    order: str = "shuffled"
    changed_order: str = "reverse_index"

    def __post_init__(self) -> None:
        if self.system not in SYSTEMS or self.intervention not in INTERVENTIONS:
            raise ValueError("Unsupported system or intervention")
        if not 4 <= self.n <= 64 or not 2 <= self.ticks <= 400:
            raise ValueError("Use 4..64 components and 2..400 ticks for this bounded pilot")
        if not 0 <= self.at < self.ticks:
            raise ValueError("Intervention time must precede the final tick")
        if self.algotype not in ALL_ARMS:
            raise ValueError("Unknown sorting rule")
        if self.order not in ORDERS or self.changed_order not in ORDERS:
            raise ValueError("Unknown scheduler")


@dataclass(frozen=True)
class Snapshot:
    system: str
    payload: str

    def unpack(self) -> dict[str, Any]:
        return json.loads(self.payload)


@dataclass(frozen=True)
class Prepared:
    snapshot: Snapshot


@dataclass(frozen=True)
class Sample:
    snapshot: Snapshot  # retained for exact replay, not passed as a blind observation
    tick: int
    values: tuple[float, ...]
    identities: tuple[int, ...]
    inactive: tuple[bool, ...]
    metric: float
    metric_name: str
    steps: int
    rms_speed: float | None = None


World = SortingWorld | BowlWorld


def pack(system: str, world: World) -> Snapshot:
    return Snapshot(system, json.dumps(world.snapshot(), sort_keys=True, separators=(",", ":")))


def restore(snapshot: Snapshot) -> World:
    if snapshot.system == "sorting":
        world = SortingWorld.from_values([])
    elif snapshot.system == "bowl":
        world = BowlWorld.from_seed(0, 0)
    else:
        raise ValueError("Unsupported snapshot system")
    world.restore(snapshot.unpack())
    return world


def initial(config: Config, arm: str = "baseline") -> Snapshot:
    if arm not in ("baseline", "changed", "null"):
        raise ValueError("Unknown comparison arm")
    if config.system == "sorting":
        values = list(range(config.n))
        random.Random(config.seed).shuffle(values)
        world = SortingWorld.from_values(
            values,
            "random_swap" if arm == "null" else config.algotype,
            order=config.order,
            seed=config.seed,
        )
    else:
        world = BowlWorld.from_seed(config.n, config.seed)
        if arm == "null":
            for coordinate in world.coords:
                coordinate.frozen = True
    return pack(config.system, world)


def change_context(world: World, config: Config, arm: str) -> None:
    """External experiment schedule, called before the tick's native transition.

    Context here is externally prescribed, not a reciprocal adapting environment.
    State/freeze interventions fire once; environment replacement persists.
    """
    if arm != "changed" or world.tick < config.at:
        return
    if config.intervention == "environment":
        if isinstance(world, SortingWorld):
            world.order = config.changed_order
        else:
            world.damping = 0.0
    elif world.tick == config.at:
        if isinstance(world, SortingWorld):
            intervention = (
                Intervention("block_swap", {"fraction": 0.25})
                if config.intervention == "state"
                else Intervention(
                    "freeze_cells", {"positions": [config.n // 2], "mode": Freeze.IMMOVABLE.value}
                )
            )
            apply(world, intervention, config.seed + 10000)
        elif config.intervention == "state":
            for coordinate in world.coords:
                coordinate.x += 5.0
        else:
            world.coords[0].frozen = True


def readout(snapshot: Snapshot) -> Sample:
    world = restore(snapshot)
    if isinstance(world, SortingWorld):
        values = tuple(world.values)
        inversions = sum(a > b for i, a in enumerate(values) for b in values[i + 1 :])
        metric = inversions / (len(values) * (len(values) - 1) / 2)
        identities = tuple(c.cell_id for c in world.cells)
        inactive = tuple(not c.acts for c in world.cells)
        metric_name = "Inversion fraction (supplied probe)"
    else:
        values = tuple(world.positions)
        metric = math.sqrt(sum(x * x for x in values) / len(values))
        identities = tuple(c.coord_id for c in world.coords)
        inactive = tuple(c.frozen for c in world.coords)
        metric_name = "RMS distance from zero (supplied probe)"
    speed = (
        None
        if isinstance(world, SortingWorld)
        else math.sqrt(sum(v * v for v in world.velocities) / len(world.coords))
    )
    return Sample(
        snapshot, world.tick, values, identities, inactive, metric, metric_name, world.steps, speed
    )


@dataclass(frozen=True)
class Stage:
    name: str
    source: str
    target: str
    input_class: type
    output_class: type
    function: Callable

    def __call__(self, value: Any) -> Any:
        if not isinstance(value, self.input_class):
            raise TypeError(f"{self.name} requires {self.input_class.__name__}")
        result = self.function(value)
        if not isinstance(result, self.output_class):
            raise TypeError(f"{self.name} returned an invalid value")
        return result


class Pipeline:
    """Ordinary Python gets real connection checks too: this is the fair baseline."""

    def __init__(self, stages: tuple[Stage, ...]):
        if not stages:
            raise ValueError("A pipeline requires stages")
        for left, right in pairwise(stages):
            if left.target != right.source or left.output_class != right.input_class:
                raise ValueError(f"Incompatible wiring: {left.target} -> {right.source}")
        self.stages = stages

    def __call__(self, value: Any) -> Any:
        for stage in self.stages:
            value = stage(value)
        return value


def stages_for(config: Config, arm: str) -> tuple[Stage, ...]:
    if arm not in ("baseline", "changed", "null"):
        raise ValueError("Unknown arm")
    state, prepared, sample = (
        f"{config.system}:{name}" for name in ("State", "Prepared", "Sample")
    )

    def context(snapshot: Snapshot) -> Prepared:
        if snapshot.system != config.system:
            raise ValueError("Cross-system state supplied to this interface")
        world = restore(snapshot)
        change_context(world, config, arm)
        return Prepared(pack(config.system, world))

    def transition(value: Prepared) -> Snapshot:
        if value.snapshot.system != config.system:
            raise ValueError("Cross-system prepared state supplied to transition")
        world = restore(value.snapshot)
        world.step_tick()
        return pack(config.system, world)

    def observe(snapshot: Snapshot) -> Sample:
        if snapshot.system != config.system:
            raise ValueError("Cross-system snapshot supplied to readout")
        return readout(snapshot)

    return (
        Stage(f"Context: {arm}", state, prepared, Snapshot, Prepared, context),
        Stage("Existing transition", prepared, state, Prepared, Snapshot, transition),
        Stage("Readout", state, sample, Snapshot, Sample, observe),
    )


def categorical(stages: tuple[Stage, ...]):
    """Return the actual diagram, its interpreter, and its atomic boxes.

    DisCoPy owns composition/identity/tensor, rather than a home-grown category
    implementation. The interpreted diagram—not a separately coded executor—is run.
    """
    if not stages:
        raise ValueError("A diagram requires stages")
    boxes = tuple(diagram.Box(s.name, diagram.Ty(s.source), diagram.Ty(s.target)) for s in stages)
    objects = {}
    arrows = {}
    meanings = {}
    for box, stage in zip(boxes, stages):
        for port, cls in ((box.dom, stage.input_class), (box.cod, stage.output_class)):
            if port in objects and objects[port] != (cls,):
                raise ValueError(f"Conflicting type interpretation for {port}")
            objects[port] = (cls,)
        if box in meanings and meanings[box] != stage:
            raise ValueError(f"Conflicting box interpretation for {box}")
        meanings[box] = stage
        arrows[box] = semantics.Function(stage, (stage.input_class,), (stage.output_class,))
    interpreter = diagram.Functor(
        objects, arrows, cod=diagram.Category(semantics.Ty, semantics.Function)
    )
    wired = boxes[0]
    for box in boxes[1:]:
        wired = wired >> box
    return wired, interpreter, boxes


def run(config: Config, arm: str = "baseline", backend: str = "python") -> list[Sample]:
    stages = stages_for(config, arm)
    if backend == "python":
        execute = Pipeline(stages)
    elif backend == "discopy":
        wired, interpreter, _ = categorical(stages)
        execute = interpreter(wired)
    elif backend == "native":
        # Independent direct call order verifies that BOTH wrappers preserve the kernel.
        world = restore(initial(config, arm))
        result = [readout(pack(config.system, world))]
        for _ in range(config.ticks):
            change_context(world, config, arm)
            world.step_tick()
            result.append(readout(pack(config.system, world)))
        return result
    else:
        raise ValueError("Unknown execution backend")
    snapshot = initial(config, arm)
    result = [readout(snapshot)]
    for _ in range(config.ticks):
        sample = execute(snapshot)
        result.append(sample)
        snapshot = sample.snapshot
    return result


def compare(config: Config) -> dict[str, Any]:
    arms = {}
    for arm in ("baseline", "changed", "null"):
        direct = run(config, arm, "python")
        composed = run(config, arm, "discopy")
        native = run(config, arm, "native")
        mismatches = [
            i
            for i, (a, b, c) in enumerate(zip_longest(direct, composed, native))
            if a != b or a != c
        ]
        arms[arm] = {"samples": [asdict(s) for s in composed], "mismatch_ticks": mismatches}
    return {
        "config": asdict(config),
        "arms": arms,
        "exact_match": all(not a["mismatch_ticks"] for a in arms.values()),
        "evidence_grade": "White-box composition calibration; no goals inferred",
        "intervention_convention": "Applied before transition at t; first post-event sample is t+1",
        "null_convention": "Null differs in mechanism from t=0; not a matched intervention branch",
        "environment_limit": "Sorting scheduler replacement also changes shared RNG consumption; "
        "not an isolated activation-order effect. Bowl damping is a prescribed physical parameter.",
        "environment_noop": config.system == "sorting"
        and config.intervention == "environment"
        and config.order == config.changed_order,
    }


def law_checks(config: Config) -> dict[str, bool]:
    stages = stages_for(config, "baseline")
    wired, interpreter, (context, step, observe) = categorical(stages)
    snapshot = initial(config)
    other = initial(replace(config, seed=config.seed + 1))
    original = snapshot.payload
    pipeline = Pipeline(stages)
    bad_python = False
    bad_diagram = False
    try:
        Pipeline((stages[2], stages[1]))
    except ValueError:
        bad_python = True
    try:
        observe >> step
    except Exception as error:
        # DisCoPy AxiomError (specific version) is checked instead of swallowed.
        from discopy.utils import AxiomError

        if not isinstance(error, AxiomError):
            raise
        bad_diagram = True
    left = ((context >> step) @ (context >> step)) >> (observe @ observe)
    right = (context @ context) >> (step @ step) >> (observe @ observe)
    return {
        "python_rejects_invalid_wiring": bad_python,
        "discopy_rejects_invalid_wiring": bad_diagram,
        "identity": interpreter(diagram.Id(wired.dom) >> wired)(snapshot) == pipeline(snapshot),
        "right_identity": interpreter(wired >> diagram.Id(wired.cod))(snapshot)
        == pipeline(snapshot),
        "regrouping": interpreter((context >> step) >> observe)(snapshot)
        == interpreter(context >> (step >> observe))(snapshot),
        "independent_tensor": interpreter(wired @ wired)(snapshot, other)
        == (pipeline(snapshot), pipeline(other)),
        "interchange": interpreter(left)(snapshot, other) == interpreter(right)(snapshot, other),
        "input_unchanged": snapshot.payload == original,
    }
