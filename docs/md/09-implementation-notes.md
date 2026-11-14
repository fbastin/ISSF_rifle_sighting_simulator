# Implementation Notes

## Coordinate System

The HTML5 Canvas places the origin at the top-left corner with
$+x$ pointing right and $+y$ pointing *down*.  All rendering
and impact calculations use this convention.  When converting from
standard mathematical formulas (where $+y$ is up), vertical
quantities must be negated.  The key sign conventions in
`compute()` are summarized in Table 5.

<div class="table-scroll"><table>
<caption><strong>Table 5.</strong> Sign conventions for vertical quantities.</caption>
<tr><th style="text-align:left"><strong>Quantity</strong></th><th style="text-align:center"><strong>Math frame</strong> ($+y$ up)</th><th style="text-align:center"><strong>Canvas</strong> ($+y$ down)</th></tr>
<tr><td style="text-align:left">Cant $Y$ (<em>Rifle Cant</em>), no clicks</td><td style="text-align:center">$h_g(\cos\theta - 1) \leq 0$</td><td style="text-align:center">subtracted $\Rightarrow$ $+$ (down)</td></tr>
<tr><td style="text-align:left">Wind $\Delta Y$ (tailwind)</td><td style="text-align:center">$>0$ (up)</td><td style="text-align:center">subtracted $\Rightarrow$ $-$ (up)</td></tr>
<tr><td style="text-align:left">Parallax $p_y$</td><td style="text-align:center">opposite to $e_y$</td><td style="text-align:center">computed in canvas pixels, negated into mm</td></tr>
</table></div>

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

<div class="table-scroll"><table>
<caption><strong>Table 6.</strong> Physical constants and default parameters.</caption>
<tr><th style="text-align:left"><strong>Constant</strong></th><th style="text-align:left"><strong>Description</strong></th><th style="text-align:right"><strong>Value</strong></th></tr>
<tr><td style="text-align:left"><code>PX_PER_MM</code></td><td style="text-align:left">Sight-picture scale (left panel)</td><td style="text-align:right">6.0 px/mm</td></tr>
<tr><td style="text-align:left"><code>TARGETS[...].pxPerMm</code></td><td style="text-align:left">Target-face scale (right panel)</td><td style="text-align:right">6.0 / 1.875 px/mm</td></tr>
<tr><td style="text-align:left"><code>rearZ</code></td><td style="text-align:left">Rear sight $z$</td><td style="text-align:right">220</td></tr>
<tr><td style="text-align:left"><code>frontZ</code></td><td style="text-align:left">Front sight $z$</td><td style="text-align:right">350</td></tr>
<tr><td style="text-align:left"><code>targetZ</code></td><td style="text-align:left">Target $z$</td><td style="text-align:right">480</td></tr>
<tr><td style="text-align:left"><code>GRAVITY</code></td><td style="text-align:left">Gravitational accel.</td><td style="text-align:right">9.81 m/s$^2$</td></tr>
<tr><td style="text-align:left"><code>eyeZ</code></td><td style="text-align:left">Eye position $z$ (default)</td><td style="text-align:right">190</td></tr>
<tr><td style="text-align:left"><code>rearAperture_mm</code></td><td style="text-align:left">Rear diopter (default)</td><td style="text-align:right">1.6 mm</td></tr>
<tr><td style="text-align:left"><code>frontIris_mm</code></td><td style="text-align:left">Front iris (default)</td><td style="text-align:right">3.8 mm</td></tr>
<tr><td style="text-align:left"><code>sightHeight_mm</code></td><td style="text-align:left">Sight height (default)</td><td style="text-align:right">60 mm</td></tr>
</table></div>
