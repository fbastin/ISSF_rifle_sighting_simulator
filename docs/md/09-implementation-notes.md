# Implementation Notes

## Coordinate System

The HTML5 Canvas places the origin at the top-left corner with
$+x$ pointing right and $+y$ pointing *down*.  All rendering
and impact calculations use this convention.  When converting from
standard mathematical formulas (where $+y$ is up), vertical
quantities must be negated.  The key sign conventions in
`compute()` are summarized in *Implementation Notes*.


**Table.** Sign conventions for vertical quantities.

| **Quantity** | **Math frame** ($+y$ up) | **Canvas** ($+y$ down) |
| --- | --- | --- |
| Cant $\Delta y$ | $C(\cos\theta - 1) \leq 0$ | $C(1-\cos\theta) \geq 0$ |
| Wind $\Delta Y$ (tailwind) | $>0$ (up) | subtracted $\Rightarrow$ $-$ (up) |
| Parallax $p_y$ | opposite to $e_y$ | same formula (eye offset is in canvas coords) |


## Rendering Pipeline

Each animation frame (via `requestAnimationFrame`) executes:

1. `compute()` — evaluates parallax, mechanical offset, cant error, wind drift, and composes the final impact coordinates.
2. `drawLeft()` — renders the sight picture: target (with depth-of-field blur), front tunnel and iris (with cant rotation), rear diopter mask, barrel silhouette, and level indicator.
3. `drawRight()` — renders the target face with scoring rings, the parallax aim point (cyan), the impact point (red), and the wind indicator.
4. `drawPanel()` — renders the HUD with numerical parameters and the decimal score.


## Physical Constants and Defaults


**Table.** Physical constants and default parameters.

| **Constant** | **Description** | **Value** |
| --- | --- | --- |
| `PX_PER_MM` | Display scale | 6.0 px/mm |
| `rearZ` | Rear sight $z$ | 220 |
| `frontZ` | Front sight $z$ | 350 |
| `targetZ` | Target $z$ | 480 |
| `GRAVITY` | Gravitational accel. | 9.81 m/s$^2$ |
| `eyeZ` | Eye position $z$ (default) | 190 |
| `rearAperture_mm` | Rear diopter (default) | 1.6 mm |
| `frontIris_mm` | Front iris (default) | 3.8 mm |
| `sightHeight_mm` | Sight height (default) | 60 mm |
