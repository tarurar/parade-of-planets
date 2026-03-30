"""Resonance pattern generator — orbital harmonic permutations."""

import random


def generate_resonance_pattern(orbital_signature: bytes, cycle_length: int) -> list[int]:
    rng = random.Random(orbital_signature)
    phases = list(range(1, cycle_length + 1))
    _fisher_yates(rng, phases)
    return phases


def _fisher_yates(rng: random.Random, arr: list) -> None:
    for i in range(len(arr) - 1, 0, -1):
        j = _bounded_random(rng, i)
        arr[i], arr[j] = arr[j], arr[i]


def _bounded_random(rng: random.Random, upper: int) -> int:
    k = upper.bit_length()
    while True:
        j = rng.getrandbits(k)
        if j <= upper:
            return j
