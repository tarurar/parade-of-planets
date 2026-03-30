# Refined Minimal Orbit Logo — Mathematical Specification

## 1. Overview
This logo is constructed using a **quadratic Bézier curve** with a set of points (“planets”) placed exactly on the curve. The construction guarantees mathematical consistency and symmetry.

---

## 2. Bézier Curve Definition

A quadratic Bézier curve is defined as:

B(t) = (1 − t)² P₀ + 2(1 − t)t P₁ + t² P₂,   where t ∈ [0, 1]

### Control Points
- P₀ = (50, 120)
- P₁ = (300, 40)
- P₂ = (550, 120)

---

## 3. Parametric Form (Expanded)

### X component:
x(t) = (1 − t)² * 50 + 2(1 − t)t * 300 + t² * 550

Simplified:
x(t) = 50 + 500t

---

### Y component:
y(t) = (1 − t)² * 120 + 2(1 − t)t * 40 + t² * 120

Simplified:
y(t) = 120 − 160t + 160t²

---

## 4. Key Observations

- The X component is **linear** → uniform horizontal distribution
- The Y component is **quadratic** → creates the arc
- The curve is **symmetric around t = 0.5**
- Points at t and (1 − t) share the same Y value

---

## 5. Planet Placement

We choose parameter values:

t ∈ {0.1, 0.25, 0.4, 0.6, 0.75, 0.9}

These ensure:
- symmetry
- balanced visual spacing
- clean composition

---

## 6. Computed Coordinates

| t    | x(t) | y(t) |
|------|------|------|
| 0.10 | 100  | 105.6 |
| 0.25 | 175  | 90.0  |
| 0.40 | 250  | 81.6  |
| 0.60 | 350  | 81.6  |
| 0.75 | 425  | 90.0  |
| 0.90 | 500  | 105.6 |

---

## 7. Symmetry Properties

- x(t) + x(1 − t) = constant (600)
- y(t) = y(1 − t)
- Ensures perfect visual balance

---

## 8. Rendering Considerations

### Precision
- Avoid rounding during computation
- Use at least 1 decimal precision in SVG

### Stroke alignment
- SVG stroke may visually offset from mathematical curve
- Use:
  - `shape-rendering="geometricPrecision"`
  - consistent stroke width

---

## 9. Optional: Arc-Length Parameterization

Parametric t-spacing is **not visually uniform**.

To achieve equal spacing:
1. Compute arc length:
   L = ∫ |B'(t)| dt
2. Invert function numerically
3. Sample equal-length segments

This improves visual balance but increases complexity.

---

## 10. Reference Implementation (Pseudo-code)

```csharp
Point B(double t)
{
    var x = 50 + 500 * t;
    var y = 120 - 160 * t + 160 * t * t;
    return new Point(x, y);
}
```

## 11. Design intent

- Minimalism
- Mathematical precision
- Deterministic placement (no randomness)
- Clean, scientific aesthetic
