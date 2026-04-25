# User Manual

## Running the Simulator

Open `sight.html` in any modern web browser. The page loads
`simulator.js`, which renders the simulation onto an HTML5
`<canvas>` element at 1000 $\times$ 600 pixels. No server or
build step is required.


## Interface Layout

The canvas is divided into three regions (*User Manual*).


> **Figure.** Schematic layout of the simulator interface.


- **Left panel** (0–500 px): the shooter's view through the rear diopter, showing the front tunnel, iris, target, and a spirit-level indicator at the bottom.
- **Right panel** (500–1000 px): the target face with scoring rings. A cyan circle marks the parallax-shifted aim point; a red dot marks the predicted impact after all ballistic and mechanical corrections. A wind-direction indicator is displayed in the upper-right corner.
- **HUD panel** (bottom 85 px): numerical readouts of all parameters, the decimal score, and a control-key reminder.


## Controls Reference


**Table.** Complete keyboard and mouse controls.

| **Input** | **Action** | **Range** | **Section** |
| --- | --- | --- | --- |
| Mouse position | Eye offset (parallax) | canvas area | *Parallax Error* |
| **A** / **D** | Rear aperture $\pm 0.1$ mm | 0.8–2.2 mm | *Aperture Size and Eye Relief* |
| **Q** / **E** | Front iris $\pm 0.1$ mm | 2.4–7.0 mm | *Aperture Size and Eye Relief* |
| **C** / **V** | Iris ring thickness $\pm 0.1$ mm | 0.5–5.0 mm | *Aperture Size and Eye Relief* |
| **U** / **J** | Eye relief $\pm 1$ mm | 50–215 mm | *Aperture Size and Eye Relief* |
| **W** / **S** | Sight height $\pm 1$ mm | $\geq 20$ mm | *Exterior Ballistics: Gravity and Trajectory* |
| **Z** / **X** | Rifle cant $\pm 0.57^{\circ}$ | unlimited | *Rifle Cant* |
| Arrow keys | Mechanical clicks $\pm 1$ px | unlimited | *Mechanical Sight Adjustment (Clicks)* |
| **O** / **P** | Wind speed $\pm 0.5$ m/s | 0–10 m/s | *Wind Drift* |
| **K** / **L** | Wind direction $\pm 8.6^{\circ}$ | full circle | *Wind Drift* |
| **T** | Toggle 10 m / 50 m target | — | *Exterior Ballistics: Gravity and Trajectory* |


## Quick-Start Walkthrough


1. Open `sight.html`. The default view shows a 10 m air-rifle sight picture centered on the target.
2. Move the mouse across the left panel and observe both the sight picture shift and the cyan circle moving on the right panel. This is *parallax* (*Parallax Error*).
3. Press **Z** several times to cant the rifle. Watch the spirit level and the red impact dot on the right panel shift right *and* down (*Rifle Cant*).
4. Use the arrow keys to bring the red dot back to center—these are sight “clicks” (*Mechanical Sight Adjustment (Clicks)*).
5. Press **T** to switch to the 50 m target and observe how gravity drop and cant error grow dramatically (*Exterior Ballistics: Gravity and Trajectory*).
6. Increase wind with **P** and rotate its direction with **K**/**L** to see wind drift (*Wind Drift*).
