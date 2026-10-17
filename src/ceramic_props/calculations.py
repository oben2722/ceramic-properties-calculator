"""Pure calculation functions for the Ceramic Membrane Material Science Calculator.

This module provides non-interactive, testable functions that implement the
formulas used in the original Colab notebook. Units:
- lengths: mm
- areas: mm^2
- volumes: mm^3
- mass: g
- densities: g/cm^3 (conversion applied where needed)
- flow_rate: mL/hour (same as notebook)
- viscosity: cP
- pressure: bar

These functions avoid interactive input() calls and return numeric results suitable
for unit testing and reuse in scripts or web apps.
"""
from typing import List, Tuple, Dict
import math


def standardize_formulation(values: List[float]) -> List[float]:
    """Normalize a list of raw-material proportions so they sum to 100%.

    If the inputs already sum to 100 (within a small tolerance) they are
    returned unchanged. Otherwise values are rescaled proportionally.
    """
    if not values:
        return []
    total = sum(values)
    if abs(total - 100.0) < 1e-8:
        return [float(v) for v in values]
    if total == 0:
        raise ValueError("Sum of input values is zero; cannot standardize")
    return [(v / total) * 100.0 for v in values]


def compute_dry_properties(length_mm: float, thickness_mm: float, width_mm: float, mass_g: float) -> Dict[str, float]:
    """Compute dry surface area, dry volume and bulk density.

    Returns a dict with keys: surface_area_mm2, volume_mm3, bulk_density_g_per_cm3
    Note: bulk density converts mm^3 -> cm^3 (1 cm^3 = 1000 mm^3).
    """
    surface_area = length_mm * width_mm
    volume_mm3 = length_mm * thickness_mm * width_mm
    # convert mm^3 to cm^3 for density calculation
    volume_cm3 = volume_mm3 / 1000.0
    bulk_density_g_per_cm3 = mass_g / volume_cm3 if volume_cm3 > 0 else 0.0
    return {
        "surface_area_mm2": surface_area,
        "volume_mm3": volume_mm3,
        "bulk_density_g_per_cm3": bulk_density_g_per_cm3,
    }


def measurement_validation(dry_length: float, dry_mass: float, final_length: float, final_mass: float, suspended_mass: float, saturated_mass: float) -> bool:
    """Validate measured physical quantities for basic consistency.

    Returns True if values pass simple physical checks, False otherwise.
    """
    is_valid = True
    if final_mass > saturated_mass:
        is_valid = False
    if suspended_mass > final_mass:
        is_valid = False
    if final_mass > dry_mass:
        is_valid = False
    if final_length > dry_length:
        is_valid = False
    return is_valid


def compute_final_properties(
    dry_length_mm: float,
    dry_mass_g: float,
    theoretical_density_g_per_cm3: float,
    final_length_mm: float,
    final_thickness_mm: float,
    final_width_mm: float,
    final_mass_g: float,
    suspended_mass_g: float,
    saturated_mass_g: float,
) -> Dict[str, float]:
    """Compute final properties following ASTM C 373 style formulas.

    Returns dict containing:
      final_surface_area_mm2, final_volume_mm3, final_bulk_density_g_per_cm3,
      linear_shrinkage (fraction), mass_loss (fraction), apparent_porosity_percent,
      water_absorption_percent, relative_density_percent, total_porosity_percent
    """
    final_surface_area = final_length_mm * final_width_mm
    final_volume_mm3 = final_length_mm * final_thickness_mm * final_width_mm
    final_volume_cm3 = final_volume_mm3 / 1000.0
    final_bulk_density = final_mass_g / final_volume_cm3 if final_volume_cm3 > 0 else 0.0
    linear_shrinkage = (dry_length_mm - final_length_mm) / dry_length_mm if dry_length_mm > 0 else 0.0
    mass_loss = (dry_mass_g - final_mass_g) / dry_mass_g if dry_mass_g > 0 else 0.0

    volume_of_open_pores = saturated_mass_g - final_mass_g
    volume_of_membrane = saturated_mass_g - suspended_mass_g
    if volume_of_membrane > 0:
        apparent_porosity = (volume_of_open_pores / volume_of_membrane) * 100.0
    else:
        apparent_porosity = 0.0

    water_absorption = (volume_of_open_pores / final_mass_g) * 100.0 if final_mass_g > 0 else 0.0
    relative_density = (final_bulk_density / theoretical_density_g_per_cm3) * 100.0 if theoretical_density_g_per_cm3 > 0 else 0.0
    total_porosity = 100.0 - relative_density

    return {
        "final_surface_area_mm2": final_surface_area,
        "final_volume_mm3": final_volume_mm3,
        "final_bulk_density_g_per_cm3": final_bulk_density,
        "linear_shrinkage_fraction": linear_shrinkage,
        "mass_loss_fraction": mass_loss,
        "apparent_porosity_percent": apparent_porosity,
        "water_absorption_percent": water_absorption,
        "relative_density_percent": relative_density,
        "total_porosity_percent": total_porosity,
    }


def compute_membrane_performance(
    apparent_porosity_percent: float,
    membrane_area_mm2: float,
    membrane_thickness_mm: float,
    water_viscosity_cP: float,
    pressure_difference_bar: float,
    flow_rate_mL_per_hour: float,
) -> Dict[str, float]:
    """Calculate permeability, average pore size and classification.

    The formulas are taken from the Colab notebook. Units are kept consistent with
    the original implementation (flow_rate in mL/hour, viscosity in cP, thickness in mm).
    """
    epsilon = apparent_porosity_percent / 100.0
    permeability = (flow_rate_mL_per_hour * water_viscosity_cP * membrane_thickness_mm) / pressure_difference_bar if pressure_difference_bar > 0 else 0.0

    average_pore_size = 0.0
    try:
        inner_term = (2.9 - 1.75 * epsilon) * 8 * water_viscosity_cP * membrane_thickness_mm * flow_rate_mL_per_hour
        if inner_term >= 0 and (epsilon * membrane_area_mm2 * pressure_difference_bar) > 0:
            average_pore_size = math.sqrt(inner_term) / (epsilon * membrane_area_mm2 * pressure_difference_bar)
        else:
            average_pore_size = 0.0
    except Exception:
        average_pore_size = 0.0

    if average_pore_size > 50.0:
        classification = "Macroporous"
        application = "Microfiltration"
    elif 2.0 < average_pore_size <= 50.0:
        classification = "Mesoporous"
        application = "Microfiltration"
    else:
        classification = "Microporous"
        application = "Ultrafiltration"

    return {
        "permeability": permeability,
        "average_pore_size_microns": average_pore_size,
        "classification": classification,
        "recommended_application": application,
    }
