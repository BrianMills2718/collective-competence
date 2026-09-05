"""Q1-003: a candidate family with a latent shared regressor.

Additive. The frozen P15 proposal path is imported and used unchanged; nothing
here modifies it, so no P15 artifact or hash is invalidated.

Local family (P15's):        next(x_i,t) = A x_i,t + b
This family:                 next(x_i,t) = A x_i,t + b + c z_t

`z_t` is one scalar per timestep shared by every entity, estimated from the data
rather than supplied: fit the local model, then take the cross-entity mean
residual at each timestep as the estimate of `c z_t`. Under genuine independence
that mean is noise around zero.

Two statistics, both frozen in the protocol before this file existed:
  shared_variance_fraction -- how much residual variance the local law leaves to
      a common component. This is the failure-to-explain adequacy report.
  persistence -- fraction of timesteps where the estimate is materially
      non-zero, which separates a sustained driver from a one-off shock.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

import numpy as np

PERSISTENCE_THRESHOLD = 0.1  # fraction of the estimate's own peak magnitude


@dataclass(frozen=True)
class SharedDriverReport:
    shared_variance_fraction: float
    persistence: float
    local_residual_variance: float
    residual_variance_after_shared: float
    n_entities: int
    n_transitions: int


def _stack(package: dict[str, Any]) -> tuple[np.ndarray, np.ndarray]:
    """Return (current, following) arrays shaped (unit, time, entity, field)."""
    units = []
    for unit in package["units"]:
        frames = sorted(unit["frames"], key=lambda f: f["time"])
        rows = []
        for frame in frames:
            entities = sorted(frame["entities"], key=lambda e: e["entity_id"])
            rows.append([[e["values"]["f000"], e["values"]["f001"]] for e in entities])
        units.append(np.asarray(rows, dtype=float))
    stacked = np.asarray(units)  # (unit, time, entity, field)
    return stacked[:, :-1], stacked[:, 1:]


def analyze(package: dict[str, Any]) -> SharedDriverReport:
    current, following = _stack(package)
    n_units, n_time, n_entities, n_fields = current.shape

    # Fit the shared local law exactly as the local family does: one A, b for all
    # entities, each entity treated independently.
    x = current.reshape(-1, n_fields)
    y = following.reshape(-1, n_fields)
    design = np.hstack([x, np.ones((x.shape[0], 1))])
    coef, *_ = np.linalg.lstsq(design, y, rcond=None)
    residual = (y - design @ coef).reshape(n_units, n_time, n_entities, n_fields)

    # The common component: cross-entity mean residual per (unit, time).
    shared = residual.mean(axis=2, keepdims=True)          # (unit, time, 1, field)
    remaining = residual - shared

    local_var = float(np.var(residual))
    after_var = float(np.var(remaining))
    fraction = 0.0 if local_var <= 0 else max(0.0, (local_var - after_var) / local_var)

    # Persistence: how much of the run does the shared estimate stay live?
    magnitude = np.linalg.norm(shared[:, :, 0, :], axis=-1)  # (unit, time)
    peak = magnitude.max(axis=1, keepdims=True)
    live = np.where(peak > 0, magnitude / np.where(peak > 0, peak, 1.0), 0.0)
    persistence = float((live > PERSISTENCE_THRESHOLD).mean())

    return SharedDriverReport(
        shared_variance_fraction=fraction,
        persistence=persistence,
        local_residual_variance=local_var,
        residual_variance_after_shared=after_var,
        n_entities=n_entities,
        n_transitions=int(n_units * n_time * n_entities),
    )


def report_dict(package: dict[str, Any]) -> dict[str, Any]:
    return asdict(analyze(package))
