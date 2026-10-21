"""Simple Coulomb-friction loss model for preliminary cycloidal-drive studies.

This module estimates frictional power from normal contact forces and relative
sliding speeds. It does not calculate the contact kinematics itself: sliding
speeds must be supplied by the caller and should eventually come from a
validated kinematic model or measurements.
"""

from __future__ import annotations
import numpy as np

def frictional_power_loss(normal_forces: np.ndarray, coefficient_of_friction: float, sliding_speeds: float | np.ndarray,
) -> float:
    """Estimate tpta; frictional power loss using Coulomb friction

    For each contact, friction magnitude is approximated by F_f = mu * F_n,
    and frictional power is P_loss = F_f * abs(v_slip)

    Parameters:
        normal_forces: Normal contact forces in newtons. Negative forces are not physically valid for this model.
        coefficient_of_friction: Dimensionless Coulomb friction coefficient, mu >= 0.
        sliding_speeds: Relative sliding speed at each contact in m/s. May be
            a scalar shared by all contacts or an array matching normal_forces.
            Use zero only for a genuinely zero-sliding contact, not as a default
            assumption for a real gearbox

    Returns:
        Estimated total frictional power loss in watts
    """

    forces = np.asarray(normal_forces, dtype=float)
    speeds = np.asarray(sliding_speeds, dtype=float)

    if forces.size == 0:
        raise ValueError("normal_forces must not be empty.")
    
    if not np.all(np.isfinite(forces)) or not np.all(np.isfinite(speeds)):
        raise ValueError("Forces and sliding speeds must be finite.")
    
    if np.any(forces < 0):
        raise ValueError("Normal forces must be non-negative.")
    
    if coefficient_of_friction < 0 or not np.isfinite(coefficient_of_friction):
        raise ValueError("coefficient_of_friction must be finite and non-negative.")
    
    if np.any(speeds < 0):
        raise ValueError("Sliding speeds must be supplied as non-negative magnitudes.")

    try:
        speeds = np.broadcast_to(speeds, forces.shape)

    except ValueError as exc:
        raise ValueError(
            "sliding_speeds must be a scalar or match the shape of normal_forces."
        ) from exc

    friction_forces = coefficient_of_friction * forces
    power_loss = np.sum(friction_forces * speeds)
    return float(power_loss)

def estimate_output_performance(torque_input: float, input_speed_rpm: float, gear_ratio: float, friction_power_loss: float,
) -> dict[str, float]:
    """Estimate output torque and efficiency from an estimated power loss.

    Parameters:
        torque_input: Input torque magnitude in N*m.
        input_speed_rpm: Input speed magnitude in rpm.
        gear_ratio: Positive reduction ratio, omega_in / omega_out.
        friction_power_loss: Estimated frictional loss in watts.

    Returns:
        Dictionary with input power, ideal output torque, estimated output
        torque, loss power, and estimated efficiency (fraction from 0 to 1).
    """
    values = (torque_input, input_speed_rpm, gear_ratio, friction_power_loss)
    if not all(np.isfinite(value) for value in values):
        raise ValueError("All inputs must be finite.")
    
    if torque_input < 0 or input_speed_rpm < 0 or friction_power_loss < 0:
        raise ValueError("Torque, speed, and loss power must be non-negative.")
    
    if gear_ratio <= 0:
        raise ValueError("gear_ratio must be greater than zero.")

    omega_input = input_speed_rpm * 2.0 * np.pi / 60.0
    input_power = torque_input * omega_input
    ideal_output_torque = torque_input * gear_ratio

    if input_power == 0:
        if friction_power_loss > 0:
            raise ValueError("Loss power cannot exceed zero input power.")
        return {
            "input_power_w": 0.0,
            "friction_power_loss_w": 0.0,
            "ideal_output_torque_nm": ideal_output_torque,
            "estimated_output_torque_nm": 0.0,
            "estimated_efficiency": 0.0,
        }

    if friction_power_loss >= input_power:
        raise ValueError(
            "Estimated friction loss must be lower than input power. Check the "
            "force model, sliding-speed assumptions, and friction coefficient."
        )

    output_power = input_power - friction_power_loss
    estimated_efficiency = output_power / input_power
    estimated_output_torque = ideal_output_torque * estimated_efficiency

    return {
        "input_power_w": float(input_power),
        "friction_power_loss_w": float(friction_power_loss),
        "ideal_output_torque_nm": float(ideal_output_torque),
        "estimated_output_torque_nm": float(estimated_output_torque),
        "estimated_efficiency": float(estimated_efficiency),
    }