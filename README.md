# 30:1 Cycloidal-drive-analysis
Computational modeling, parametric rotor disc geometry generation, pin force distribution kinematics, and Hertzian contact stress analysis for a 30:1 reduction ratio cycloidal drive.

# Project Overview
This repository provides an automated computational engineering workdlow for analyzing a 30:1 single-stage cycloidal gearbox disc
- Parametric Profile Generation: Generates undercut-free epitrochoid rotor disc geometry

- Kinematics & Contact Mechanics: Models non-linear load distribution across active contact housing pins using 1D root-finding ('brentq') and compares it against a uniform load baseline model

- Hertzian Stress Calculator: Calculates peak line contact stress across rotor lobes and housing pins

## Technical Specifications
- Reduction Ratio: 30:1, 30 rotor teeth, 31 housing pins
- Pin Circle Diameter : 53mm (pitch circle radius: 26.5mm)
- Eccentricity: 0.75mm (shaft offset distance)
- Input Torque: 1.2Nm (applied operating torque load)
- Disc Thickness: 4mm (rotor thickness)

## Repository Structure
```text
Cycloidal-drive-analysis/
├── docs/                      # Auto-generated HTML API documentation (pdoc)
├── src/                       # Core analytical source code
│   ├── __init__.py
│   ├── geometry.py            # Profile coordinate parametric equations
│   ├── kinematics.py          # 1D root-finder & pin force distribution solvers
│   └── hertzian.py            # Closed-form Hertzian line contact stress calculation
├── tests/                     # Automated unit test suite
│   ├── test_geometry.py       # Geometry bounds and undercutting assertions
│   └── test_kinematics.py     # Solver convergence & force output verification
├── analysis_results.png       # Generated rotor profile & pin force comparison plot
├── conftest.py                # Pytest configuration file
├── README.md                  # Project overview and instructions
├── requirements.txt           # Python dependency requirements
└── run_analysis.py            # Main entry point and performance profiler
```