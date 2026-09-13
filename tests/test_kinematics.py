## testing for force solvers and Hertzian stress outputs
import numpy as np
import pytest
from src.hertzian import hertzian_contact_stress
from src.kinematics import (compute_pin_forces_baseline, compute_pin_forces_proposed, pin_contact_angle)


def test_pin_contact_angle_convergence():
    """test 1D root finder convergence for contact pressure angle"""
    pitch_r = 0.0265
    ecc = 0.00075
    num_pins = 31

    alpha0 = pin_contact_angle(theta_input=0, pin_index=0, num_pins=num_pins, eccentricity=ecc, pitch_radius=pitch_r)

    assert isinstance(alpha0, float)
    assert -np.pi / 2 <= alpha0 <= np.pi /2

def test_compute_pin_forces_proposed_output():
    """test active force distribution array sizing and non-negative forces"""
    torque = 1.2
    num_teeth = 30
    pitch_r = 0.0265
    ecc = 0.00075

    forces = compute_pin_forces_proposed(torque, num_teeth, pitch_r, ecc)

    assert len(forces) == num_teeth + 1
    assert np.all(forces >= 0.0)
    assert np.max(forces) > 0.0  

def test_compute_pin_forces_baseline_output():
    """test uniform force distribution baseline model"""
    torque = 1.2
    num_teeth = 30
    pitch_r = 0.0265
    num_pins = num_teeth + 1

    forces = compute_pin_forces_baseline(torque, num_teeth, pitch_r)
    expected_force = torque / (num_pins * pitch_r)

    assert len(forces) == num_pins
    assert np.allclose(forces, expected_force) 

def test_hertzian_contact_stress_positive():
    """test closed-form hertzian line contact stress output"""
    normal_force = 50.0  # N
    disc_thickness = 0.004  # m
    radius_cycloid = 0.015  # m
    radius_pin = 0.0015  # m

    stress = hertzian_contact_stress(
        normal_force, disc_thickness, radius_cycloid, radius_pin
    )

    assert stress > 0.0
    assert stress > 1e6 #expected stress is usually around the MPa range