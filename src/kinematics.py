"""Contact mechanics and load distribution solver module."""

import numpy as np
from scipy.optimize import root_scalar


def pin_contact_angle(
    theta_input: float,
    pin_index: int,
    num_pins: int,
    eccentricity: float,
    pitch_radius: float,
) -> float:
    """Calculates the contact pressure angle for a specific housing pin.

    Solves the non-linear position constraint using 1D root-finding.
    """
    if num_pins < 2:
        raise ValueError("num_pins must be at least 2.")
    
    if not 0 <= pin_index < num_pins:
        raise ValueError("pin_index must be between 0 and num_pins - 1.")
    
    if eccentricity <= 0 or pitch_radius <= eccentricity:
        raise ValueError("Require eccentricity > 0 and pitch_radius > eccentricity.")

    phi_pin = 2.0 * np.pi * pin_index / num_pins

    def contact_equation(alpha: float) -> float:
        return pitch_radius * np.sin(alpha - phi_pin) - eccentricity * np.sin(
            alpha - theta_input
        )

    result = root_scalar(
        contact_equation, bracket=[-np.pi / 2, np.pi / 2], method="brentq"
    )
    if not result.converged:
        raise RuntimeError("Root finder failed to converge on contact angle.")
    
    return float(result.root)


def compute_pin_forces_proposed(
    torque_input: float,
    num_teeth: int,
    pitch_radius: float,
    eccentricity: float,
    theta_input: float = 0.0,
) -> np.ndarray:
    """Calculates pin force distribution using variable contact angles (Proposed Method)."""
    if torque_input < 0:
        raise ValueError("torque_input must be non-negative.")
    
    if num_teeth < 1:
        raise ValueError("num_teeth must be at least 1.")
    
    if pitch_radius <= 0 or eccentricity <= 0:
        raise ValueError("pitch_radius and eccentricity must be positive.")

    num_pins = num_teeth + 1

    forces = np.zeros(num_pins)
    for i in range(num_pins):
        alpha = pin_contact_angle(
            theta_input, i, num_pins, eccentricity, pitch_radius
        )

        moment_arm = pitch_radius * np.sin(alpha)
        if moment_arm > 0:
            forces[i] = (torque_input / (num_pins * eccentricity)) * np.sin(alpha)

    return forces


def compute_pin_forces_baseline(
    torque_input: float, num_teeth: int, pitch_radius: float
) -> np.ndarray:
    """Calculates uniform force distribution assuming equal load across pins (Baseline Method)."""
    if torque_input < 0:
        raise ValueError("torque_input must be non-negative.")
    
    if num_teeth < 1:
        raise ValueError("num_teeth must be at least 1.")
    
    if pitch_radius <= 0:
        raise ValueError("pitch_radius must be positive.")
    
    num_pins = num_teeth + 1

    average_force = torque_input / (num_pins * pitch_radius)
    return np.full(num_pins, average_force)
