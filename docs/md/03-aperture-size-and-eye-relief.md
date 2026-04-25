# Aperture Size and Eye Relief

## The Issue for Competitive Shooters

The rear diopter and front iris form the optical frame of the sight
picture.  Their diameters and the distance from the eye to the rear
sight (*eye relief*) determine three competing properties:

1. **Depth of field:** smaller apertures yield sharper images of both the front sight and the target, analogous to a pinhole camera [hecht].
2. **Light transmission:** too small an aperture reduces brightness and may cause diffraction artifacts, leading to eye fatigue.
3. **Parallax sensitivity:** as derived in *Parallax Error*, smaller apertures reduce the magnitude of parallax error.


## Why It Matters

Choosing the correct aperture is a balance: too wide and the front
sight ring blurs, degrading centering precision; too narrow and the
image darkens, especially in indoor ranges with poor lighting.  Eye
relief must also be consistent—changes in head position alter the
apparent size of the rear aperture in the sight picture, which
disrupts the concentricity judgment [nra].


## Physical Explanation and Illustration


> **Figure.** Pinhole analogy.  A smaller rear aperture restricts the cone
of accepted light rays, increasing depth of field and reducing
parallax sensitivity.


### Apparent Aperture Size and Eye Relief

The visual angle subtended by the rear diopter from the eye depends
inversely on the relief distance $R = z_r - z_e$:

$$
% \label{eq:apparent-size}
  r_{\text{apparent}} \;\propto\; \frac{d_{\text{rear}}}{R}\,.
$$

Larger relief makes the aperture appear smaller, narrowing the
visible field, while smaller relief opens the view.  The simulator
implements this in the rendering code as:

$$
% \label{eq:rearR}
  r_{\text{px}} = (d_{\text{rear}} \times 10) \times \frac{250}{R}\,.
$$



### Target Blur

When the rear aperture is large, the depth of field shrinks and the
target image appears blurred.  The simulator applies a Gaussian blur
proportional to the aperture size:

$$
% \label{eq:blur}
  \sigma_{\text{blur}} = \max\!\bigl(0,\;(d_{\text{rear}} - 0.9) \times 4\bigr)\;\text{px}.
$$



## Implementation

In `simulator.js`, the rendering function `drawLeft()`
(lines 171–173 and 120–121):

```javascript
const relief = Math.max(5, rearZ - eyeZ);
const rearR = (rearAperture_mm * 10) * (250 / relief);
const targetBlur = Math.max(0, (rearAperture_mm - 0.9) * 4);
```


The front iris and ring thickness are rendered as concentric arcs
whose radii are proportional to `frontIris_mm` and
`frontThickness_mm`, providing a visual representation of the
three-ring sight picture (rear diopter, front tunnel, front iris).


## Simulator Exercises


1. Start with the default aperture (1.6 mm). Press **D** to widen the rear aperture to 2.2 mm: note the target blur increase and the parallax sensitivity rise.
2. Press **A** to narrow to 0.8 mm: the image sharpens and darkens, and parallax sensitivity drops.
3. Use **U**/**J** to change eye relief. Watch how the visible diameter of the sight picture changes (*Aperture Size and Eye Relief*). A relief that is too short causes the rear aperture to fill the view; too long and the front tunnel cannot be framed concentrically.
4. Adjust front iris (**Q**/**E**) and thickness (**C**/**V**) to explore how the inner ring frames the target bull.
