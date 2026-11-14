# User Manual

## Running the Simulator

Open `index.html` in any modern web browser. The page loads
`simulator.js`, which renders the simulation onto an HTML5
`<canvas>` element at 1000 × 600 pixels. No server or
build step is required.

## Interface Layout

The canvas is divided into three regions (Figure 1).

> **Figure 1.** Schematic layout of the simulator interface.

- **Left panel** (0–500 px): the shooter's view through
        the rear diopter, showing the front tunnel, iris, target, and
        a spirit-level indicator at the bottom.
- **Right panel** (500–1000 px): the target face with
        scoring rings. A cyan circle marks the
        parallax-shifted aim point; a red dot marks
        the predicted impact after all ballistic and mechanical
        corrections.  A wind-direction indicator is displayed in the
        upper-right corner.
- **HUD panel** (bottom 85 px): numerical readouts of
        all parameters, the decimal score, and a control-key reminder.

## Controls Reference

<div class="table-scroll"><table>
<caption><strong>Table 1.</strong> Complete keyboard and mouse controls.</caption>
<tr><th style="text-align:left"><strong>Input</strong></th><th style="text-align:left"><strong>Action</strong></th><th style="text-align:left"><strong>Range</strong></th><th style="text-align:left"><strong>Section</strong></th></tr>
<tr><td style="text-align:left">Mouse position</td><td style="text-align:left">Eye offset (parallax)</td><td style="text-align:left">canvas area</td><td style="text-align:left"><em>Parallax Error</em></td></tr>
<tr><td style="text-align:left"><strong>A</strong> / <strong>D</strong></td><td style="text-align:left">Rear aperture $\pm 0.1$ mm</td><td style="text-align:left">0.8–2.2 mm</td><td style="text-align:left"><em>Aperture Size and Eye Relief</em></td></tr>
<tr><td style="text-align:left"><strong>Q</strong> / <strong>E</strong></td><td style="text-align:left">Front iris $\pm 0.1$ mm</td><td style="text-align:left">2.4–7.0 mm</td><td style="text-align:left"><em>Aperture Size and Eye Relief</em></td></tr>
<tr><td style="text-align:left"><strong>C</strong> / <strong>V</strong></td><td style="text-align:left">Iris ring thickness $\pm 0.1$ mm</td><td style="text-align:left">0.5–5.0 mm</td><td style="text-align:left"><em>Aperture Size and Eye Relief</em></td></tr>
<tr><td style="text-align:left"><strong>U</strong> / <strong>J</strong></td><td style="text-align:left">Eye relief $\pm 1$ mm</td><td style="text-align:left">50–215 mm</td><td style="text-align:left"><em>Aperture Size and Eye Relief</em></td></tr>
<tr><td style="text-align:left"><strong>W</strong> / <strong>S</strong></td><td style="text-align:left">Sight height $\pm 1$ mm</td><td style="text-align:left">$\geq 20$ mm</td><td style="text-align:left"><em>Exterior Ballistics: Gravity and Trajectory</em></td></tr>
<tr><td style="text-align:left"><strong>Z</strong> / <strong>X</strong></td><td style="text-align:left">Rifle cant $\pm 0.57^{\circ}$</td><td style="text-align:left">unlimited</td><td style="text-align:left"><em>Rifle Cant</em></td></tr>
<tr><td style="text-align:left">Arrow keys</td><td style="text-align:left">Rear-sight clicks $\pm 1$</td><td style="text-align:left">unlimited</td><td style="text-align:left"><em>Mechanical Sight Adjustment (Clicks)</em></td></tr>
<tr><td style="text-align:left"><strong>G</strong> / <strong>H</strong></td><td style="text-align:left">Click value $\pm 0.01$ mm</td><td style="text-align:left">0.01–0.10 mm</td><td style="text-align:left"><em>Mechanical Sight Adjustment (Clicks)</em></td></tr>
<tr><td style="text-align:left"><strong>O</strong> / <strong>P</strong></td><td style="text-align:left">Wind speed $\pm 0.5$ m/s</td><td style="text-align:left">0–10 m/s</td><td style="text-align:left"><em>Wind Drift</em></td></tr>
<tr><td style="text-align:left"><strong>K</strong> / <strong>L</strong></td><td style="text-align:left">Wind direction $\pm 8.6^{\circ}$</td><td style="text-align:left">full circle</td><td style="text-align:left"><em>Wind Drift</em></td></tr>
<tr><td style="text-align:left"><strong>T</strong></td><td style="text-align:left">Toggle 10 m / 50 m target</td><td style="text-align:left">—</td><td style="text-align:left"><em>Exterior Ballistics: Gravity and Trajectory</em></td></tr>
<tr><td style="text-align:left"><strong>R</strong></td><td style="text-align:left">Reset all parameters to defaults</td><td style="text-align:left">—</td><td style="text-align:left">—</td></tr>
<tr><td style="text-align:left"><strong>F</strong></td><td style="text-align:left">Toggle language (English / French)</td><td style="text-align:left">—</td><td style="text-align:left">—</td></tr>
</table></div>

## Quick-Start Walkthrough

1. Open `index.html`. The default view shows a 10 m air-rifle
        sight picture centered on the target.
2. Move the mouse across the left panel and observe both the sight picture
        shift and the cyan circle moving on the right panel.  This is
        *parallax* (*Parallax Error*).
3. Press **X** several times to cant the rifle clockwise.  The
        bubble of the spirit level moves left, to the high side, and the
        red impact dot on the right panel shifts right *and* down
        (*Rifle Cant*).
4. Use the arrow keys to bring the red dot back to center—these
        are sight “clicks” (*Mechanical Sight Adjustment (Clicks)*).
5. Press **T** to switch to the 50 m target and observe how
        gravity drop and cant error grow dramatically
        (*Exterior Ballistics: Gravity and Trajectory*).
6. Increase wind with **P** and rotate its direction with
        **K**/**L** to see wind drift (*Wind Drift*).
