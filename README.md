# OpenMC Geometry Modeling Examples

This repository contains a small set of OpenMC examples that document my practical exposure to Monte Carlo reactor physics and nuclear-fuel geometry modeling.

## Projects

### 1. Basic cylindrical fuel pin
`01_basic_pin/basic_pin.py`

A simple PWR-style pin-cell model using:
- 4.25% enriched UO2 fuel
- Zircaloy cladding
- Light-water moderator
- Cylindrical fuel and cladding surfaces
- Reflective square boundary
- `openmc.model.pin()` for pin construction

### 2. Hexagonal fuel pin
`02_hexagonal_pin/hexagonal_pin.py`

A variation of the pin model using a reflective hexagonal prism boundary. This example demonstrates how the same pin concept can be placed inside a different lattice cell shape.

### 3. CANDU-style 37-element fuel bundle
`03_candu_bundle/candu_bundle.py`

A more advanced geometry-building example based on concentric fuel-pin rings. It demonstrates:
- UO2 fuel and Zircaloy cladding
- Heavy-water moderator
- Concentric moderator regions
- Explicit fuel-pin placement using polar coordinates
- Ring populations of 1, 6, 12, and 18 pins
- Pin translations in the OpenMC universe
- Explicit cell IDs for later identification in tallies
- Geometry plotting for inspection

The bundle geometry uses representative pressure-tube and calandria dimensions as parameters in the script.

## Software

- Python 3
- OpenMC
- NumPy
- Matplotlib

## Installation

Install OpenMC according to the official documentation and install the Python dependencies with:

```bash
pip install -r requirements.txt
```

## Running the examples

From the repository root:

```bash
python 01_basic_pin/basic_pin.py
python 02_hexagonal_pin/hexagonal_pin.py
python 03_candu_bundle/candu_bundle.py
```

The scripts create geometry objects and use OpenMC plotting to visualize the models. They are geometry-learning examples and do not by themselves perform a complete criticality calculation.

## What I practiced

These examples helped me practice the following OpenMC concepts:

- `Material`
- elemental and isotopic composition
- density assignment
- S(alpha,beta) thermal scattering data
- `ZCylinder`
- reflective boundaries
- `Cell`
- `Universe`
- `Geometry`
- `openmc.model.pin()`
- `openmc.model.hexagonal_prism()`
- cell regions and Boolean geometry operations
- cell translation
- explicit cell IDs
- geometry plotting

## Suggested next steps

A natural extension of this repository is to add a complete eigenvalue calculation with:

1. a `settings.xml` definition,
2. source distribution,
3. materials and geometry XML export,
4. `openmc.run()`,
5. statepoint analysis, and
6. `k-effective` and neutron-flux tallies.

## Note

The repository is intended to demonstrate OpenMC learning and geometry-modeling practice. Parameter values should be checked against the specific reactor design and reference used for any research calculation.
