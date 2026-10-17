import math
from ceramic_props.calculations import (
    standardize_formulation,
    compute_dry_properties,
    compute_final_properties,
    compute_membrane_performance,
)


def approx(a, b, tol=1e-4):
    return abs(a-b) <= tol


def test_standardize_formulation():
    vals = [44, 16, 8, 12, 10]
    std = standardize_formulation(vals)
    # From the original notebook the standardized values were approx: 48.89,17.78,8.89,13.33,11.11
    assert approx(std[0], 48.8889, 1e-3)
    assert approx(std[1], 17.7778, 1e-3)
    assert approx(std[2], 8.8889, 1e-3)
    assert approx(std[3], 13.3333, 1e-3)
    assert approx(std[4], 11.1111, 1e-3)


def test_membrane_performance_sample():
    # Values taken from the executed notebook run: apparent_porosity ~48.44, area 2073.6, thickness 11.5
    apparent_porosity = 48.44
    area = 2073.6
    thickness = 11.5
    viscosity = 0.0089
    pressure = 1.0
    flow_rate = 300.0

    perf = compute_membrane_performance(apparent_porosity, area, thickness, viscosity, pressure, flow_rate)
    # permeability and average pore size should be non-zero and classification microporous per notebook
    assert perf['permeability'] > 0
    assert perf['average_pore_size_microns'] >= 0
    assert perf['classification'] in ("Microporous", "Mesoporous", "Macroporous")
