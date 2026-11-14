# Exterior Ballistics: Gravity and Trajectory

## The Issue for Competitive Shooters

The line of sight is perfectly straight, but a projectile follows a
parabolic arc under gravity [mccoy,rinker].  To make the
bullet hit the point of aim at a given distance, the barrel must be
angled slightly upward relative to the sight line.  The angular
offset depends on the *sight height* (the vertical distance
from bore center to the optical axis of the sights) and the
*gravity drop* at the target distance.

## Why It Matters

The bore starts $H$ below the line of sight and rises $H + h_g$ over
the distance, so its straight extension crosses the target plane
$h_g$ *above* the point of aim: gravity then brings the bullet
down onto it.  This offset $h_g$—not $H + h_g$—is what canting
turns sideways (*Rifle Cant*).  At 50 m, gravity drop is seven
times larger than at 10 m, which is why canting errors are far more
severe in smallbore competition.  Understanding the relationship between sight height,
muzzle velocity, and gravity drop helps athletes interpret their
equipment choices [litz,pejsa].

## Physical Explanation and Illustration

> **Figure 4.** Sight height and gravity drop.  The bore, $H$ below the line of sight, rises by $H + h_g$ over the distance: its straight extension crosses the target plane $h_g$ above the point of aim, and gravity brings the bullet down by $h_g$ onto it.

## Mathematical Model

For a projectile with muzzle velocity $v$ fired at a target at
distance $d$, the time of flight is:

$$
t = \frac{d}{v}\,.
$$

The vertical drop due to gravity during this time is [mccoy]:

$$
h_g = \frac{1}{2}\,g\,t^2 = \frac{g\,d^2}{2\,v^2}\,.
$$

Over the distance $d$ the bore must rise by

$$
H + h_g\,,
$$

where $H$ is the sight height: $H$ to reach the line of sight, $h_g$
to make up for the drop.  Typical values used in the simulator:

<div class="table-scroll"><table>
<caption><strong>Table 2.</strong> Time of flight and gravity drop for the two target modes.</caption>
<tr><th style="text-align:left"><strong>Discipline</strong></th><th style="text-align:center">$d$ (m)</th><th style="text-align:center">$v$ (m/s)</th><th style="text-align:center">$t$ (ms)</th><th style="text-align:center">$h_g$ (mm)</th></tr>
<tr><td style="text-align:left">10 m Air Rifle</td><td style="text-align:center">10</td><td style="text-align:center">175</td><td style="text-align:center">57.1</td><td style="text-align:center">16.0</td></tr>
<tr><td style="text-align:left">50 m Smallbore</td><td style="text-align:center">50</td><td style="text-align:center">330</td><td style="text-align:center">151.5</td><td style="text-align:center">112.6</td></tr>
</table></div>

## Implementation

In `simulator.js`, `compute()`:

```javascript
const dist_m = targetType === "10m" ? 10 : 50;
const velocity_ms = targetType === "10m" ? 175.0 : 330.0;
const time_s = dist_m / velocity_ms;
const gravityDrop_mm = 0.5 * GRAVITY * (time_s * time_s) * 1000;
```

The factor of 1000 converts from metres to millimetres.  The sight
height does not enter the computation of the impact: at the zeroing
distance it cancels (*Rifle Cant*), and `sightHeight_mm`
only sets the drawing of the barrel in the sight picture.

## Simulator Exercises

1. In 10 m mode, note the gravity drop displayed in the HUD
        (≈16 mm).  Press **T** to switch to 50 m and
        observe the drop increase to ≈113 mm.
2. Cant the rifle, then use **W**/**S** to raise or lower
        the sight height.  The impact does not move: at the zeroing
        distance the cant error does not depend on the sight height
        (*Rifle Cant*).
