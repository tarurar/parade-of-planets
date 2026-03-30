import calendar

import pytest

from parade.catalog import CONSTELLATION_CATALOG
from parade.observatory import (
    chart_constellation,
    interpret_phase,
    observe_phase,
    read_constellation_chart,
)

SECRET = "test-gravitational-constant"
EPOCH = 2026


class TestObservePhase:
    def test_returns_valid_day(self):
        day = observe_phase("a", EPOCH, 1, SECRET)
        max_day = calendar.monthrange(EPOCH, 1)[1]
        assert 1 <= day <= max_day

    def test_deterministic(self):
        d1 = observe_phase("a", EPOCH, 1, SECRET)
        d2 = observe_phase("a", EPOCH, 1, SECRET)
        assert d1 == d2

    def test_different_bodies_different_days(self):
        days = {observe_phase(c, EPOCH, 1, SECRET) for c in "abcde"}
        assert len(days) == 5

    def test_rejects_invalid_body(self):
        with pytest.raises(ValueError, match="Unknown celestial body"):
            observe_phase("1", EPOCH, 1, SECRET)


class TestInterpretPhase:
    def test_returns_single_character(self):
        day = observe_phase("a", EPOCH, 1, SECRET)
        body = interpret_phase(day, EPOCH, 1, SECRET)
        assert len(body) == 1

    def test_rejects_invalid_phase(self):
        with pytest.raises(ValueError, match=r"Phase .* not observed"):
            interpret_phase(99, EPOCH, 1, SECRET)


class TestRoundTrip:
    def test_all_bodies_round_trip_january(self):
        for body in CONSTELLATION_CATALOG:
            day = observe_phase(body, EPOCH, 1, SECRET)
            recovered = interpret_phase(day, EPOCH, 1, SECRET)
            assert recovered == body

    def test_all_bodies_round_trip_february_non_leap(self):
        for body in CONSTELLATION_CATALOG:
            day = observe_phase(body, 2025, 2, SECRET)
            recovered = interpret_phase(day, 2025, 2, SECRET)
            assert recovered == body

    def test_all_bodies_round_trip_february_leap(self):
        for body in CONSTELLATION_CATALOG:
            day = observe_phase(body, 2024, 2, SECRET)
            recovered = interpret_phase(day, 2024, 2, SECRET)
            assert recovered == body

    def test_all_months(self):
        body = "z"
        for cycle in range(1, 13):
            day = observe_phase(body, EPOCH, cycle, SECRET)
            recovered = interpret_phase(day, EPOCH, cycle, SECRET)
            assert recovered == body


class TestChartConstellation:
    def test_returns_correct_number_of_entries(self):
        result = chart_constellation("hello", EPOCH, SECRET)
        assert len(result) == 5

    def test_entries_are_cycle_phase_tuples(self):
        result = chart_constellation("hello", EPOCH, SECRET)
        for cycle, phase in result:
            assert 1 <= cycle <= 12
            max_day = calendar.monthrange(EPOCH, cycle)[1]
            assert 1 <= phase <= max_day

    def test_rejects_word_longer_than_12(self):
        with pytest.raises(ValueError, match="exceeds maximum"):
            chart_constellation("a" * 13, EPOCH, SECRET)

    def test_empty_constellation_returns_empty(self):
        result = chart_constellation("", EPOCH, SECRET)
        assert result == []


class TestReadConstellationChart:
    def test_round_trip_word(self):
        word = "hello"
        chart = chart_constellation(word, EPOCH, SECRET)
        phases = [phase for _, phase in chart]
        recovered = read_constellation_chart(phases, EPOCH, SECRET)
        assert recovered == word

    def test_round_trip_with_space(self):
        word = "hi there"
        chart = chart_constellation(word, EPOCH, SECRET)
        phases = [phase for _, phase in chart]
        recovered = read_constellation_chart(phases, EPOCH, SECRET)
        assert recovered == word

    def test_round_trip_full_alphabet(self):
        word = "abcdefghijkl"
        chart = chart_constellation(word, EPOCH, SECRET)
        phases = [phase for _, phase in chart]
        recovered = read_constellation_chart(phases, EPOCH, SECRET)
        assert recovered == word


class TestGoldenDeterminism:
    def test_known_word_produces_exact_phases(self):
        result = chart_constellation("hello", 2026, "golden-test-key")
        expected = [(1, 24), (2, 23), (3, 12), (4, 4), (5, 2)]
        assert result == expected
