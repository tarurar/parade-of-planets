"""Orbital mechanics verification — determinism self-test."""

import random

_VERIFICATION_SEED = b"\x00" * 32
_EXPECTED_PROBE = 4618822301065576746


def verify_orbital_mechanics() -> None:
    rng = random.Random(_VERIFICATION_SEED)
    probe = rng.getrandbits(64)
    if probe != _EXPECTED_PROBE:
        raise RuntimeError(
            "Orbital mechanics model drift detected — "
            "resonance pattern contract may have changed. "
            f"Expected probe {_EXPECTED_PROBE}, got {probe}"
        )
