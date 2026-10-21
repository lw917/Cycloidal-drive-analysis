import numpy as np

def hertzian_contact_stress(normal_force: float, disc_thickness: float, radius_pin: float, radius_cycloid: float, e_modulus: float = 2.1e11, poison_ratio: float = 0.3) -> float:
    """
    Calculatet the Max Hertzian line-contact stress between cycloid tooth and housing pin

    Args:
        normal_force (float): Contact normal force in Newtons
        disc_thickness (float): Axial thickness of rotor disc in meters
        radius_cycloid (float): Local radius of curvature of tooth profile in meters
        e_modulus (float): Young's Modulus in Pascals (default 210Gpa for steel)
        possion_ratio (float): Poisson's ratio (default 0.3)

    Returns:
        float: Peak Hertzian contact pressure in Pascals
    """

    if normal_force < 0:
        raise ValueError("normal_force must be non-negative.")
    if normal_force == 0:
        return 0.0
    if disc_thickness <= 0 or radius_pin <= 0 or radius_cycloid <= 0:
        raise ValueError("Thickness and radii must be positive.")
    if e_modulus <= 0:
        raise ValueError("e_modulus must be positive.")
    if not 0 <= poison_ratio < 0.5:
        raise ValueError("poisson_ratio must be in the range [0, 0.5).")

    # Two identical elastic materials: 1/E* = 2(1-nu^2)/E.
    effective_modulus = e_modulus / (2.0 * (1.0 - poison_ratio**2))
    effective_radius = 1.0 / (1.0 / radius_pin + 1.0 / radius_cycloid)
    max_pressure = np.sqrt(
        normal_force * effective_modulus
        / (np.pi * disc_thickness * effective_radius)
    )
    return float(max_pressure)
