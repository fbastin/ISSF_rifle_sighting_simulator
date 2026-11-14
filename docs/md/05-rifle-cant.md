# Rifle Cant

## The Issue for Competitive Shooters

*Canting* is a tilt of the rifle to the left or right as viewed
from behind.  The shooter keeps the sights on the aiming mark while
doing so, so the rifle turns about the *line of sight*.  Because
the barrel is angled *upward* to compensate for gravity
(*Exterior Ballistics: Gravity and Trajectory*), the straight extension of the bore crosses
the target plane $h_g$ above the point of aim; any tilt turns this
offset out of the vertical plane, while gravity keeps pulling the
bullet straight down.  The result is a point-of-impact error that has
*both* a lateral and a vertical component—the “canting
paradox” [rinker].

## Why It Matters

Even small cant angles produce measurable errors, especially at
longer distances where the drop $h_g$ is large.  At 50 m, a
2$^\circ$ cant shifts the impact laterally by ≈ 3.9 mm,
about half the distance between two rings of the 50 m target
(8 mm); at 10 m the same cant costs 0.56 mm, about a fifth of the
2.5 mm between rings of the air-rifle target.  Because the rifle
appears “almost level” to the shooter, canting errors are easy to
introduce and difficult to detect without a spirit level.  The impact
**always drops** and shifts **toward the direction of
the cant** [nra,rinker].

## Physical Explanation and Illustration

> **Figure 5.** The canting paradox, seen from behind along the line of sight.  The straight extension of the bore crosses the target plane $h_g$ above the point of aim; tilting the rifle by $\theta$ about the line of sight turns this offset, while gravity still lowers the bullet by $h_g$ straight down: lateral error $\Delta x = h_g\sin\theta$, vertical loss $\Delta y = h_g(1-\cos\theta)$.

## Mathematical Model

Work in the rifle's own frame, on the target plane, with the point of
aim at the origin.  The bore starts $H$ below the line of sight and
rises $H + h_g$ over the distance (Figure 4), so its
straight extension crosses the target plane at

$$
\mathbf{c} = (c_x,\;c_y) = (k_x,\;h_g + k_y)\,,
$$

where $(k_x, k_y)$ is the correction set with the rear-sight clicks
(*Mechanical Sight Adjustment (Clicks)*).  The sight height has cancelled:
$-H + (H + h_g) = h_g$.  Canting turns everything fixed to the
rifle—the offset $\mathbf{c}$ included—by $\theta$ about the line
of sight; gravity, fixed in space, then lowers the bullet by $h_g$.
The impact relative to the point of aim ($+y$ up, $\theta > 0$
clockwise as seen by the shooter) is

$$
\begin{aligned}X &= c_x\cos\theta + c_y\sin\theta\,,\\
  Y &= -c_x\sin\theta + c_y\cos\theta - h_g\,.\end{aligned}
$$

With the clicks at zero, $\mathbf{c} = (0,\,h_g)$ and the errors
reduce to

$$
\begin{aligned}\Delta x &= h_g\,\sin\theta \,,          \\
  \Delta y &= h_g\,(1 - \cos\theta) \,,\end{aligned}
$$

where $\Delta x$ is the lateral shift (positive in the direction of
the cant) and $\Delta y$ is the vertical loss (always
positive—impact always falls).

For small angles ($\theta \ll 1$), the approximations
$\sin\theta \approx \theta$ and $1 - \cos\theta \approx
\theta^2/2$ reveal that the lateral error is first-order in $\theta$
while the vertical drop is second-order.  This explains the
well-known observation that cant primarily causes horizontal
dispersion at small angles.

### Sight Height

The sight height $H$ does not appear in *Rifle Cant*.
Canting does turn the bore's upward angle $(H + h_g)/d$ sideways,
which alone would move the bullet by $(H + h_g)\sin\theta$ at the
target; but the same rotation about the line of sight moves the
muzzle, which sits $H$ below that line, sideways by $H\sin\theta$ the
other way, and the two terms in $H$ cancel.  The rule of thumb used at
long range—multiply the total elevation, zero included, by
$\sin\theta$ ([litz], pp. 146–147)—ignores the muzzle's move and
overstates the error by $H\sin\theta$.  At several hundred metres,
where the drop is counted in metres, this is negligible; at 10 m,
where $H = 60$ mm is close to four times $h_g = 16.0$ mm, it would
make the error 4.7 times too large.

The cancellation is exact at the zeroing distance, the only distance
the simulator models.  At another distance $r$, the straight bore line
crosses the target plane $h_g(d)\,r/d - H\,(1 - r/d)$ above the point
of aim, and $H$ reappears.

### Numerical Example

At 50 m ($h_g = 112.6$ mm), a cant of
$\theta = 2^\circ$ ($0.0349$ rad):

$$
\begin{aligned}\Delta x &= 112.6 \times \sin(0.0349) = 3.9\;\text{mm}\,,\\
  \Delta y &= 112.6 \times (1 - \cos(0.0349)) = 0.07\;\text{mm}\,.\end{aligned}
$$

At 10 m ($h_g = 16.0$ mm), the same cant gives $\Delta x = 0.56$ mm
and $\Delta y = 0.01$ mm.  The horizontal shift is 57× larger
than the vertical drop, consistent with competitive experience.

## Implementation

In `simulator.js`, `compute()` evaluates
*Rifle Cant* in millimetres, $+y$ up:

```javascript
const gunX_mm = clickCountX * clickShift_mm;
const gunY_mm = clickCountY * clickShift_mm + gravityDrop_mm;
const cosCant = Math.cos(cant), sinCant = Math.sin(cant);
const rifleX_mm =  gunX_mm * cosCant + gunY_mm * sinCant;
const rifleY_mm = -gunX_mm * sinCant + gunY_mm * cosCant - gravityDrop_mm;
```

A positive `cant` is the clockwise rotation that
`ctx.rotate(cant)` draws in the sight picture.  The vertical
impact is converted to canvas coordinates ($+y$ down) only when the
final impact is composed, by subtraction.

## Simulator Exercises

1. In 10 m mode, press **X** several times to introduce a
        clockwise cant.  Observe the red dot shift right and slightly
        down on the right panel, and the bubble of the spirit level move
        left, to the high side, in the left panel.
2. Press **T** to switch to 50 m and repeat.  The same cant
        angle produces a lateral shift seven times larger, because
        $h_g$ is seven times larger.
3. With the rifle canted, change the sight height with
        **W**/**S**: the impact does not move.
4. Use the arrow keys to bring the impact back to the centre with
        clicks (*Mechanical Sight Adjustment (Clicks)*), then remove the cant with **Z**.
        The impact now moves to the opposite side: a correction set
        under a cant holds only at that same cant.
