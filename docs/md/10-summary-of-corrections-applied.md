# Summary of Corrections Applied

The following corrections were identified and applied to
`simulator.js`:

1. **Cant vertical error sign (line 93).**
    The original code computed
    `shiftY_mm = -totalComp_mm * (1 - Math.cos(cant))`,
    yielding a negative value that moved the impact *upward*
    on the canvas.  Physically, canting always lowers the impact
    (*Rifle Cant*).  In Canvas coordinates ($+y$ down), the
    correct expression is
    `shiftY_mm = totalComp_mm * (1 - Math.cos(cant))`,
    which is non-negative and moves the impact downward.
2. **Scoring offset (line 113).**
    The original formula `10.9 - dist_mm / 2.5` evaluated to
    9.9 at the 10-ring boundary (2.5 mm), whereas ISSF rules score
    this as 10.0.  The corrected formula
    `Math.min(10.9, 11.0 - dist_mm / 2.5)` aligns the ring
    boundaries with integer scores and caps the maximum at 10.9.
3. **Cant error and sight height (2026-11-12).**
    The code and this document took the cant error as
    $(H + h_g)\sin\theta$, the sight height added to the drop.  At the
    zeroing distance the sight height cancels (*Rifle Cant*): the
    error is $h_g\sin\theta$.  The former value was 4.7 times too large
    at 10 m (2.7 mm instead of 0.56 mm for a 2$^\circ$ cant) and
    1.5 times too large at 50 m (6.0 mm instead of 3.9 mm).  The
    cant now also turns the click correction, which is fixed to the
    rifle.
4. **50 m target (2026-11-12).**
    The 50 m mode drew and scored the 10 m air-rifle face, 2.5 mm
    between rings, with a note giving about 4 mm for the 50 m face;
    it is 8 mm (Table 4).  Clicks, wind and cant at 50 m
    cost 3.2 times too many points.  Both faces now come from the
    `TARGETS` table.
5. **Display scale of the impact (2026-11-12).**
    The right panel drew the impact 1.2 times farther from the centre
    than the rings, so the red dot sat away from the ring its score gave
    (a 6.0 on the line of the 4).  Rings and impact now share one scale.
6. **Decimal truncation (2026-11-12).**
    The score was rounded to one decimal (9.96 shown as 10.0); ISSF
    zones run from `.0` to `.9`, so the value is now
    truncated (9.9), and a shot outside ring 1 scores 0.
7. **Spirit level (2026-11-12).**
    The bubble moved toward the low side of the cant.  A bubble rises
    to the high side: it now moves left for a clockwise cant.

The backup file `simulator.best.js` retains the original code
for reference.
