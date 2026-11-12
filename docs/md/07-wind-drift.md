# Wind Drift

## The Issue for Competitive Shooters

Once the projectile leaves the barrel, it is subject to aerodynamic
forces.  A crosswind exerts a lateral force that deflects the bullet
from its intended path[mccoy,litz].  In outdoor ISSF
disciplines (50 m rifle, 300 m rifle), wind reading is the
dominant skill separating competitors of similar technical
ability[litz].

## Why It Matters

Wind is invisible, variable, and non-uniform along the bullet's
path.  Shooters must estimate its speed and direction from range flags
or mirage, then decide whether to adjust sights (clicks) or hold off
the center.  A 3 m/s crosswind at 50 m produces ≈ 31 mm
of lateral drift—several scoring rings.

## Physical Explanation and Illustration

<div style="text-align:center;margin:1.5rem 0"><img src="figures/fig_6.svg" alt="Wind deflection (top-down view).  A crosswind with velocity
component $W\sin\alpha$ pushes the bullet laterally over the full
time of flight." style="max-width:100%"><br><em><strong>Figure.</strong> Wind deflection (top-down view).  A crosswind with velocity
component $W\sin\alpha$ pushes the bullet laterally over the full
time of flight.</em></div>

## Mathematical Model

The full aerodynamic treatment of wind deflection involves the drag
coefficient, projectile mass, and cross-sectional area integrated
over the flight path[mccoy].  For pedagogical purposes, the
simulator uses a linearized empirical model:

$$
\begin{aligned}\Delta X_{\text{wind}} &= W \cdot K_w \cdot \sin\alpha  ,
    \\
  \Delta Y_{\text{wind}} &= W \cdot K_{w,y} \cdot \cos\alpha  ,\end{aligned}
$$

where $W$ is the wind speed (m/s), $\alpha$ is the wind direction
angle (0$^\circ$ = tailwind, 90$^\circ$ = full crosswind from the
left), $K_w$ is a lateral drift coefficient (mm per m/s of
crosswind), and $K_{w,y} = 0.2 K_w$ is a much smaller longitudinal
coefficient representing the effect of head/tailwinds on time of
flight and hence gravity drop.

<table>
<caption><strong>Table.</strong> Wind drift coefficients used in the simulator.</caption>
<tr><th><strong>Discipline</strong></th><th>$K_w$ (mm per m/s)</th><th>$K_{w,y}$ (mm per m/s)</th></tr>
<tr><td>10 m Air Rifle</td><td>1.2</td><td>0.24</td></tr>
<tr><td>50 m Smallbore</td><td>10.5</td><td>2.1</td></tr>
</table>

### Wind Direction Convention

The wind angle $\alpha$ is measured from the shooter–target axis,
with 0$^\circ$ representing a tailwind (wind blowing from behind the
shooter toward the target) and 90$^\circ$ a crosswind blowing from
left to right.  The wind indicator on the right panel shows an arrow
pointing in the direction of wind flow.

A tailwind ($\alpha = 0^\circ$) slightly increases the effective
velocity, reducing time of flight and gravity drop, thus raising the
impact.  A headwind ($\alpha = 180^\circ$) has the opposite
effect[litz].

## Implementation

In `simulator.js`, `compute()`:

“`javascript
const windFactor = targetType === "10m" ? 1.2 : 10.5;
const windDriftX_mm = windSpeed_ms * windFactor
                      * Math.sin(windDir_rad);
const windDriftY_mm = windSpeed_ms * (windFactor * 0.2)
                      * Math.cos(windDir_rad);
“`

The wind drift is added to the parallax and to the cant result
(*Rifle Cant*), all in millimetres in mathematical coordinates
($+y$ up); the sum is *subtracted* from the canvas ordinate of the
sight picture, which grows downward:

“`javascript
const impactX_mm = parallaxX_mm + rifleX_mm + windDriftX_mm;
const impactY_mm = parallaxY_mm + rifleY_mm + windDriftY_mm;
finalY: cy - impactY_mm * PX_PER_MM
“`

## Simulator Exercises

1. Set a 3 m/s crosswind: press **P** six times from the
        default.  The red dot drifts laterally on the target.
2. Rotate the wind with **K**/**L** and observe how the
        drift direction follows the wind arrow on the upper-right
        indicator.
3. Compare drift at 10 m and 50 m (**T** to toggle):
        the 50 m drift coefficient is nearly $9\times$ larger.
4. Set a pure headwind ($\alpha = 180^\circ$, rotate until
        the arrow points downward on the clock face) and observe the
        subtle vertical impact shift.