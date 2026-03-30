"""Observatory — observe and interpret celestial phase alignments."""

import calendar

from parade.catalog import (
    celestial_body_index,
    celestial_body_at,
    validate_celestial_body,
    catalog_size,
)
from parade.signature import compute_orbital_signature, parse_gravitational_constant
from parade.resonance import generate_resonance_pattern
from parade.verification import verify_orbital_mechanics

verify_orbital_mechanics()

_MAX_CONSTELLATION_LENGTH = 12


def observe_phase(body: str, epoch: int, cycle: int, constant: str) -> int:
    validate_celestial_body(body)
    pattern = _build_resonance(epoch, cycle, constant)
    index = celestial_body_index(body)
    return pattern[index]


def interpret_phase(phase: int, epoch: int, cycle: int, constant: str) -> str:
    pattern = _build_resonance(epoch, cycle, constant)
    try:
        index = pattern.index(phase)
    except ValueError:
        raise ValueError(
            f"Phase {phase} not observed in epoch {epoch}, cycle {cycle}"
        )
    if index >= catalog_size():
        raise ValueError(
            f"Phase {phase} not observed in epoch {epoch}, cycle {cycle} "
            f"(silent phase — not mapped to any celestial body)"
        )
    return celestial_body_at(index)


def chart_constellation(
    constellation: str, epoch: int, constant: str
) -> list[tuple[int, int]]:
    if len(constellation) > _MAX_CONSTELLATION_LENGTH:
        raise ValueError(
            f"Constellation length {len(constellation)} exceeds maximum "
            f"of {_MAX_CONSTELLATION_LENGTH} celestial bodies"
        )
    return [
        (cycle, observe_phase(body, epoch, cycle, constant))
        for cycle, body in enumerate(constellation, start=1)
    ]


def read_constellation_chart(
    phases: list[int], epoch: int, constant: str
) -> str:
    return "".join(
        interpret_phase(phase, epoch, cycle, constant)
        for cycle, phase in enumerate(phases, start=1)
    )


def _build_resonance(epoch: int, cycle: int, constant: str) -> list[int]:
    key = parse_gravitational_constant(constant)
    signature = compute_orbital_signature(key, epoch, cycle)
    days_in_cycle = calendar.monthrange(epoch, cycle)[1]
    return generate_resonance_pattern(signature, days_in_cycle)
