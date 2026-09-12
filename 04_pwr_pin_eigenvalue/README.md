# PWR Pin-Cell Eigenvalue Calculation

This example extends the basic OpenMC fuel-pin geometry into a simple continuous-energy criticality calculation.

## Model

- 4.25 at.% enriched UO2 fuel
- Zircaloy cladding
- Light-water moderator with thermal scattering data
- 1.24 cm reflective square pitch
- Fuel radius: 0.32 cm
- Cladding outer radius: 0.34 cm

## What this example demonstrates

- `openmc.Settings` for an eigenvalue problem
- Initial neutron source distribution
- Fissionable-source constraint
- `batches`, `inactive`, and `particles`
- Cell-based flux tally
- XML model export
- OpenMC execution from Python
- StatePoint post-processing
- Extraction of `k-effective`

## Run

From this directory:

```bash
python pwr_pin.py
```

The script creates the OpenMC input files under `openmc_input/` and writes a short result summary under `results/`.

## Important

The numerical result depends on the installed OpenMC version and nuclear-data library. The model is intended for learning and portfolio demonstration. It is not a validated benchmark or a reactor-design model.
