"""Parade of Planets — printable ephemeris chart generator."""

import argparse
import sys

from parade.print.renderer import render_ephemeris_pdf


def main(argv: list[str] | None = None) -> None:
    parser = _build_parser()
    args = parser.parse_args(argv)
    args.handler(args)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="parade-print",
        description="Generate printable ephemeris charts for sequential epochs.",
    )
    parser.add_argument(
        "--start",
        "-s",
        type=int,
        required=True,
        help="First epoch to chart",
    )
    parser.add_argument(
        "--years",
        "-n",
        type=int,
        required=True,
        help="Number of epochs",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        help="Output file path (default: parade_{start}_{years}y.pdf)",
    )
    parser.set_defaults(handler=_handle_print)
    return parser


def _handle_print(args: argparse.Namespace) -> None:
    if args.years < 1:
        print("Epoch count must be at least 1", file=sys.stderr)
        sys.exit(1)

    output = args.output or _default_filename(args.start, args.years)
    render_ephemeris_pdf(args.start, args.years, output)

    if args.output is None:
        print(output)


def _default_filename(start: int, years: int) -> str:
    return f"parade_{start}_{years}y.pdf"
