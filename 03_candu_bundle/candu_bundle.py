from math import cos, pi, sin

import numpy as np
import openmc

# Materials
fuel = openmc.Material(name="UO2 fuel")
fuel.add_element("U", 1.0)
fuel.add_element("O", 2.0)
fuel.set_density("g/cm3", 10.0)

clad = openmc.Material(name="Zircaloy cladding")
clad.add_element("Zr", 1.0)
clad.set_density("g/cm3", 6.0)

heavy_water = openmc.Material(name="Heavy water")
heavy_water.add_nuclide("H2", 2.0)
heavy_water.add_nuclide("O16", 1.0)
heavy_water.add_s_alpha_beta("c_D_in_D2O")
heavy_water.set_density("g/cm3", 1.1)

# Geometry dimensions (cm)
r_fuel = 0.6122
r_clad = 0.6540

pressure_tube_ir = 5.16890
pressure_tube_or = 5.60320
calendria_ir = 6.44780
calendria_or = 6.58750

# Radius from bundle center to each fuel-pin ring
ring_radii = np.array([0.0, 1.4885, 2.8755, 4.3305])

# Divide the moderator into concentric annular regions.
radial_surf = [
    openmc.ZCylinder(r=r)
    for r in (ring_radii[:-1] + ring_radii[1:]) / 2
]

water_cells = []
for i in range(ring_radii.size):
    if i == 0:
        water_region = -radial_surf[i]
    elif i == ring_radii.size - 1:
        water_region = +radial_surf[i - 1]
    else:
        water_region = +radial_surf[i - 1] & -radial_surf[i]

    water_cells.append(
        openmc.Cell(fill=heavy_water, region=water_region)
    )

plot_args = {"width": (2 * calendria_or, 2 * calendria_or)}

bundle_universe = openmc.Universe(cells=water_cells)

# Plot the moderator-only bundle before adding fuel pins.
bundle_universe.plot(**plot_args)

# Build a single fuel pin universe.
surf_fuel = openmc.ZCylinder(r=r_fuel)
fuel_cell = openmc.Cell(fill=fuel, region=-surf_fuel)
clad_cell = openmc.Cell(fill=clad, region=+surf_fuel)
pin_universe = openmc.Universe(cells=(fuel_cell, clad_cell))

pin_universe.plot(**plot_args)

# Number of pins in each ring and angular offsets (degrees)
num_pins = [1, 6, 12, 18]
angles = [0, 0, 15, 0]

for i, (r, n, a) in enumerate(zip(ring_radii, num_pins, angles)):
    for j in range(n):
        theta = (a + j / n * 360.0) * pi / 180.0
        x = r * cos(theta)
        y = r * sin(theta)

        pin_boundary = openmc.ZCylinder(x0=x, y0=y, r=r_clad)

        # Remove each fuel-pin volume from the heavy-water region.
        water_cells[i].region &= +pin_boundary

        pin = openmc.Cell(fill=pin_universe, region=-pin_boundary)
        pin.translation = (x, y, 0.0)

        # ID convention: ring number * 100 + pin number within ring
        pin.id = (i + 1) * 100 + j
        bundle_universe.add_cell(pin)

# Plot the complete CANDU-style bundle.
bundle_universe.plot(**plot_args)
