"""Constellation catalog — the registry of known celestial bodies."""

CONSTELLATION_CATALOG = "abcdefghijklmnopqrstuvwxyz "

_BODY_TO_INDEX = {body: i for i, body in enumerate(CONSTELLATION_CATALOG)}


def catalog_size() -> int:
    return len(CONSTELLATION_CATALOG)


def celestial_body_index(body: str) -> int:
    validate_celestial_body(body)
    return _BODY_TO_INDEX[body]


def celestial_body_at(index: int) -> str:
    if not 0 <= index < len(CONSTELLATION_CATALOG):
        raise ValueError(
            f"Celestial body index out of range: "
            f"expected 0–{len(CONSTELLATION_CATALOG) - 1}, got {index}"
        )
    return CONSTELLATION_CATALOG[index]


def validate_celestial_body(body: str) -> None:
    if body not in _BODY_TO_INDEX:
        raise ValueError(
            f"Unknown celestial body '{body}': "
            f"not found in constellation catalog"
        )
