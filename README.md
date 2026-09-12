# OpenMC Reactor Physics Examples

This repository documents hands-on practice with the OpenMC Monte Carlo particle transport code and Python-based nuclear reactor geometry modeling.

The examples progress from simple fuel-pin geometry to a criticality calculation.

## Projects

### 1. Basic cylindrical fuel pin
`01_basic_pin/basic_pin.py`

A PWR-style reflected pin-cell geometry using 4.25% enriched UO2 fuel, Zircaloy cladding, and light-water moderator.

### 2. Hexagonal fuel pin
`02_hexagonal_pin/hexagonal_pin.py`

A pin-cell variation using a reflective hexagonal prism boundary.

### 3. CANDU-style 37-element fuel bundle
`03_candu_bundle/candu_bundle.py`

A heavy-water moderated bundle model with concentric rings containing 1, 6, 12, and 18 fuel pins. The example demonstrates explicit polar-coordinate placement, cell translation, Boolean regions, and cell IDs.

### 4. PWR pin-cell eigenvalue calculation
`04_pwr_pin_eigenvalue/pwr_pin.py`

A learning example that extends the basic PWR pin-cell model with criticality settings, a neutron source, a cell-based flux tally, OpenMC execution, and StatePoint post-processing to obtain k-effective.
## Software

- Python 3
- OpenMC 0.15.3 or compatible newer development version
- NumPy
- Matplotlib

OpenMC 0.15.3 is the latest numbered release listed by the official OpenMC project at the time this repository was prepared. citeturn623376search0

## Installation

Install OpenMC and its nuclear-data library following the official documentation, then install the Python packages:

```bash
pip install -r requirements.txt
```

OpenMC criticality simulations require a neutron cross-section data library configured on your system. The OpenMC documentation specifies that an eigenvalue problem uses a starting source and particle count in `Settings`. citeturn678841search6

## Running the examples

From the repository root:

```bash
python 01_basic_pin/basic_pin.py
python 02_hexagonal_pin/hexagonal_pin.py
python 03_candu_bundle/candu_bundle.py
python 04_pwr_pin_eigenvalue/pwr_pin.py
```

The first three scripts focus on geometry construction and plotting. The fourth performs an eigenvalue calculation and reads the resulting StatePoint file.

## OpenMC concepts practiced

- `Material`
- Elemental composition and enrichment
- Material density
- Thermal scattering data
- `ZCylinder`
- Reflective boundaries
- `Cell`, `Universe`, and `Geometry`
- `openmc.model.pin()`
- `openmc.model.hexagonal_prism()`
- Boolean region operations
- Cell translation
- Explicit cell IDs
- Geometry plotting
- `Settings`
- `IndependentSource`
- Fissionable source constraints
- `Tally` and `CellFilter`
- Eigenvalue calculations
- StatePoint post-processing
- `k-effective` extraction

## Portfolio note

These examples demonstrate practical learning in Monte Carlo reactor physics and OpenMC modeling. Parameters should be verified against validated benchmark data before being used for research conclusions or reactor-design work.
