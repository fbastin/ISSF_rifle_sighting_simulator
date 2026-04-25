# ISSF Rifle Sighting Simulator

A web-based simulator designed to help users understand and practice the mechanics of sighting an ISSF (International Shooting Sport Federation) rifle. 

By utilizing HTML and JavaScript, this project provides a lightweight, interactive environment to simulate sight adjustments (elevation and windage) and their direct impact on point of impact, helping shooters and coaches visualize sighting theory without needing to be at the range.

## Files and Structure

- **`sight.html`**: The main entry point for the simulator. Open this file in any modern web browser to run the application.
- **`simulator.js`**: The core JavaScript logic that powers the simulation, handles user inputs, and calculates the sight adjustments and shot placements.
- **`doc.tex` / `doc.pdf`**: The underlying documentation and mathematical/theoretical explanation behind the simulator, written in LaTeX and provided as a compiled PDF.
- **`tex2html.py`**: A Python utility script used to convert the LaTeX documentation (`doc.tex`) into HTML format.
- **`docs/`**: Directory containing additional documentation or supplementary project assets.

## Getting Started

### Prerequisites
No special software is required to run the simulator. All you need is a modern web browser (e.g., Chrome, Firefox, Safari, Edge).

To modify the documentation or use the Python script, you will need:
- A LaTeX distribution (e.g., TeX Live, MiKTeX) to compile `doc.tex`.
- Python 3.x to run the `tex2html.py` conversion script.

### Running the Simulator
1. Clone or download this repository to your local machine:
   ```bash
   git clone [https://github.com/fbastin/ISSF_rifle_sighting_simulator.git](https://github.com/fbastin/ISSF_rifle_sighting_simulator.git)