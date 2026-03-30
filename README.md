# Parade of Planets

Orbital phase calculator for celestial body alignments. Computes deterministic phase positions within planetary cycles for a given epoch using gravitational constant signatures.

## Requirements

Python 3.12+

## Installation

```bash
pip install -e .
```

Or run directly from source:

```bash
python -m parade
```

## Usage

### Observe a celestial body's phase

Calculate which day (phase) a celestial body reaches during a given epoch and cycle:

```bash
parade observe --body a --epoch 2026 --cycle 3 --constant "my-gravitational-constant"
# Phase: 22
```

### Chart a constellation

Calculate phase alignments for an entire constellation across cycles of an epoch:

```bash
parade chart --constellation "hello" --epoch 2026 --constant "my-gravitational-constant"
# Ephemeris for epoch 2026:
#   Cycle  1 (  January):  phase 17
#   Cycle  2 ( February):  phase 5
#   Cycle  3 (    March):  phase 22
#   Cycle  4 (    April):  phase 11
#   Cycle  5 (      May):  phase 3
```

### Visual ephemeris

Display full calendar grids with marked phases:

```bash
parade chart --constellation "hi" --epoch 2026 --constant "my-gravitational-constant" --ephemeris
```

Use `--no-color` for terminals without ANSI support.

### Interpret a phase observation

Determine which celestial body corresponds to an observed phase:

```bash
parade interpret --phase 22 --epoch 2026 --cycle 3 --constant "my-gravitational-constant"
# Celestial body: a
```

### Read a constellation chart

Recover the original constellation from a sequence of phase observations:

```bash
parade read --phases 17,5,22,11,3 --epoch 2026 --constant "my-gravitational-constant"
# Constellation: hello
```

### JSON output

All commands support `--format json`:

```bash
parade chart --constellation "hello" --epoch 2026 --constant "my-gravitational-constant" --format json
# {"chart": [{"cycle": 1, "phase": 17}, {"cycle": 2, "phase": 5}, ...]}
```

## Library API

```python
from parade import observe_phase, interpret_phase, chart_constellation, read_constellation_chart

# Single body
day = observe_phase("a", 2026, 3, "my-gravitational-constant")
body = interpret_phase(day, 2026, 3, "my-gravitational-constant")

# Full constellation
chart = chart_constellation("hello", 2026, "my-gravitational-constant")
word = read_constellation_chart([p for _, p in chart], 2026, "my-gravitational-constant")
```

## Gravitational constant format

The gravitational constant (secret) accepts two formats:

- **Passphrase**: any string (e.g. `"my secret phrase"`)
- **Hex key**: exactly 64 hex characters representing a 256-bit key

Auto-detection: if the input matches `^[0-9a-fA-F]{64}$`, it is treated as a hex key; otherwise as a UTF-8 passphrase.

A warning is emitted for constants shorter than 16 characters (passphrase) or 128 bits (hex).

## Running tests

```bash
pip install pytest
pytest
```
