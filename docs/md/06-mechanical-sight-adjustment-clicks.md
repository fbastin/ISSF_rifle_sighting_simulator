# Mechanical Sight Adjustment (Clicks)

## The Issue for Competitive Shooters

After establishing a natural point of aim, the shooter adjusts the
front sight to bring the group center onto the target center.
These adjustments—commonly called “clicks” because many
mechanisms produce an audible click per increment—physically
displace the front-sight element relative to the barrel, changing
the angle between the bore and the line of sight [nra].


## Why It Matters

Correct use of sight adjustments is essential for zeroing and for
responding to changing conditions (wind, light, temperature).
Understanding the *lever-arm geometry* helps the shooter
predict how many clicks are needed for a given correction and why
front-sight adjustments move the group in the *same* direction
as the adjustment.


## Physical Explanation and Illustration


> **Figure.** Mechanical sight adjustment geometry.  A front-sight
displacement $\delta$ is amplified by the lever-arm ratio $M$ at
the target.


## Mathematical Model

The line of sight pivots about the rear sight.  When the front sight
is displaced by $\delta$ (in pixels or mm), the intercept theorem
gives the impact shift at the target as:

$$
% \label{eq:clicks}
  \Delta_{\text{target}} = \delta \cdot M,
  \qquad M = \frac{z_t - z_r}{z_f - z_r}\,.
$$

With the default values $z_r = 220$, $z_f = 350$, $z_t = 480$:

$$
M = \frac{480 - 220}{350 - 220} = \frac{260}{130} = 2.0\,.
$$

A one-pixel front-sight click produces a two-pixel impact shift at
the target.  Because the line of sight passes *through* the
displaced front sight, the impact moves in the *same*
direction as the front-sight adjustment.


## Implementation

In `simulator.js`, lines 81–83:

```javascript
const mechanicalScale = (targetZ - rearZ) / (frontZ - rearZ);
const tx = frontXoff * mechanicalScale;
const ty = frontYoff * mechanicalScale;
```



## Simulator Exercises


1. Press the right arrow key several times. The red dot moves right on the target—the front sight has been displaced rightward, tilting the line of sight rightward.
2. Combine clicks with cant (**Z**/**X**) to practice the real-world workflow of zeroing under imperfect conditions.
