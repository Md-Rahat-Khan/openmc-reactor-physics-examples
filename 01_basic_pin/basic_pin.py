import openmc

# Materials
fuel = openmc.Material(name="UO2 fuel")
fuel.add_element("U", 1, percent_type="ao", enrichment=4.25)
fuel.add_element("O", 2)
fuel.set_density("g/cc", 10.4)

clad = openmc.Material(name="Zircaloy cladding")
clad.add_element("Zr", 1)
clad.set_density("g/cc", 6.0)

water = openmc.Material(name="Light water")
water.add_element("O", 1)
water.add_element("H", 2)
water.set_density("g/cc", 1.0)
water.add_s_alpha_beta("c_H_in_H2O")

materials = openmc.Materials([fuel, clad, water])

# Fuel and cladding radii (cm)
radii = [0.32, 0.34]

# Build a pin cell using OpenMC's pin helper
pin_surfaces = [openmc.ZCylinder(r=r) for r in radii]
pin_universe = openmc.model.pin(pin_surfaces, materials)

# Reflective square boundary
bound_box = openmc.model.rectangular_prism(
    1.24, 1.24, boundary_type="reflective"
)

root_cell = openmc.Cell(fill=pin_universe, region=bound_box)
geometry = openmc.Geometry([root_cell])

# Plot the geometry
geometry.root_universe.plot()
