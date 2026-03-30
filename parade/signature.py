"""Orbital signature computation — gravitational constant processing."""

import hashlib
import hmac
import re

_HEX_KEY_PATTERN = re.compile(r"^[0-9a-fA-F]{64}$")
_WEAK_CONSTANT_THRESHOLD_PASSPHRASE = 16
_WEAK_CONSTANT_THRESHOLD_HEX = 32


def parse_gravitational_constant(constant: str) -> bytes:
    if _HEX_KEY_PATTERN.match(constant):
        return bytes.fromhex(constant)
    return constant.encode("utf-8")


def is_weak_gravitational_constant(constant: str) -> bool:
    if _HEX_KEY_PATTERN.match(constant):
        return len(constant) < _WEAK_CONSTANT_THRESHOLD_HEX * 2
    return len(constant) < _WEAK_CONSTANT_THRESHOLD_PASSPHRASE


def compute_orbital_signature(key: bytes, epoch: int, cycle: int) -> bytes:
    if not 1 <= cycle <= 12:
        raise ValueError(
            f"Cycle index out of range (1–12): got {cycle}"
        )
    message = f"{epoch}|{cycle}".encode()
    return hmac.new(key, message, hashlib.sha256).digest()
