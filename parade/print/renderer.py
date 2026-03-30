"""Ephemeris chart renderer — printable orbital phase calendars."""

import calendar
import math

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas

_MONTH_ABBR = [
    "", "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
]

_WEEKDAY_HEADERS = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]

_MARGIN = 15 * mm
_YEAR_GAP = 8 * mm
_MONTH_COLS = 4
_MONTH_ROWS = 3


def render_ephemeris_pdf(start_year: int, num_years: int, output_path: str) -> None:
    page_width, page_height = A4
    total_pages = math.ceil(num_years / 2)
    c = Canvas(output_path, pagesize=A4)

    content_width = page_width - 2 * _MARGIN
    content_height = page_height - 2 * _MARGIN
    year_block_height = (content_height - _YEAR_GAP) / 2

    for page_idx in range(total_pages):
        if page_idx > 0:
            c.showPage()

        _draw_page_number(c, page_width, page_idx + 1, total_pages)

        for slot in range(2):
            year_idx = page_idx * 2 + slot
            if year_idx >= num_years:
                break

            year = start_year + year_idx
            block_top = page_height - _MARGIN - slot * (year_block_height + _YEAR_GAP)

            _draw_year_block(c, year, _MARGIN, block_top, content_width, year_block_height)

    c.save()


def _draw_page_number(c: Canvas, page_width: float, current: int, total: int) -> None:
    c.setFont("Helvetica", 7)
    c.drawRightString(page_width - _MARGIN, _MARGIN - 10, f"[{current}/{total}]")


def _draw_year_block(
    c: Canvas, year: int, left: float, top: float, width: float, height: float
) -> None:
    header_height = 8 * mm
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(left + width / 2, top - header_height + 2, str(year))

    grid_top = top - header_height - 2 * mm
    grid_height = height - header_height - 2 * mm
    month_width = width / _MONTH_COLS
    month_height = grid_height / _MONTH_ROWS

    for month_idx in range(12):
        col = month_idx % _MONTH_COLS
        row = month_idx // _MONTH_COLS
        mx = left + col * month_width
        my = grid_top - row * month_height
        _draw_month(c, year, month_idx + 1, mx, my, month_width, month_height)


def _draw_month(
    c: Canvas,
    year: int,
    month: int,
    left: float,
    top: float,
    width: float,
    height: float,
) -> None:
    padding = 2 * mm
    inner_left = left + padding
    inner_width = width - 2 * padding

    name_y = top - 3.5 * mm
    c.setFont("Helvetica-Bold", 8)
    c.drawString(inner_left, name_y, _MONTH_ABBR[month])

    header_y = name_y - 3.5 * mm
    cell_width = inner_width / 7
    c.setFont("Helvetica", 5.5)
    for i, day_name in enumerate(_WEEKDAY_HEADERS):
        cx = inner_left + i * cell_width + cell_width / 2
        c.drawCentredString(cx, header_y, day_name)

    cal = calendar.Calendar(firstweekday=0)
    weeks = cal.monthdayscalendar(year, month)
    row_height = 3.2 * mm

    c.setFont("Helvetica", 7)
    for week_idx, week in enumerate(weeks):
        row_y = header_y - (week_idx + 1) * row_height
        for day_idx, day in enumerate(week):
            if day == 0:
                continue
            cx = inner_left + day_idx * cell_width + cell_width / 2
            c.drawCentredString(cx, row_y, str(day))
