# Parallax Error

## The Issue for Competitive Shooters

In ISSF rifle shooting, the shooter views the target through a
small rear diopter aperture.  If the eye is not perfectly centered
behind this aperture, the line of sight through the front sight
projects onto a different point on the target than intended.  This
displacement is called *parallax error* [nra,mann].

Even sub-millimeter changes in cheek-weld position can shift the
apparent aim point by a scoring ring or more on the target.  Because
the shooter *perceives* the sights as correctly aligned, the
error is insidious: the sight picture looks acceptable, yet the
point of impact has moved.


## Why It Matters

At the 10 m air-rifle level, a 10.0 versus a 10.5 can determine a
final ranking.  Parallax is the single largest source of shot-to-shot
dispersion for a well-trained athlete whose hold and trigger control
are consistent [nra].  Understanding the geometry allows
coaches to diagnose inconsistent groups that are not explained by
natural hold wobble.


## Physical Explanation and Illustration


> **Figure.** Parallax geometry.  An eye offset $e_x$ projects through
the rear-sight center onto the target, producing an error $p_x$ in
the opposite direction, magnified by the distance ratio.


The line of sight originates at the eye position
$(e_x, z_e)$, passes through the center of the rear aperture
$(0, z_r)$, and intersects the target plane at $z_t$.  By the
intercept theorem (similar triangles), the target intersection is:

$$
% \label{eq:parallax}
  p_x = e_x \cdot \frac{z_r - z_t}{z_r - z_e}\,.
$$

Since $z_t > z_r > z_e$, the fraction is negative, so the parallax
offset on the target is in the *opposite* direction from the
eye displacement and magnified by the ratio of distances.


### Aperture Damping

A smaller rear aperture physically blocks off-axis light rays,
constraining the eye to a narrow cone and reducing the range of
parallax offsets that are optically possible [hecht,smith].
The simulator models this with a linear damping factor:

$$
% \label{eq:damping}
  f = \max\!\bigl(0.05,\;\tfrac{d_{\text{rear}}}{4.5}\bigr),
  \qquad p_x \leftarrow p_x \cdot f\,,
$$

where $d_{\text{rear}}$ is the rear aperture diameter in mm.  At the
minimum aperture of 0.8 mm, $f \approx 0.18$, reducing parallax
sensitivity by roughly 80 \%.


## Implementation

In `simulator.js`, the `compute()` function (lines 74–79):

```javascript
const scale = (targetZ - eyeZ) / (rearZ - eyeZ);
let px = eyeXoff + (0 - eyeXoff) * scale;
let py = eyeYoff + (0 - eyeYoff) * scale;

const f = Math.max(0.05, rearAperture_mm / 4.5);
px *= f;  py *= f;
```

Here `scale` is the ratio $\frac{z_t - z_e}{z_r - z_e}$, and
the expression `eyeXoff + (0 - eyeXoff) * scale` evaluates to
$e_x(1 - \text{scale}) = e_x \cdot \frac{z_r - z_t}{z_r - z_e}$,
which is *Parallax Error*.  The aperture damping factor $f$
(*Parallax Error*) is applied to both axes.


## Simulator Exercises


1. With the default 1.6 mm rear aperture, sweep the mouse across the canvas and note the cyan dot displacement on the right panel.
2. Reduce the aperture to 0.8 mm (**A**) and repeat. The cyan dot should move far less—this is the pinhole effect (*Parallax Error*).
3. Increase the aperture to 2.2 mm (**D**). Parallax sensitivity rises and the target image becomes blurred (see *Aperture Size and Eye Relief*).
