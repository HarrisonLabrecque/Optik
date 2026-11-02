# Optik

**An open-source optics and photonics desktop application built with Python and PySide6.**

Optik is a scientific desktop application designed to help students, educators, researchers, and engineers explore fundamental optics concepts through mathematical calculations and interactive visualization.

The project focuses on providing accessible tools for studying light behavior, optical systems, and photonics.

**Current Version:** 0.1.0 Release Candidate  
**Development Status:** Active Development  
**License:** MIT  
**Primary Language:** Python  

---

## Overview

Optik combines fundamental optical calculations with a graphical interface and two-dimensional ray visualization.

The initial version focuses on geometrical optics, including reflection, refraction, critical angles, and total internal reflection.

Future releases aim to expand Optik into a broader optics and photonics reference and simulation application.

## Features

### Reflection Calculator

- Calculate reflected angles.
- Apply the law of reflection.
- Visualize incident and reflected rays.
- Adjust incident angles interactively.

### Refraction Calculator

- Calculate refracted angles using Snell's law.
- Enter custom refractive indices.
- Calculate critical angles.
- Detect total internal reflection.
- Visualize incident, reflected, and refracted rays.

### Scientific Visualization

- Two-dimensional optical ray diagrams.
- Matplotlib integration.
- Surface normal visualization.
- Optical interface representation.
- Dynamic diagram updates.

### Desktop Interface

- Modern dark-themed interface.
- Sidebar navigation.
- Dedicated calculator pages.
- Numerical input controls.
- Scrollable content areas.
- Input validation and error handling.

## Technologies

Optik is developed using:

| Technology | Purpose |
|---|---|
| Python | Application development |
| PySide6 | Desktop GUI |
| Matplotlib | Scientific visualization |
| NumPy | Numerical computing |
| SciPy | Scientific computing |
| pytest | Unit testing |
| pytest-qt | GUI testing |
| Git | Version control |

The initial optics calculations primarily use Python's standard mathematical functions.

## Installation

### Requirements

- Compatible Python 3 installation
- Git (optional)
- Supported desktop operating system

Windows is the primary development environment.

### Clone the Repository

```bash
git clone <repository-url>
cd Optik
```

Replace `<repository-url>` with the official repository address.

### Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the environment on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

On Linux/macOS:

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Run Optik

```bash
python main.py
```

The application will launch its graphical interface.

## Using Optik

### Reflection

1. Open the Reflection page.
2. Enter an incident angle.
3. Click **Calculate Reflection**.
4. Review the reflected angle and ray diagram.

The law of reflection states:

**θᵣ = θᵢ**

### Refraction

1. Open the Refraction page.
2. Enter the refractive indices of both media.
3. Enter the incident angle.
4. Click **Calculate Refraction**.
5. Review the results and ray visualization.

The calculation uses Snell's law:

**n₁ sin(θ₁) = n₂ sin(θ₂)**

### Total Internal Reflection

When light travels from a medium with a higher refractive index to one with a lower refractive index, total internal reflection may occur.

Optik calculates the critical angle and identifies when the incident angle exceeds it.

## Project Structure

```text
Optik/
├── main.py
├── app/
├── ui/
│   ├── pages/
│   ├── widgets/
│   └── styles/
├── optics/
├── visualization/
├── utils/
├── tests/
├── docs/
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── pyproject.toml
└── requirements.txt
```

## Testing

Optik uses pytest and pytest-qt for automated testing.

Run the complete test suite:

```bash
python -m pytest tests/ -v
```

The test suite covers:

- Optical physics calculations
- Input validation
- Critical-angle calculations
- Total internal reflection
- GUI initialization
- Calculator interactions
- Main window navigation
- Optical ray visualization

## Documentation

Additional project documentation is available in the `docs/` directory.

| Document | Description |
|---|---|
| `docs/SRS.md` | Software Requirements Specification |
| `docs/SDD.md` | Software Design Document |
| `docs/USER_GUIDE.md` | User instructions |
| `docs/DEVELOPMENT.md` | Developer documentation |
| `CHANGELOG.md` | Version history |
| `CONTRIBUTING.md` | Contribution guidelines |
| `LICENSE` | MIT License |

## Roadmap

### v0.1.0 — Initial Release

- Application framework
- Sidebar navigation
- Reflection calculator
- Refraction calculator
- Critical-angle calculations
- Total internal reflection detection
- Two-dimensional ray visualization
- Automated testing
- Project documentation

### Future Releases

Planned development areas include:

- Lens and mirror calculations
- Optical materials
- Wave optics
- Polarization
- Diffraction and interference
- Optical system visualization
- Advanced numerical simulations

Future features and release schedules are subject to change.

## Contributing

Contributions, suggestions, and bug reports are welcome.

Developers interested in contributing should review `CONTRIBUTING.md` and `docs/DEVELOPMENT.md`.

## Known Limitations

Optik v0.1.0 focuses on idealized geometrical optics.

It does not currently simulate:

- Diffraction
- Interference
- Polarization-dependent effects
- Optical power transmission
- Absorption
- Complex optical systems

The diagrams illustrate ray geometry rather than full electromagnetic wave behavior.

## License

Optik is licensed under the MIT License.
