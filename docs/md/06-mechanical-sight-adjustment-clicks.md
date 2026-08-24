# Mechanical Sight Adjustment (Clicks)

## The Issue for Competitive Shooters

After establishing a natural point of aim, the shooter brings the
group center onto the target center with the *rear* sight—the
diopter aperture in ISSF rifle shooting. These adjustments—commonly
called “clicks” because the mechanism produces an audible click per
increment—physically displace the aperture relative to the barrel,
changing the angle between the bore and the line of sight [nra].
Match diopters move a few hundredths of a millimetre per click: the
simulator default is $c = 0.04$ mm, and the value is adjustable with
**G**/**H** over $0.01$–$0.10$ mm.


## Why It Matters

Correct use of sight adjustments is essential for zeroing and for
responding to changing conditions (wind, light, temperature).
Understanding the *lever-arm geometry* helps the shooter predict
how many clicks are needed for a given correction. The rule of
direction follows from the geometry: a *rear*-sight click moves the
impact in the *same* direction as the click, while a *front*-sight
adjustment (insert height) moves it in the *opposite* direction.


## Physical Explanation and Illustration


> **Figure.** Mechanical sight adjustment geometry. A rear-aperture
click $c$ tilts the line of sight by $\theta = c/L$ ($L$: sight
radius). Re-centering the sight picture rotates the whole gun—and
the bore with it—by $\theta$, so the impact moves by
$\Delta = c\,R/L$ at the target distance $R$, in the *same*
direction as the click.


## Mathematical Model

When the aperture is displaced by $c$ and the shooter re-centers the
sight picture, the gun rotates by the small angle

$$
  \theta = \frac{c}{L},
  \qquad L = z_f - z_r \ \text{(sight radius)},
$$

and the bore follows. At a target distance $R$ the impact therefore
moves

$$
% \label{eq:clicks}
  \Delta_{\text{target}} = c \times \frac{R}{L}.
$$

With the simulator's default click value $c = 0.04$ mm and a match
sight radius $L = 800$ mm:

$$
  \Delta = 0.04 \times \frac{10\,000}{800} = 0.5 \text{ mm per click at 10 m},
  \qquad
  \Delta = 0.04 \times \frac{50\,000}{800} = 2.5 \text{ mm per click at 50 m}.
$$

Because the sight line is re-centered through the displaced
aperture, the impact moves in the *same* direction as a rear-sight
click. A *front*-sight displacement would tilt the line of sight the
other way: re-centering would rotate the gun *against* the
adjustment, and the impact would move *opposite* to it. (The exact
pivot of the re-centering rotation only contributes second-order
terms; see the wiki page “La visée au dioptre”, which develops the
same relation from Thales' theorem.)


## Implementation

In `simulator.js`, the click value (in hundredths of a millimetre)
and the per-click shift are:

```javascript
const SIGHT_RADIUS_mm = 800;               // diopter<->front sight
const clickShift_mm = (clickValue_cmm / 100) * (dist_m * 1000) / SIGHT_RADIUS_mm;
const tx =  clickCountX * clickShift_mm * PX_PER_MM;
const ty = -clickCountY * clickShift_mm * PX_PER_MM;  // canvas Y is down
```



## Simulator Exercises


1. Press the right arrow key several times. The red dot moves right on the target: a rear-sight click moves the impact in the *same* direction—$0.5$ mm per click at 10 m, $2.5$ mm at 50 m with the default value.
2. Press **G**/**H** to change the click value and watch the per-click shift scale proportionally: the lever-arm ratio $R/L$ is fixed by the rifle, the click value by the sight.
3. Combine clicks with cant (**Z**/**X**) to practice the real-world workflow of zeroing under imperfect conditions.
