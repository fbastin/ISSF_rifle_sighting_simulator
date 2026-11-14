# Scoring Model

## ISSF Decimal Scoring

In ISSF finals and electronic-target qualification, shots are scored
to one decimal place [issf].  A shot takes the highest zone that
its hole touches; each ring is divided into ten equal zones numbered
from `.0` to `.9`, so the value is truncated, not
rounded, and the maximum is 10.9.

## Target Faces

The simulator draws and scores the two rifle faces of the ISSF
General Technical Rules (2020, § 6.3.4.2–6.3.4.3):

<div class="table-scroll"><table>
<caption><strong>Table 4.</strong> Rifle target faces used by the simulator.</caption>
<tr><th style="text-align:left"><strong>Face</strong></th><th style="text-align:center"><strong>10 ring</strong></th><th style="text-align:center"><strong>Ring spacing</strong></th><th style="text-align:center"><strong>Black</strong></th><th style="text-align:center"><strong>Gauge</strong></th></tr>
<tr><td style="text-align:left"></td><td style="text-align:center">(diameter)</td><td style="text-align:center">(radius)</td><td style="text-align:center">(diameter)</td><td style="text-align:center"></td></tr>
<tr><td style="text-align:left">10 m air rifle</td><td style="text-align:center">0.5 mm</td><td style="text-align:center">2.5 mm</td><td style="text-align:center">30.5 mm (rings 4–9)</td><td style="text-align:center">4.5 mm</td></tr>
<tr><td style="text-align:left">50 m rifle</td><td style="text-align:center">10.4 mm</td><td style="text-align:center">8.0 mm</td><td style="text-align:center">112.4 mm (part of 3 to 10)</td><td style="text-align:center">5.6 mm</td></tr>
</table></div>

## Mathematical Model

A hole whose centre lies at the distance $r$ from the target centre
touches ring $v$ when $r \leq r_v + b$, where $r_v$ is the radius of
ring $v$ and $b$ the bullet radius.  On both rifle faces $r_{10} + b$
equals the ring spacing $s$ ($0.25 + 2.25 = 2.5$ mm at 10 m,
$5.2 + 2.8 = 8.0$ mm at 50 m), so the decimal score is

$$
S = \min\!\Bigl(10.9,\;\tfrac{1}{10}\bigl\lfloor 10\,(11 - r/s)\bigr\rfloor\Bigr),
  \qquad S = 0 \ \text{if}\ 11 - r/s < 1\,.
$$

Key values (10 m / 50 m):

- $r = 0$: $S = 10.9$.
- $r = s$ (2.5 / 8 mm): $S = 10.0$, the hole touching the 10 ring.
- $r = 2s$ (5 / 16 mm): $S = 9.0$.
- $r > 10s$ (25 / 80 mm): $S = 0$, the hole missing ring 1.

## Implementation

In `simulator.js`, `computeScore()` takes the impact in
millimetres from the target centre and applies the general rule—the
10 zone split over $r_{10} + b$, the others over $s$—which reduces to
*Scoring Model* on these two faces:

```javascript
function computeScore(x_mm, y_mm) {
  const T = TARGETS[targetType];
  const d = Math.hypot(x_mm, y_mm);
  const EPS = 1e-9;
  const R10 = T.ring10_r + T.bullet_r;
  if (d <= R10) return 10 + Math.min(9, Math.floor(10 * (R10 - d) / R10 + EPS)) / 10;
  const k = Math.ceil((d - R10) / T.spacing - EPS);    // rings beyond the 10
  const v = 10 - k;
  if (v < 1) return 0;
  const Rv = R10 + k * T.spacing;
  return v + Math.min(9, Math.floor(10 * (Rv - d) / T.spacing + EPS)) / 10;
}
```

The right panel draws the rings and the impact at the same scale,
`TARGETS[targetType].pxPerMm`: 6 px/mm at 10 m and
1.875 px/mm at 50 m, that is 15 px between rings on both faces.
