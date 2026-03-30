import pytest

from parade.ephemeris import render_cycle_grid, render_ephemeris


class TestRenderCycleGrid:
    def test_header_contains_epoch_and_cycle(self):
        grid = render_cycle_grid(2026, 1, 17, use_color=False)
        assert "Epoch 2026" in grid
        assert "Cycle 1" in grid
        assert "January" in grid

    def test_marked_day_has_asterisk_no_color(self):
        grid = render_cycle_grid(2026, 1, 17, use_color=False)
        assert "*17" in grid

    def test_all_days_present(self):
        grid = render_cycle_grid(2026, 1, 17, use_color=False)
        for d in range(1, 32):
            assert str(d) in grid

    def test_weekday_header_present(self):
        grid = render_cycle_grid(2026, 1, 17, use_color=False)
        assert "Mo" in grid
        assert "Su" in grid

    def test_no_column_shift_from_marker(self):
        grid = render_cycle_grid(2026, 1, 5, use_color=False)
        lines = grid.strip().split("\n")
        weekday_idx = next(i for i, l in enumerate(lines) if l.startswith("Mo"))
        week_lines = lines[weekday_idx + 1:]
        for line in week_lines:
            assert len(line.rstrip()) <= 20

    def test_february_non_leap(self):
        grid = render_cycle_grid(2025, 2, 14, use_color=False)
        assert "28" in grid
        assert "29" not in grid

    def test_february_leap(self):
        grid = render_cycle_grid(2024, 2, 14, use_color=False)
        assert "29" in grid


class TestRenderEphemeris:
    def test_renders_multiple_cycles(self):
        chart = [(1, 17), (2, 5), (3, 22)]
        output = render_ephemeris(2026, chart, use_color=False)
        assert "Cycle 1" in output
        assert "Cycle 2" in output
        assert "Cycle 3" in output

    def test_empty_chart(self):
        output = render_ephemeris(2026, [], use_color=False)
        assert output == ""
