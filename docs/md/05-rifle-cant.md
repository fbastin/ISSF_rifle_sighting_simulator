# Rifle Cant

## The Issue for Competitive Shooters

*Canting* is the rotation of the rifle about the bore axis—a
tilt to the left or right as viewed from behind.  Because the barrel
must be angled *upward* to compensate for gravity
(*Exterior Ballistics: Gravity and Trajectory*), any tilt rotates this vertical compensation
vector out of the vertical plane.  The result is a point-of-impact
error that has *both* a lateral and a vertical component—the
“canting paradox” [rinker,mann].


## Why It Matters

Even small cant angles produce measurable errors, especially at
longer distances where the total compensation $C = H + h_g$ is
large.  At 50 m, a 2$^\circ$ cant shifts the impact laterally by
$\approx$ 6 mm—more than a full scoring ring.  Because the rifle
appears “almost level” to the shooter, canting errors are easy to
introduce and difficult to detect without a spirit level.  The impact
**always drops** and shifts **toward the direction of
the cant** [nra,rinker].


## Physical Explanation and Illustration


> **Figure.** The canting paradox.  When the rifle is tilted by $\theta$,
the compensation vector $C$ rotates, producing a lateral error
$\Delta x = C\sin\theta$ and a vertical loss
$\Delta y = C(1-\cos\theta)$.


## Mathematical Model

When the rifle is level, the bore-to-sight compensation vector is
purely vertical: $(0, C)$.  When the rifle is canted by angle
$\theta$, this vector rotates to $(C\sin\theta, C\cos\theta)$.
The errors on the target, relative to the uncanted aim point,
are [rinker,mann]:

$$
\begin{aligned}\Delta x &= C\,\sin\theta \,,          % \label{eq:cant-x}\\
  \Delta y &= C\,(1 - \cos\theta) \,,    % \label{eq:cant-y}\end{aligned}
$$

where $\Delta x$ is the lateral shift (positive in the direction of
the cant) and $\Delta y$ is the vertical drop (always
positive—impact always falls).

For small angles ($\theta \ll 1$), the approximations
$\sin\theta \approx \theta$ and $1 - \cos\theta \approx
\theta^2/2$ reveal that the lateral error is first-order in $\theta$
while the vertical drop is second-order.  This explains the
well-known observation that cant primarily causes horizontal
dispersion at small angles.


### Numerical Example

At 50 m ($C = 60 + 112.6 = 172.6$ mm), a cant of
$\theta = 2^\circ$ ($0.0349$ rad):

$$
\begin{aligned}\Delta x &= 172.6 \times \sin(0.0349) = 6.0\;\text{mm}\,,\\
  \Delta y &= 172.6 \times (1 - \cos(0.0349)) = 0.1\;\text{mm}\,.\end{aligned}
$$

The horizontal shift is 60$\times$ larger than the vertical drop,
consistent with competitive experience.


## Implementation

In `simulator.js`, lines 91–93 of `compute()`.  The cant
errors are computed in **canvas coordinates** where $+y$ points
downward, so a positive `shiftY_mm` moves the impact
downward on screen (i.e., the impact drops, as expected physically):

```javascript
const totalComp_mm = sightHeight_mm + gravityDrop_mm;
const shiftX_mm = totalComp_mm * Math.sin(cant);
const shiftY_mm = totalComp_mm * (1 - Math.cos(cant));
```


**Note on coordinate convention.**
In a standard mathematical frame ($+y$ up), the vertical error is
$C(\cos\theta - 1) \leq 0$ (negative means downward).  In the HTML5
Canvas frame ($+y$ down), the same physical drop corresponds to a
*positive* pixel offset.
*Rifle Cant* is expressed in the canvas convention used by the
implementation: $\Delta y = C(1-\cos\theta) \geq 0$.


## Simulator Exercises


1. In 10 m mode, press **X** several times to introduce a clockwise cant. Observe the red dot shift right and slightly down on the right panel, and the spirit-level indicator move in the left panel.
2. Press **T** to switch to 50 m and repeat. The same cant angle produces a much larger lateral shift because $C$ is larger.
3. Increase sight height with **W** and note how this amplifies the cant error (larger $C$ in *Rifle Cant*).
4. Use the arrow keys to zero-out the cant error with clicks (*Mechanical Sight Adjustment (Clicks)*), then remove the cant with **Z**. The impact now moves to the opposite side—demonstrating why zeroing under a cant and then removing it doubles the error.
