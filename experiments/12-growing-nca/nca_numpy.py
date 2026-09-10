"""NumPy inference adapter for the pinned Growing Neural Cellular Automata model.

This is an independent CPU translation of the published WebGL inference path in
``public/ca.js`` at the commit pinned by ``upstream_manifest.json``. It decodes
the authors' pretrained quantized weights; it does not train or alter the model.
"""
from __future__ import annotations

import base64
import json
from pathlib import Path

import numpy as np

CHANNELS = 16
MAX_ACTIVATION = 10.0
C = np.arctan(MAX_ACTIVATION)
SOBEL_X = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32) / 8.0
SOBEL_Y = SOBEL_X.T


def _quantize(x: np.ndarray, relu: bool = False) -> np.ndarray:
    if relu:
        x = np.maximum(x, 0.0)
        encoded = np.arctan(x) / C
        q = np.rint(np.clip(encoded, 0.0, 1.0) * 255.0) / 255.0
        return np.tan(q * C).astype(np.float32)
    encoded = np.arctan(x) / (2.0 * C) + 127.0 / 255.0
    q = np.rint(np.clip(encoded, 0.0, 1.0) * 255.0) / 255.0
    return np.tan((q - 127.0 / 255.0) * (2.0 * C)).astype(np.float32)


def _decode_layer(spec: dict) -> tuple[np.ndarray, np.ndarray]:
    raw = np.frombuffer(base64.b64decode(spec["data_b64"]), dtype=np.uint8)
    packed = raw.reshape(spec["in_ch"] + 1, spec["out_ch"]).astype(np.float32) / 255.0
    weights = (packed[:-1] - 0.5) * float(spec["weight_scale"])
    bias = (packed[-1] - 0.5) * float(spec["bias_scale"])
    return weights.astype(np.float32), bias.astype(np.float32)


def load_model(path: str | Path):
    specs = json.loads(Path(path).read_text())
    if [(x["in_ch"], x["out_ch"]) for x in specs] != [(48, 128), (128, 16)]:
        raise ValueError("unexpected Growing NCA layer shapes")
    return _decode_layer(specs[0]), _decode_layer(specs[1])


def _sample_offset(x: np.ndarray, dy: int, dx: int) -> np.ndarray:
    # public/ca.js wraps reads with fract(...), so inference is toroidal.
    return np.roll(x, shift=(-dy, -dx), axis=(0, 1))


def _filter3(x: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    out = np.zeros_like(x, dtype=np.float32)
    for iy, dy in enumerate((-1, 0, 1)):
        for ix, dx in enumerate((-1, 0, 1)):
            out += kernel[iy, ix] * _sample_offset(x, dy, dx)
    return out


def _max3(a: np.ndarray) -> np.ndarray:
    return np.maximum.reduce([
        _sample_offset(a, dy, dx)
        for dy in (-1, 0, 1)
        for dx in (-1, 0, 1)
    ])


def seed_state(size: int = 96) -> np.ndarray:
    state = np.zeros((size, size, CHANNELS), dtype=np.float32)
    cell = np.ones(CHANNELS, dtype=np.float32)
    cell[:3] = 0.0
    cell[3] = 1.0
    state[size // 2, size // 2] = _quantize(cell)
    return state


def visible_rgb(state: np.ndarray) -> np.ndarray:
    rgba = state[..., :4]
    rgb = 1.0 - rgba[..., 3:4] + rgba[..., :3]
    return np.clip(rgb, 0.0, 1.0)


def clear_circle(state: np.ndarray, y: int, x: int, radius: float) -> None:
    h, w, _ = state.shape
    yy, xx = np.mgrid[:h, :w]
    dy = np.minimum(np.abs(yy - y), h - np.abs(yy - y))
    dx = np.minimum(np.abs(xx - x), w - np.abs(xx - x))
    state[np.sqrt(dx * dx + dy * dy) < radius] = 0.0


class NCA:
    def __init__(self, model_path: str | Path, size: int = 96, seed: int = 0):
        self.layer1, self.layer2 = load_model(model_path)
        self.state = seed_state(size)
        self.rng = np.random.default_rng(seed)
        self.steps = 0

    def step(self, update_gate: np.ndarray | None = None) -> None:
        """Advance once, optionally suppressing updates without changing RNG use.

        ``update_gate`` is a per-cell multiplier applied only after the native
        stochastic update mask has been drawn. This is an intervention seam for
        matched action-availability tests; it does not overwrite cell state.
        """
        w1, b1 = self.layer1
        w2, b2 = self.layer2
        state = self.state
        perception = np.concatenate([
            state,
            _filter3(state, SOBEL_X),
            _filter3(state, SOBEL_Y),
        ], axis=-1)
        perception = _quantize(perception)
        hidden = perception.reshape(-1, 48) @ w1 + b1
        hidden = _quantize(hidden.reshape(*state.shape[:2], 128), relu=True)
        update = hidden.reshape(-1, 128) @ w2 + b2
        update = _quantize(update.reshape(state.shape))
        mask = (self.rng.random((*state.shape[:2], 1)) <= 0.5).astype(np.float32)
        if update_gate is not None:
            gate = np.asarray(update_gate, dtype=np.float32)
            if gate.shape == state.shape[:2]:
                gate = gate[..., None]
            if gate.shape != (*state.shape[:2], 1):
                raise ValueError("update_gate must match the NCA grid")
            if np.any((gate < 0.0) | (gate > 1.0)):
                raise ValueError("update_gate values must lie in [0, 1]")
            mask = mask * gate
        masked = _quantize(update * mask)
        pre = _max3(state[..., 3])
        post = _max3(state[..., 3] + masked[..., 3])
        alive = np.minimum(pre, post) >= 0.1
        new_state = _quantize(state + masked)
        new_state[~alive] = 0.0
        self.state = new_state
        self.steps += 1

    def run(self, n: int) -> np.ndarray:
        for _ in range(n):
            self.step()
        return self.state

    def damage(self, y: int, x: int, radius: float = 8.0) -> None:
        clear_circle(self.state, y, x, radius)


def mse_rgb(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.mean((visible_rgb(a) - visible_rgb(b)) ** 2))


def live_fraction(state: np.ndarray) -> float:
    return float(np.mean(state[..., 3] > 0.1))
