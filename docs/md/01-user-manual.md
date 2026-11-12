# User Manual

## Running the Simulator

Open `index.html` in any modern web browser. The page loads
`simulator.js`, which renders the simulation onto an HTML5
`<canvas>` element at 1000 × 600 pixels. No server or
build step is required.

## Interface Layout

The canvas is divided into three regions (*User Manual*).

<div style="text-align:center;margin:1.5rem 0"><img src="figures/fig_0.svg" alt="Schematic layout of the simulator interface." style="max-width:100%"><br><em><strong>Figure.</strong> Schematic layout of the simulator interface.</em></div>

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

<table>
<caption><strong>Table.</strong> Complete keyboard and mouse controls.</caption>
<tr><th><strong>Input</strong></th><th><strong>Action</strong></th><th><strong>Range</strong></th><th><strong>Section</strong></th></tr>
<tr><td>Mouse position</td><td>Eye offset (parallax)</td><td>canvas area</td><td><em>Parallax Error</em></td></tr>
<tr><td><strong>A</strong> / <strong>D</strong></td><td>Rear aperture $\pm 0.1$ mm</td><td>0.8–2.2 mm</td><td><em>Aperture Size and Eye Relief</em></td></tr>
<tr><td><strong>Q</strong> / <strong>E</strong></td><td>Front iris $\pm 0.1$ mm</td><td>2.4–7.0 mm</td><td><em>Aperture Size and Eye Relief</em></td></tr>
<tr><td><strong>C</strong> / <strong>V</strong></td><td>Iris ring thickness $\pm 0.1$ mm</td><td>0.5–5.0 mm</td><td><em>Aperture Size and Eye Relief</em></td></tr>
<tr><td><strong>U</strong> / <strong>J</strong></td><td>Eye relief $\pm 1$ mm</td><td>50–215 mm</td><td><em>Aperture Size and Eye Relief</em></td></tr>
<tr><td><strong>W</strong> / <strong>S</strong></td><td>Sight height $\pm 1$ mm</td><td>$\geq 20$ mm</td><td><em>Exterior Ballistics: Gravity and Trajectory</em></td></tr>
<tr><td><strong>Z</strong> / <strong>X</strong></td><td>Rifle cant $\pm 0.57^{\circ}$</td><td>unlimited</td><td><em>Rifle Cant</em></td></tr>
<tr><td>Arrow keys</td><td>Rear-sight clicks $\pm 1$</td><td>unlimited</td><td><em>Mechanical Sight Adjustment (Clicks)</em></td></tr>
<tr><td><strong>G</strong> / <strong>H</strong></td><td>Click value $\pm 0.01$ mm</td><td>0.01–0.10 mm</td><td><em>Mechanical Sight Adjustment (Clicks)</em></td></tr>
<tr><td><strong>O</strong> / <strong>P</strong></td><td>Wind speed $\pm 0.5$ m/s</td><td>0–10 m/s</td><td><em>Wind Drift</em></td></tr>
<tr><td><strong>K</strong> / <strong>L</strong></td><td>Wind direction $\pm 8.6^{\circ}$</td><td>full circle</td><td><em>Wind Drift</em></td></tr>
<tr><td><strong>T</strong></td><td>Toggle 10 m / 50 m target</td><td>—</td><td><em>Exterior Ballistics: Gravity and Trajectory</em></td></tr>
<tr><td><strong>R</strong></td><td>Reset all parameters to defaults</td><td>—</td><td>—</td></tr>
<tr><td><strong>F</strong></td><td>Toggle language (English / French)</td><td>—</td><td>—</td></tr>
</table>

## Quick-Start Walkthrough

1. Open `index.html`. The default view shows a 10 m air-rifle
        sight picture centered on the target.
2. Move the mouse across the left panel and observe both the sight picture
        shift and the cyan circle moving on the right panel.  This is
        *parallax* (*Parallax Error*).
3. Press **X** several times to cant the rifle clockwise.  Watch
        the spirit level and the red impact dot on the right panel shift
        right *and* down (*Rifle Cant*).
4. Use the arrow keys to bring the red dot back to center—these
        are sight “clicks” (*Mechanical Sight Adjustment (Clicks)*).
5. Press **T** to switch to the 50 m target and observe how
        gravity drop and cant error grow dramatically
        (*Exterior Ballistics: Gravity and Trajectory*).
6. Increase wind with **P** and rotate its direction with
        **K**/**L** to see wind drift (*Wind Drift*).