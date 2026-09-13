#dedicated testing for teeth profiel and undercut exceptions

import numpy as np
import pytest
from src.geometry import calculate_gear_ratio, generate_cycloid_profile

def test_generate_cycloid_profile():
    """test generating profile with valid SI unit dimensions"""
    pitch_r = 0.053 /2 #26.5mm pitch radius
    pin_r = 0.0015 # 1.5mm pin radius
    ecc = 0.00075 # 0.75mm eccentricity
    num_teeth = 30
    num_points = 500

    x, y = generate_cycloid_profile(pitch_r, pin_r, ecc, num_teeth, num_points)

    assert len(x) == num_points
    assert len(y) == num_points
    assert isinstance(x, np.ndarray)
    assert isinstance(y, np.ndarray)

def test_generate_cycloid_profile_undercut_exception():
    """test if there is excessive eccentricity which raises a ValueError for undercutting"""
    pitch_r = 0.010
    pin_r = 0.0015
    ecc = 0.005  # 0.005 * 31 > 0.010 -> Triggers undercutting check
    num_teeth = 30

    with pytest.raises(ValueError, match="Excessive eccentricity causes tooth undercutting!"):
        generate_cycloid_profile(pitch_r, pin_r, ecc, num_teeth)

def test_generate_cycloid_profile_invalid_inputs():
    """test that zero or negative physical dimensions raise ValueError"""
    with pytest.raises(
        ValueError, match="Eccentricity must be greater than zero."):
        generate_cycloid_profile(0.0265, 0.0015, -0.00075, 30)

    with pytest.raises(
        ValueError, match="Pitch radius and pin radius must be positive."):
        generate_cycloid_profile(0.0, 0.0015, 0.00075, 30)

def test_calculate_gear_ratio():
    """est single-stage gear reduction ratio calculation."""
    assert calculate_gear_ratio(30) == 30.0
    assert calculate_gear_ratio(10) == 10.0

    with pytest.raises(
        ValueError, match="Number of teeth must be at least 1."
    ):
        calculate_gear_ratio(0)