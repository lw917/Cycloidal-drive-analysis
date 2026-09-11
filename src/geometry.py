"""
Geometry generation module for a cycloidal gear profile.
"""

import numpy as np


def generate_cycloid_profile(
    pitch_radius: float,
    pin_radius: float,
    eccentricity: float,
    num_teeth: int,
    num_points: int = 1000,
) -> tuple[np.ndarray, np.ndarray]:
    """Generates 2D Cartesian coordinates (x, y) for a cycloidal rotor disc profile.

    Parameters:
        pitch_radius (float): Radius of the pin pitch circle in meters (Rc).
        pin_radius (float): Radius of housing pins in meters (Rr).
        eccentricity (float): Shaft offset distance in meters (e).
        num_teeth (int): Number of teeth on the rotor disc (N).
        num_points (int): Number of points used to discretize the curve.

    Returns:
        tuple[np.ndarray, np.ndarray]: Arrays containing x and y coordinates.
    """
    # Check for invalid geometry inputs
    if eccentricity <= 0:
        raise ValueError("Eccentricity must be greater than zero.")
    if pitch_radius <= 0 or pin_radius <= 0:
        raise ValueError("Pitch radius and pin radius must be positive.")

    num_pins = num_teeth + 1

    # Check to prevent geometric undercutting / self-intersection
    if eccentricity * num_pins >= pitch_radius:
        raise ValueError(
            "Excessive eccentricity causes tooth undercutting!"
        )

    # Discretize input angle from 0 to 2*pi
    psi = np.linspace(0, 2 * np.pi, num_points)

    # Intermediate calculation angle (gamma)
    gamma = np.arctan2(
        np.sin(num_teeth * psi),
        (pitch_radius / (eccentricity * num_pins)) - np.cos(num_teeth * psi),
    )

    # Parametric equations for epitrochoid cycloid profile
    x = (
        pitch_radius * np.cos(psi)
        - pin_radius * np.cos(psi + gamma)
        - eccentricity * np.cos(num_pins * psi)
    )
    y = (
        -pitch_radius * np.sin(psi)
        + pin_radius * np.sin(psi + gamma)
        + eccentricity * np.sin(num_pins * psi)
    )

    return x, y


def calculate_gear_ratio(num_teeth: int) -> float:
    """Calculates single-stage reduction ratio."""
    if num_teeth < 1:
        raise ValueError("Number of teeth must be at least 1.")
    return float(num_teeth)
