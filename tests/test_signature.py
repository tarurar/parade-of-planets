import hashlib
import hmac

import pytest

from parade.signature import compute_orbital_signature, parse_gravitational_constant


class TestParseGravitationalConstant:
    def test_passphrase_returns_utf8_bytes(self):
        result = parse_gravitational_constant("my secret")
        assert result == b"my secret"

    def test_hex_64_chars_returns_raw_bytes(self):
        hex_key = "aa" * 32
        result = parse_gravitational_constant(hex_key)
        assert result == bytes.fromhex(hex_key)
        assert len(result) == 32

    def test_hex_detection_case_insensitive(self):
        hex_key = "AA" * 32
        result = parse_gravitational_constant(hex_key)
        assert result == bytes.fromhex(hex_key)

    def test_non_hex_64_chars_treated_as_passphrase(self):
        not_hex = "g" * 64
        result = parse_gravitational_constant(not_hex)
        assert result == not_hex.encode("utf-8")

    def test_short_hex_treated_as_passphrase(self):
        short_hex = "aa" * 16
        result = parse_gravitational_constant(short_hex)
        assert result == short_hex.encode("utf-8")


class TestComputeOrbitalSignature:
    def test_returns_32_bytes(self):
        sig = compute_orbital_signature(b"key", 2026, 3)
        assert len(sig) == 32

    def test_deterministic(self):
        sig1 = compute_orbital_signature(b"key", 2026, 3)
        sig2 = compute_orbital_signature(b"key", 2026, 3)
        assert sig1 == sig2

    def test_different_epoch_different_signature(self):
        sig1 = compute_orbital_signature(b"key", 2026, 3)
        sig2 = compute_orbital_signature(b"key", 2027, 3)
        assert sig1 != sig2

    def test_different_cycle_different_signature(self):
        sig1 = compute_orbital_signature(b"key", 2026, 3)
        sig2 = compute_orbital_signature(b"key", 2026, 4)
        assert sig1 != sig2

    def test_different_key_different_signature(self):
        sig1 = compute_orbital_signature(b"key1", 2026, 3)
        sig2 = compute_orbital_signature(b"key2", 2026, 3)
        assert sig1 != sig2

    def test_matches_manual_hmac(self):
        key = b"test-key"
        msg = b"2026|3"
        expected = hmac.new(key, msg, hashlib.sha256).digest()
        result = compute_orbital_signature(key, 2026, 3)
        assert result == expected

    def test_cycle_validation_rejects_zero(self):
        with pytest.raises(ValueError, match="Cycle index out of range"):
            compute_orbital_signature(b"key", 2026, 0)

    def test_cycle_validation_rejects_13(self):
        with pytest.raises(ValueError, match="Cycle index out of range"):
            compute_orbital_signature(b"key", 2026, 13)
