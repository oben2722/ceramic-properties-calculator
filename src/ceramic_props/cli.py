"""Command-line interface for the Ceramic Membrane Material Science Calculator.

This interactive script reproduces the original Colab flow but calls the
pure functions defined in ceramic_props.calculations so results are testable.
"""
from ceramic_props.calculations import (
    standardize_formulation,
    compute_dry_properties,
    measurement_validation,
    compute_final_properties,
    compute_membrane_performance,
)


def get_positive_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a positive number.")
            else:
                return value
        except ValueError:
            print("Please enter a valid number.")


def run_interactive():
    print("=== Ceramic Membrane Material Science Calculator ===\n")

    print("--- Standardizing Formulation ---")
    kaolin = get_positive_float('Enter the proportion of kaolin: ')
    rice_husk = get_positive_float('Enter the proportion of rice husk: ')
    calcite = get_positive_float('Enter the proportion of calcite: ')
    feldspar = get_positive_float('Enter the proportion of feldspar: ')
    quartz = get_positive_float('Enter the proportion of quartz: ')
    standardized = standardize_formulation([kaolin, rice_husk, calcite, feldspar, quartz])
    print("Standardized proportions: ")
    print(f"  Kaolin = {standardized[0]:.2f}%, Rice Husk = {standardized[1]:.2f}%, Calcite = {standardized[2]:.2f}%, Feldspar = {standardized[3]:.2f}%, Quartz = {standardized[4]:.2f}%")

    print("\n--- Initial Dimensions (dry) ---")
    dry_length = get_positive_float('Enter the length of the dry membrane in mm: ')
    dry_thickness = get_positive_float('Enter the thickness of the dry membrane in mm: ')
    dry_width = get_positive_float('Enter the width of the dry membrane in mm: ')
    dry_mass = get_positive_float('Enter the mass of the dry membrane in g: ')
    theoretical_density = get_positive_float('Enter the theoretical density (g/cm^3): ')
    dry_props = compute_dry_properties(dry_length, dry_thickness, dry_width, dry_mass)
    print(f"The surface area of the dry membrane is {dry_props['surface_area_mm2']:.2f} mm^2\n the volume is {dry_props['volume_mm3']:.2f} mm^3\n dry_bulk_density is {dry_props['bulk_density_g_per_cm3']:.4f} g/cm^3")

    print("\n--- Final Physical Characterization (ASTM C 373) ---")
    while True:
        final_length = get_positive_float('Enter the length of the final membrane in mm : ')
        final_thickness = get_positive_float('Enter the thickness of the final membrane in mm : ')
        final_width = get_positive_float('Enter the width of the final membrane in mm : ')
        final_mass = get_positive_float('Enter the mass of the final membrane in g : ')
        suspended_mass = get_positive_float('Enter the suspended mass of the final membrane in g : ')
        saturated_mass = get_positive_float('Enter the saturated mass of the final membrane in g : ')

        if measurement_validation(dry_length, dry_mass, final_length, final_mass, suspended_mass, saturated_mass):
            break
        print('Please re-enter correct physical measurements.\n')

    final_props = compute_final_properties(
        dry_length, dry_mass, theoretical_density,
        final_length, final_thickness, final_width, final_mass, suspended_mass, saturated_mass,
    )

    print('\nResults:')
    print(f"  Final Surface Area: {final_props['final_surface_area_mm2']:.2f} mm^2")
    print(f"  Final Volume: {final_props['final_volume_mm3']:.2f} mm^3")
    print(f"  Final Bulk Density: {final_props['final_bulk_density_g_per_cm3']:.4f} g/cm^3")
    print(f"  Linear Shrinkage: {final_props['linear_shrinkage_fraction']:.4f} ({final_props['linear_shrinkage_fraction']*100:.2f}%)")
    print(f"  Mass Loss: {final_props['mass_loss_fraction']:.4f} ({final_props['mass_loss_fraction']*100:.2f}%)")
    print(f"  Apparent Porosity: {final_props['apparent_porosity_percent']:.2f}%")
    print(f"  Water Absorption: {final_props['water_absorption_percent']:.2f}%")
    print(f"  Relative Density: {final_props['relative_density_percent']:.2f}%")
    print(f"  Total Porosity: {final_props['total_porosity_percent']:.2f}%")

    print('\n--- Membrane Performance Analysis ---')
    water_viscosity = get_positive_float("Enter the water viscosity (cP): ")
    pressure_difference = get_positive_float("Enter the pressure difference (bar): ")
    flow_rate = get_positive_float("Enter the measured water flow rate (mL/hour): ")

    perf = compute_membrane_performance(final_props['apparent_porosity_percent'], final_props['final_surface_area_mm2'], final_props['final_volume_mm3']**0.0 + final_props.get('final_volume_mm3', 0), water_viscosity, pressure_difference, flow_rate)
    # Note: original notebook passed membrane_thickness; in this interactive flow we reuse final_thickness
    perf = compute_membrane_performance(final_props['apparent_porosity_percent'], final_props['final_surface_area_mm2'], final_thickness, water_viscosity, pressure_difference, flow_rate)

    print('\nPerformance Metrics:')
    print(f"  Water Permeability: {perf['permeability']:.4f}")
    print(f"  Average Pore Size: {perf['average_pore_size_microns']:.4f} microns")
    print(f"  Membrane Classification: {perf['classification']}")
    print(f"  Recommended Application: {perf['recommended_application']}")


if __name__ == '__main__':
    run_interactive()
