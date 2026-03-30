import pytest

from parade import verification


class TestVerification:
    def test_self_test_passes(self):
        verification.verify_orbital_mechanics()

    def test_drift_detection(self, monkeypatch):
        monkeypatch.setattr(verification, "_EXPECTED_PROBE", 999999)
        with pytest.raises(
            RuntimeError,
            match="Orbital mechanics model drift detected",
        ):
            verification.verify_orbital_mechanics()
