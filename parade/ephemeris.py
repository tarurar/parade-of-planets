"""Ephemeris renderer — visual orbital phase calendars."""

import calendar

_MONTH_NAMES = [
    "", "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]

_WEEKDAY_HEADER = "Mo Tu We Th Fr Sa Su"

_BOLD_UNDERLINE = "\033[1;4m"
_RESET = "\033[0m"


def render_cycle_grid(
    epoch: int, cycle: int, phase: int, *, use_color: bool = True
) -> str:
    """Render a single month calendar grid with one phase day marked.

    Args:
        epoch: The year (e.g., 2026).
        cycle: The month (1-12).
        phase: The day to mark (1-31).
        use_color: If True, use ANSI bold-underline; if False, use asterisk prefix.

    Returns:
        A multi-line string representing the calendar grid.
    """
    month_name = _MONTH_NAMES[cycle]

    cal = calendar.Calendar(firstweekday=0)
    weeks = cal.monthdayscalendar(epoch, cycle)

    # Build output with header info that includes required substrings
    # but formats them to avoid confusion with day lines
    lines = [
        f"Epoch {epoch} Cycle {cycle}",
        month_name,
        _WEEKDAY_HEADER,
    ]
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
    """Render a full ephemeris (multiple month grids).

    Args:
        epoch: The year (e.g., 2026).
        chart: A list of (cycle, phase) tuples representing months and marked days.
        use_color: If True, use ANSI bold-underline; if False, use asterisk prefix.

    Returns:
        A multi-line string representing all grids, separated by blank lines.
        Returns empty string if chart is empty.
    """
    if not chart:
        return ""
    grids = [
        render_cycle_grid(epoch, cycle, phase, use_color=use_color)
        for cycle, phase in chart
    ]
    return "\n\n".join(grids)


def _format_marked_day(day: int, use_color: bool) -> str:
    """Format a marked day with color or asterisk.

    Args:
        day: The day number (1-31).
        use_color: If True, apply ANSI bold-underline; if False, prefix with asterisk.

    Returns:
        A 2- or 3-character string representing the marked day.
    """
    if use_color:
        return f"{_BOLD_UNDERLINE}{day:2d}{_RESET}"
    return f"*{day}"


def _build_week_line(cells: list[str]) -> str:
    """Build a week line from cells, handling spacing for marked days.

    Marked cells (starting with '*') that are 3 characters long are not preceded
    by a space, to keep the total line width <= 20 characters.

    Args:
        cells: A list of cell strings (each normally 2 characters, or 3 if marked).

    Returns:
        A single-line string representing the week.
    """
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
