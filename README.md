# Optik

**An open-source optics and photonics desktop application built with Python and PySide6.**

Optik is a scientific desktop application designed to help students, educators, researchers, and engineers explore fundamental optics concepts through mathematical calculations and interactive visualization.

The project focuses on providing accessible tools for studying light behavior, optical systems, and photonics.

**Current Version:** v0.2.0 (In Development)  
**Latest Stable Release:** v0.1.0  
**Development Status:** Active Development  
**License:** MIT  
**Primary Language:** Python

---

## Overview

Optik combines fundamental optical calculations with a graphical interface and two-dimensional ray visualization.

The application currently focuses on geometrical optics, including reflection, refraction, critical angles, total internal reflection, and thin lens image formation.

Version 0.2.0 expands the application with thin lens calculations, magnification analysis, image classification, and an improved Matplotlib visualization system.

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

### Thin Lens Calculator (v0.2.0)

- Calculate image distance using the thin lens equation.
- Enter positive or negative focal lengths.
- Model converging and diverging thin lenses.
- Calculate image magnification and image height.
- Determine whether an image is upright or inverted.
- Classify image size as enlarged, reduced, or unchanged.
- Identify real and virtual image formation.
- Handle objects positioned at the focal point.
- Visualize principal optical rays and image formation.

### Scientific Visualization

- Two-dimensional optical ray diagrams.
- Matplotlib integration with PySide6.
- Surface normal and optical interface visualization.
- Thin lens and focal-point visualization.
- Dynamic diagram updates.
- Light and dark plotting themes.
- Navigation toolbar for Matplotlib figures.
- Figure export support for PNG, JPG, SVG, and PDF through the Plot Manager API.

### Desktop Interface

- Light and dark themes.
- Sidebar navigation.
- Home dashboard with calculator shortcuts.
- Dedicated Reflection, Refraction, and Thin Lens pages.
- Numerical input controls.
- Scrollable content areas.
- Persistent application settings and calculation defaults.
- Input validation and error handling.

## Technologies

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

Current geometrical optics calculations primarily use Python's standard mathematical functions.

NumPy and SciPy are intended to support increasingly advanced numerical calculations in future releases.

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

### Thin Lens Optics

1. Open the **Thin Lens** page from the sidebar or Home dashboard.
2. Enter the focal length in centimeters.
3. Enter the object distance in centimeters.
4. Enter the object height in centimeters.
5. Click **Calculate Lens**.
6. Review the image properties and ray diagram.

The thin lens equation is:

**1/f = 1/dₒ + 1/dᵢ**

Where:

- **f** — Focal length
- **dₒ** — Object distance
- **dᵢ** — Image distance

A positive focal length represents a converging lens, while a negative focal length represents a diverging lens.

For the real-object convention used by Optik, a positive image distance indicates a real image, while a negative image distance indicates a virtual image.

### Magnification

Optik calculates signed magnification using:

**m = −dᵢ / dₒ**

The image height is calculated using:

**hᵢ = m × hₒ**

Where:

- **m** — Magnification
- **hᵢ** — Image height
- **hₒ** — Object height

Negative magnification indicates an inverted image, while positive magnification indicates an upright image.

The magnitude of magnification determines whether an image is enlarged, reduced, or the same size as the object.

When the object is positioned at the focal point of a converging lens, the ideal thin lens model places the image at infinity.

## Project Structure

```text
Optik/
├── main.py
├── app/
│   ├── main_window.py
│   └── config.py
├── ui/
│   ├── pages/
│   │   ├── home_page.py
│   │   ├── reflection_page.py
│   │   ├── refraction_page.py
│   │   ├── lens_page.py
│   │   └── settings_page.py
│   ├── widgets/
│   │   └── sidebar.py
│   └── styles/
├── optics/
│   ├── reflection.py
│   ├── refraction.py
│   ├── snells_law.py
│   ├── total_internal_reflection.py
│   ├── thin_lens.py
│   └── magnification.py
├── visualization/
│   ├── ray_diagram.py
│   ├── lens_diagram.py
│   └── plot_manager.py
├── utils/
├── tests/
├── docs/
│   ├── SRS.md
│   ├── SDD.md
│   ├── USER_GUIDE.md
│   └── DEVELOPMENT.md
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

Run specific test modules:

```bash
python -m pytest tests/test_thin_lens.py -v
python -m pytest tests/test_magnification.py -v
python -m pytest tests/test_lens_diagram.py -v
python -m pytest tests/test_plot_manager.py -v
python -m pytest tests/test_main_window.py -v
```

The test suite covers:

- Reflection and refraction calculations
- Snell's law
- Critical-angle calculations
- Total internal reflection
- Thin lens calculations
- Magnification and image classification
- Input validation and error handling
- GUI initialization
- Main window navigation
- Matplotlib figure management
- Optical ray visualization
- Figure export

GUI integration testing for the Thin Lens page is part of the v0.2.0 release verification.

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

### v0.2.0 — Thin Lens Optics (In Development)

- Thin lens equation calculations
- Converging and diverging lenses
- Magnification calculations
- Image height and orientation
- Image classification
- Principal ray diagrams
- Reusable Plot Manager
- Updated Home dashboard and navigation
- Expanded automated testing
- Documentation updates

### Planned Future Releases

| Version | Development Focus |
|---|---|
| v0.3.0 | Mirrors and image formation |
| v0.4.0 | Multiple lenses and optical systems |
| v0.5.0 | Wave optics |
| v0.6.0 | Interference and diffraction |
| v0.7.0 | Polarization |
| v0.8.0 | Optical materials and dispersion |
| v0.9.0 | Numerical and Fourier optics |
| v1.0.0 | Integration, validation, documentation, and stable release |

Future features and release schedules are subject to change.

## Contributing

Contributions, suggestions, and bug reports are welcome.

Developers interested in contributing should review `CONTRIBUTING.md` and `docs/DEVELOPMENT.md`.

## Known Limitations

Optik currently focuses on idealized geometrical optics.

The thin lens calculations assume ideal lenses and use the paraxial approximation.

The application does not currently simulate:

- Diffraction
- Interference
- Polarization-dependent effects
- Optical power transmission
- Absorption
- Lens aberrations
- Complex multi-element optical systems

The diagrams illustrate ray geometry rather than full electromagnetic wave behavior.

## License

Optik is licensed under the MIT License.