# Implementation Notes

## Coordinate System

The HTML5 Canvas places the origin at the top-left corner with
$+x$ pointing right and $+y$ pointing *down*.  All rendering
and impact calculations use this convention.  When converting from
standard mathematical formulas (where $+y$ is up), vertical
quantities must be negated.  The key sign conventions in
`compute()` are summarized in *Implementation Notes*.

<table>
<caption><strong>Table.</strong> Sign conventions for vertical quantities.</caption>
<tr><th><strong>Quantity</strong></th><th><strong>Math frame</strong> ($+y$ up)</th><th><strong>Canvas</strong> ($+y$ down)</th></tr>
<tr><td>Cant $Y$ (<em>eq:cant-Y</em>), no clicks</td><td>$h_g(\cos\theta - 1) \leq 0$</td><td>subtracted $\Rightarrow$ $+$ (down)</td></tr>
<tr><td>Wind $\Delta Y$ (tailwind)</td><td>$>0$ (up)</td><td>subtracted $\Rightarrow$ $-$ (up)</td></tr>
<tr><td>Parallax $p_y$</td><td>opposite to $e_y$</td><td>same formula (eye offset is in canvas coords)</td></tr>
</table>

## Rendering Pipeline

Each animation frame (via `requestAnimationFrame`) executes:

1. `compute()` — evaluates parallax, mechanical offset,
        cant error, wind drift, and composes the final impact
        coordinates.
2. `drawLeft()` — renders the sight picture: target
        (with depth-of-field blur), front tunnel and iris (with cant
        rotation), rear diopter mask, barrel silhouette, and level
        indicator.
3. `drawRight()` — renders the target face with scoring
        rings, the parallax aim point (cyan), the impact point (red),
        and the wind indicator.
4. `drawPanel()` — renders the HUD with numerical
        parameters and the decimal score.

## Physical Constants and Defaults

<table>
<caption><strong>Table.</strong> Physical constants and default parameters.</caption>
<tr><th><strong>Constant</strong></th><th><strong>Description</strong></th><th><strong>Value</strong></th></tr>
<tr><td><code>PX\_PER\_MM</code></td><td>Display scale</td><td>6.0 px/mm</td></tr>
<tr><td><code>rearZ</code></td><td>Rear sight $z$</td><td>220</td></tr>
<tr><td><code>frontZ</code></td><td>Front sight $z$</td><td>350</td></tr>
<tr><td><code>targetZ</code></td><td>Target $z$</td><td>480</td></tr>
<tr><td><code>GRAVITY</code></td><td>Gravitational accel.</td><td>9.81 m/s$^2$</td></tr>
<tr><td><code>eyeZ</code></td><td>Eye position $z$ (default)</td><td>190</td></tr>
<tr><td><code>rearAperture\_mm</code></td><td>Rear diopter (default)</td><td>1.6 mm</td></tr>
<tr><td><code>frontIris\_mm</code></td><td>Front iris (default)</td><td>3.8 mm</td></tr>
<tr><td><code>sightHeight\_mm</code></td><td>Sight height (default)</td><td>60 mm</td></tr>
</table>