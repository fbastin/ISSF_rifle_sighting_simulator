# Summary of Corrections Applied

During the preparation of this document, two corrections were
identified and applied to `simulator.js`:


1. **Cant vertical error sign (line 93).** The original code computed `shiftY_mm = -totalComp_mm * (1 - Math.cos(cant))`, yielding a negative value that moved the impact *upward* on the canvas. Physically, canting always lowers the impact (*Rifle Cant*). In Canvas coordinates ($+y$ down), the correct expression is `shiftY_mm = totalComp_mm * (1 - Math.cos(cant))`, which is non-negative and moves the impact downward.
2. **Scoring offset (line 113).** The original formula `10.9 - dist_mm / 2.5` evaluated to 9.9 at the 10-ring boundary (2.5 mm), whereas ISSF rules score this as 10.0. The corrected formula `Math.min(10.9, 11.0 - dist_mm / 2.5)` aligns the ring boundaries with integer scores and caps the maximum at 10.9.


The backup file `simulator.best.js` retains the original code
for reference.
