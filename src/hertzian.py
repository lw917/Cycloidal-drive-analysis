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

    if normal_force <= 0:
        return 0.0

    e_effective = e_modulus / (2 * (1 - poison_ratio ** 2))

    r_effective = 1 / ((1 / radius_cycloid) + (1 / radius_pin))

    max_stress = np.sqrt((normal_force + e_effective) / (np.pi * disc_thickness * r_effective))

    return float(max_stress)
