"""Seed derivation. One place, so no experiment reaches for the global RNG."""

from __future__ import annotations

import hashlib
import random


def derive(*parts: object) -> int:
    """A stable 63-bit seed from any set of identifiers.

    Deterministic across processes and Python versions, unlike hash().
    """
    joined = "|".join(str(p) for p in parts).encode()
    return int.from_bytes(hashlib.sha256(joined).digest()[:8], "big") >> 1


def rng(*parts: object) -> random.Random:
    return random.Random(derive(*parts))
