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

The total vertical compensation $C = H + h_g$ is the foundation on
which canting error is built (*Rifle Cant*).  At 50 m, gravity
drop is an order of magnitude larger than at 10 m, explaining why
canting and wind errors become far more severe in smallbore
competition.  Understanding the relationship between sight height,
muzzle velocity, and gravity drop helps athletes interpret their
equipment choices [litz,pejsa].


## Physical Explanation and Illustration


> **Figure.** Sight height and gravity drop.  The bore is angled upward by
the combined compensation $C = H + h_g$ so that the parabolic bullet
path intersects the line of sight at the target distance.


## Mathematical Model

For a projectile with muzzle velocity $v$ fired at a target at
distance $d$, the time of flight is:

$$
% \label{eq:tof}
  t = \frac{d}{v}\,.
$$

The vertical drop due to gravity during this time is [mccoy]:

$$
% \label{eq:drop}
  h_g = \frac{1}{2}\,g\,t^2 = \frac{g\,d^2}{2\,v^2}\,.
$$

The total vertical compensation required at the target is:

$$
% \label{eq:totalcomp}
  C = H + h_g\,,
$$

where $H$ is the sight height.  Typical values used in the simulator:


**Table.** Time of flight and gravity drop for the two target modes.

| **Discipline** | $d$ (m) | $v$ (m/s) | $t$ (ms) | $h_g$ (mm) |
| --- | --- | --- | --- | --- |
| 10 m Air Rifle | 10 | 175 | 57.1 | 16.0 |
| 50 m Smallbore | 50 | 330 | 151.5 | 112.6 |


## Implementation

In `simulator.js`, lines 85–88 of `compute()`:

```javascript
const dist_m = targetType === "10m" ? 10 : 50;
const velocity_ms = targetType === "10m" ? 175.0 : 330.0;
const time_s = dist_m / velocity_ms;
const gravityDrop_mm = 0.5 * GRAVITY * (time_s * time_s) * 1000;
```

The factor of 1000 converts from metres to millimetres.  The total
compensation $C$ is formed on line 91:

```javascript
const totalComp_mm = sightHeight_mm + gravityDrop_mm;
```



## Simulator Exercises


1. In 10 m mode, note the gravity drop displayed in the HUD ($\approx$16 mm). Press **T** to switch to 50 m and observe the drop increase to $\approx$113 mm.
2. Use **W**/**S** to raise or lower the sight height. Observe in *Rifle Cant* how this changes the sensitivity to canting error.
