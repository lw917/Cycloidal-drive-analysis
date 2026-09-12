"""Main entry point for running cycloidal drive computational analysis and performance profiler."""

import time
import matplotlib.pyplot as plt
import numpy as np
from src.geometry import generate_cycloid_profile
from src.hertzian import hertzian_contact_stress
from src.kinematics import compute_pin_forces_baseline, compute_pin_forces_proposed


def run_full_analysis() -> None:
    """Executes geometry generation, contact mechanics calculations, timing benchmarks, and plot generation."""
    print("--- MMA3001 Cycloidal Drive Computational Analysis ---")

    # Gear Parameters (30:1 Reduction Ratio)
    num_teeth = 30
    pitch_r = 0.053  # 53 mm pitch radius
    pin_r = 0.0015  # 3 mm pin diameter
    ecc = 0.00075  # 0.75 mm eccentricity
    torque = 1.2  # 1.2 N*m torque load
    disc_thickness = 0.004  # 4 mm disc thickness

    # 1. Geometry Generation
    x, y = generate_cycloid_profile(pitch_r, pin_r, ecc, num_teeth)

    # 2. Timing Benchmarks: Proposed (1D Root-Find) vs Baseline (Uniform)
    t0 = time.perf_counter()
    forces_proposed = compute_pin_forces_proposed(
        torque, num_teeth, pitch_r, ecc
    )
    t_proposed = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    forces_baseline = compute_pin_forces_baseline(torque, num_teeth, pitch_r)
    t_baseline = (time.perf_counter() - t0) * 1000

    # 3. Hertzian Stress Validation
    max_force_prop = np.max(forces_proposed)
    peak_stress = hertzian_contact_stress(
        max_force_prop, disc_thickness, 0.015, pin_r
    )

    print(
        f"Proposed Non-Linear Solver Execution Time: {t_proposed:.4f} ms"
    )
    print(
        f"Baseline Uniform Solver Execution Time:    {t_baseline:.4f} ms"
    )
    print(f"Peak Pin Force (Proposed):                  {max_force_prop:.2f} N")
    print(
        f"Peak Hertzian Contact Stress:              {peak_stress / 1e6:.2f} MPa"
    )

    # 4. Results Visualization Plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    ax1.plot(x * 1000, y * 1000, "b-", label="30:1 Cycloid Rotor Disc")
    ax1.set_title("Generated Profile Geometry")
    ax1.set_xlabel("X (mm)")
    ax1.set_ylabel("Y (mm)")
    ax1.axis("equal")
    ax1.grid(True)
    ax1.legend()

    pins = np.arange(num_teeth + 1)
    ax2.bar(
        pins - 0.2,
        forces_proposed,
        width=0.4,
        label="Proposed (1D Root-Find)",
        color="navy",
    )
    ax2.bar(
        pins + 0.2,
        forces_baseline,
        width=0.4,
        label="Baseline (Uniform)",
        color="orange",
    )
    ax2.set_title("Pin Force Distribution (1.2 N·m Input Torque)")
    ax2.set_xlabel("Pin Index")
    ax2.set_ylabel("Normal Force (N)")
    ax2.grid(True)
    ax2.legend()

    plt.tight_layout()
    plt.savefig("analysis_results.png")
    plt.show()


if __name__ == "__main__":
    run_full_analysis()
