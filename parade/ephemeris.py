"""Ephemeris renderer — visual orbital phase calendars."""

import calendar

_MONTH_NAMES = [
    "",
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

_WEEKDAY_HEADER = "Mo Tu We Th Fr Sa Su"

_BOLD_UNDERLINE = "\033[1;4m"
_RESET = "\033[0m"


def render_cycle_grid(epoch: int, cycle: int, phase: int, *, use_color: bool = True) -> str:
    month_name = _MONTH_NAMES[cycle]
    header = f"\u2550\u2550 Epoch {epoch} \u2014 Cycle {cycle} ({month_name}) \u2550\u2550"

    cal = calendar.Calendar(firstweekday=0)
    weeks = cal.monthdayscalendar(epoch, cycle)

    lines = [header, _WEEKDAY_HEADER]
    for week in weeks:
        cells = []
        for day in week:
            if day == 0:
                cells.append("  ")
            elif day == phase:
                cells.append(_format_marked_day(day, use_color))
            else:
                cells.append(f"{day:2d}")
        lines.append(_build_week_line(cells))

    return "\n".join(lines)


def render_ephemeris(
    epoch: int,
    chart: list[tuple[int, int]],
    *,
    use_color: bool = True,
) -> str:
    if not chart:
        return ""
    grids = [render_cycle_grid(epoch, cycle, phase, use_color=use_color) for cycle, phase in chart]
    return "\n\n".join(grids)


def _format_marked_day(day: int, use_color: bool) -> str:
    if use_color:
        return f"{_BOLD_UNDERLINE}{day:2d}{_RESET}"
    return f"*{day}"


def _build_week_line(cells: list[str]) -> str:
    parts = []
    for i, cell in enumerate(cells):
        if i == 0:
            parts.append(cell)
        elif cell.startswith("*") and len(cell) == 3:
            # Marked double-digit day: no space before it
            parts.append(cell)
        else:
            # Unmarked or marked single-digit: space before
            parts.append(" " + cell)
    return "".join(parts)
