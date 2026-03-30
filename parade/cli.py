"""Parade of Planets — command-line orbital phase calculator."""

import argparse
import json
import sys

from parade.ephemeris import render_ephemeris
from parade.observatory import (
    chart_constellation,
    interpret_phase,
    observe_phase,
    read_constellation_chart,
)
from parade.signature import is_weak_gravitational_constant

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


def main(argv: list[str] | None = None) -> None:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if not hasattr(args, "handler"):
        parser.print_help()
        sys.exit(1)

    if hasattr(args, "constant") and is_weak_gravitational_constant(args.constant):
        print(
            "⚠ Weak gravitational constant detected — orbital predictions may be unstable",
            file=sys.stderr,
        )

    args.handler(args)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="parade",
        description="Parade of Planets — orbital phase calculator. "
        "Computes celestial body phase alignments within "
        "planetary cycles for a given epoch.",
    )
    subparsers = parser.add_subparsers(title="commands")

    _add_observe_parser(subparsers)
    _add_interpret_parser(subparsers)
    _add_chart_parser(subparsers)
    _add_read_parser(subparsers)

    return parser


def _add_observe_parser(subparsers) -> None:
    p = subparsers.add_parser(
        "observe",
        help="Observe the orbital phase of a celestial body",
        description="Calculate which phase (day) a celestial body reaches during a given epoch and cycle.",
    )
    p.add_argument("--body", "-b", required=True, help="Celestial body to observe")
    p.add_argument("--epoch", "-y", type=int, required=True, help="Epoch (year)")
    p.add_argument("--cycle", "-c", type=int, required=True, help="Cycle (1–12)")
    p.add_argument("--constant", "-g", required=True, help="Gravitational constant")
    p.add_argument("--format", "-f", choices=["text", "json"], default="text")
    p.set_defaults(handler=_handle_observe)


def _add_interpret_parser(subparsers) -> None:
    p = subparsers.add_parser(
        "interpret",
        help="Interpret a phase observation",
        description="Determine which celestial body corresponds to an observed phase in a given epoch and cycle.",
    )
    p.add_argument("--phase", "-p", type=int, required=True, help="Phase (day)")
    p.add_argument("--epoch", "-y", type=int, required=True, help="Epoch (year)")
    p.add_argument("--cycle", "-c", type=int, required=True, help="Cycle (1–12)")
    p.add_argument("--constant", "-g", required=True, help="Gravitational constant")
    p.add_argument("--format", "-f", choices=["text", "json"], default="text")
    p.set_defaults(handler=_handle_interpret)


def _add_chart_parser(subparsers) -> None:
    p = subparsers.add_parser(
        "chart",
        help="Chart a constellation's orbital phases",
        description="Calculate phase alignments for each body in a constellation across the cycles of an epoch.",
    )
    p.add_argument(
        "--constellation",
        "-n",
        required=True,
        help="Constellation to chart (max 12 bodies)",
    )
    p.add_argument("--epoch", "-y", type=int, required=True, help="Epoch (year)")
    p.add_argument("--constant", "-g", required=True, help="Gravitational constant")
    p.add_argument("--format", "-f", choices=["text", "json"], default="text")
    p.add_argument(
        "--ephemeris",
        "-e",
        action="store_true",
        help="Display full visual ephemeris grids",
    )
    p.add_argument(
        "--no-color",
        dest="no_color",
        action="store_true",
        help="Disable ANSI color codes in ephemeris output",
    )
    p.set_defaults(handler=_handle_chart)


def _add_read_parser(subparsers) -> None:
    p = subparsers.add_parser(
        "read",
        help="Read a constellation chart",
        description="Interpret a sequence of phase observations to recover the original constellation.",
    )
    p.add_argument(
        "--phases",
        "-p",
        required=True,
        help="Comma-separated phase values",
    )
    p.add_argument("--epoch", "-y", type=int, required=True, help="Epoch (year)")
    p.add_argument("--constant", "-g", required=True, help="Gravitational constant")
    p.add_argument("--format", "-f", choices=["text", "json"], default="text")
    p.set_defaults(handler=_handle_read)


def _handle_observe(args) -> None:
    day = observe_phase(args.body, args.epoch, args.cycle, args.constant)
    if args.format == "json":
        print(json.dumps({"phase": day}))
    else:
        print(f"Phase: {day}")


def _handle_interpret(args) -> None:
    body = interpret_phase(args.phase, args.epoch, args.cycle, args.constant)
    display = "void" if body == " " else body
    if args.format == "json":
        print(json.dumps({"celestial_body": body}))
    else:
        print(f"Celestial body: {display}")


def _handle_chart(args) -> None:
    chart = chart_constellation(args.constellation, args.epoch, args.constant)
    if args.format == "json":
        print(json.dumps({"chart": [{"cycle": c, "phase": p} for c, p in chart]}))
    elif args.ephemeris:
        use_color = not args.no_color
        print(render_ephemeris(args.epoch, chart, use_color=use_color))
    else:
        print(f"Ephemeris for epoch {args.epoch}:")
        for cycle, phase in chart:
            month = _MONTH_NAMES[cycle]
            print(f"  Cycle {cycle:2d} ({month:>9s}):  phase {phase}")


def _handle_read(args) -> None:
    phases = [int(p.strip()) for p in args.phases.split(",")]
    word = read_constellation_chart(phases, args.epoch, args.constant)
    if args.format == "json":
        print(json.dumps({"constellation": word}))
    else:
        print(f"Constellation: {word}")
