# Scoring Model

## ISSF Decimal Scoring

In ISSF finals and electronic-target qualification, shots are scored
to one decimal place.  The maximum score per shot is 10.9 (center),
and each integer ring boundary corresponds to a `.0` score.
For the 10 m air-rifle target, ring boundaries are spaced 2.5 mm
apart in radius [issf].


## Mathematical Model

The score is a linear function of radial distance $r$ (in mm) from
the target center, capped at the maximum:

$$
% \label{eq:score}
  S = \min\!\bigl(10.9,\;11.0 - \tfrac{r}{2.5}\bigr),
  \qquad S \geq 0\,.
$$


 Key values:

- $r = 0$ mm: $S = 10.9$ (perfect center shot).
- $r = 0.25$ mm (inner-10 / X-ring edge): $S = 10.9$.
- $r = 2.5$ mm (10-ring edge): $S = 10.0$.
- $r = 5.0$ mm (9-ring edge): $S = 9.0$.
- $r \geq 27.5$ mm: $S = 0$ (off target).


## Implementation

In `simulator.js`, lines 111–113:

```javascript
function computeScore(x, y) {
  const dist_mm = Math.hypot(x - cx, y - cy) / PX_PER_MM;
  return Math.max(0, Math.min(10.9, 11.0 - (dist_mm / 2.5)));
}
```

The computation uses the physics-space impact position (before the
$1.2\times$ display magnification applied on the right panel), so
the score reflects the true ballistic offset.

**Note.** The scoring ring spacing of 2.5 mm matches
the ISSF 10 m air-rifle target.  The 50 m smallbore target has
a different ring geometry (approximately 4 mm radial spacing), but
the simulator uses the same formula for both modes as a pedagogical
simplification.
