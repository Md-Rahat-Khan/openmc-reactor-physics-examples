"""PWR fuel-pin eigenvalue calculation using OpenMC.

This example extends the basic 4.25%-enriched UO2 pin-cell model with
criticality settings and a simple cell-based neutron flux tally.

The model is intended for learning and portfolio demonstration, not for
reactor design or licensing calculations.
"""

from pathlib import Path

import openmc


# -----------------------------
# 1. Materials
# -----------------------------
fuel = openmc.Material(name="UO2 fuel")
fuel.add_element("U", 1.0, percent_type="ao", enrichment=4.25)
fuel.add_element("O", 2.0)
fuel.set_density("g/cm3", 10.4)

clad = openmc.Material(name="Zircaloy cladding")
clad.add_element("Zr", 1.0)
clad.set_density("g/cm3", 6.0)

water = openmc.Material(name="Light water")
water.add_element("H", 2.0)
water.add_element("O", 1.0)
water.set_density("g/cm3", 1.0)
water.add_s_alpha_beta("c_H_in_H2O")

materials = openmc.Materials([fuel, clad, water])


# -----------------------------
# 2. Geometry
# -----------------------------
r_fuel = 0.32  # cm
r_clad = 0.34  # cm
pitch = 1.24   # cm

fuel_surface = openmc.ZCylinder(r=r_fuel)
clad_surface = openmc.ZCylinder(r=r_clad)

fuel_cell = openmc.Cell(name="Fuel", fill=fuel, region=-fuel_surface)
clad_cell = openmc.Cell(
    name="Cladding", fill=clad, region=+fuel_surface & -clad_surface
)
moderator_cell = openmc.Cell(
    name="Moderator", fill=water, region=+clad_surface
)

pin_universe = openmc.Universe(
    name="PWR pin universe", cells=[fuel_cell, clad_cell, moderator_cell]
)

pin_boundary = openmc.model.rectangular_prism(
    pitch, pitch, boundary_type="reflective"
)
root_cell = openmc.Cell(name="Root", fill=pin_universe, region=pin_boundary)

geometry = openmc.Geometry(root_cell)


# -----------------------------
# 3. Criticality settings
# -----------------------------
settings = openmc.Settings()
settings.run_mode = "eigenvalue"
settings.batches = 100
settings.inactive = 20
settings.particles = 5000
settings.seed = 12345

source_space = openmc.stats.Box(
    lower_left=(-pitch / 2, -pitch / 2, -0.1),
    upper_right=(pitch / 2, pitch / 2, 0.1),
)
settings.source = openmc.IndependentSource(
    space=source_space,
    constraints={"fissionable": True},
)


# -----------------------------
# 4. Flux tally
# -----------------------------
cell_filter = openmc.CellFilter(fuel_cell)
flux_tally = openmc.Tally(name="fuel flux")
flux_tally.filters = [cell_filter]
flux_tally.scores = ["flux"]

tallies = openmc.Tallies([flux_tally])


# -----------------------------
# 5. Build and run
# -----------------------------
model = openmc.Model(
    geometry=geometry,
    materials=materials,
    settings=settings,
    tallies=tallies,
)

# Export XML input files to this directory.
output_dir = Path("openmc_input")
output_dir.mkdir(exist_ok=True)
model.export_to_xml(output_dir)

# Generate a simple geometry image for the repository.
plot = openmc.Plot()
plot.filename = str(Path("results") / "pwr_pin_geometry")
plot.basis = "xy"
plot.origin = (0.0, 0.0, 0.0)
plot.width = (pitch, pitch)
plot.pixels = (600, 600)
plot.color_by = "material"
openmc.Plots([plot]).export_to_xml(output_dir)
openmc.plot_geometry(output=output_dir)

print("Running OpenMC eigenvalue calculation...")
statepoint_path = model.run(cwd=output_dir)

# -----------------------------
# 6. Post-processing
# -----------------------------
with openmc.StatePoint(statepoint_path) as statepoint:
    keff = statepoint.keff
    tally = statepoint.get_tally(name="fuel flux")
    flux_mean = float(tally.mean.flatten()[0])
    flux_std = float(tally.std_dev.flatten()[0])

summary = (
    "PWR Pin-Cell Eigenvalue Calculation\n"
    "===================================\n"
    f"k-effective: {keff.nominal_value:.6f}\n"
    f"k-effective standard deviation: {keff.std_dev:.6f}\n"
    f"Fuel-cell flux tally: {flux_mean:.6e}\n"
    f"Fuel-cell flux standard deviation: {flux_std:.6e}\n"
)

Path("results").mkdir(exist_ok=True)
Path("results/statepoint_summary.txt").write_text(summary, encoding="utf-8")

print(summary)
