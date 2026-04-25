# Wind Drift

## The Issue for Competitive Shooters

Once the projectile leaves the barrel, it is subject to aerodynamic
forces.  A crosswind exerts a lateral force that deflects the bullet
from its intended path [mccoy,litz].  In outdoor ISSF
disciplines (50 m rifle, 300 m rifle), wind reading is the
dominant skill separating competitors of similar technical
ability [litz].


## Why It Matters

Wind is invisible, variable, and non-uniform along the bullet's
path.  Shooters must estimate its speed and direction from range flags
or mirage, then decide whether to adjust sights (clicks) or hold off
the center.  A 3 m/s crosswind at 50 m produces $\approx$ 31 mm
of lateral drift—several scoring rings.


## Physical Explanation and Illustration


> **Figure.** Wind deflection (top-down view).  A crosswind with velocity
component $W\sin\alpha$ pushes the bullet laterally over the full
time of flight.


## Mathematical Model

The full aerodynamic treatment of wind deflection involves the drag
coefficient, projectile mass, and cross-sectional area integrated
over the flight path [mccoy].  For pedagogical purposes, the
simulator uses a linearized empirical model:

$$
\begin{aligned}\Delta X_{\text{wind}} &= W \cdot K_w \cdot \sin\alpha \,,
    % \label{eq:wind-x}\\
  \Delta Y_{\text{wind}} &= W \cdot K_{w,y} \cdot \cos\alpha \,,
    % \label{eq:wind-y}\end{aligned}
$$

where $W$ is the wind speed (m/s), $\alpha$ is the wind direction
angle (0$^\circ$ = tailwind, 90$^\circ$ = full crosswind from the
left), $K_w$ is a lateral drift coefficient (mm per m/s of
crosswind), and $K_{w,y} = 0.2 K_w$ is a much smaller longitudinal
coefficient representing the effect of head/tailwinds on time of
flight and hence gravity drop.


**Table.** Wind drift coefficients used in the simulator.

| **Discipline** | $K_w$ (mm per m/s) | $K_{w,y}$ (mm per m/s) |
| --- | --- | --- |
| 10 m Air Rifle | 1.2 | 0.24 |
| 50 m Smallbore | 10.5 | 2.1 |


### Wind Direction Convention

The wind angle $\alpha$ is measured from the shooter–target axis,
with 0$^\circ$ representing a tailwind (wind blowing from behind the
shooter toward the target) and 90$^\circ$ a crosswind blowing from
left to right.  The wind indicator on the right panel shows an arrow
pointing in the direction of wind flow.

A tailwind ($\alpha = 0^\circ$) slightly increases the effective
velocity, reducing time of flight and gravity drop, thus raising the
impact.  A headwind ($\alpha = 180^\circ$) has the opposite
effect [litz].


## Implementation

In `simulator.js`, lines 97–100:

```javascript
const windFactor = targetType === "10m" ? 1.2 : 10.5;
const windDriftX_mm = windSpeed_ms * windFactor
                      * Math.sin(windDir_rad);
const windDriftY_mm = windSpeed_ms * (windFactor * 0.2)
                      * Math.cos(windDir_rad);
```

In the final impact computation (line 107), `windDriftY_mm` is
*subtracted* because it is computed in mathematical coordinates
($+y$ up) while the Canvas uses $+y$ down:

```javascript
finalY: cy + py + ty
      + (shiftY_mm * PX_PER_MM)
      - (windDriftY_mm * PX_PER_MM)
```



## Simulator Exercises


1. Set a 3 m/s crosswind: press **P** six times from the default. The red dot drifts laterally on the target.
2. Rotate the wind with **K**/**L** and observe how the drift direction follows the wind arrow on the upper-right indicator.
3. Compare drift at 10 m and 50 m (**T** to toggle): the 50 m drift coefficient is nearly $9\times$ larger.
4. Set a pure headwind ($\alpha = 180^\circ$, rotate until the arrow points downward on the clock face) and observe the subtle vertical impact shift.
