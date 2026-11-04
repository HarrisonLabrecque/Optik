# Optik — Development Guide

**Version:** 0.2.0  
**Project:** Optik  
**Language:** Python  
**GUI Framework:** PySide6  
**License:** MIT  
**Development Status:** v0.2.0 Release Candidate

---

## 1. Introduction

Optik is an open-source desktop application for optics and photonics calculations and visualization.

The application is developed using Python and PySide6, with Matplotlib providing graphical representations of optical ray behavior and image formation.

Version 0.2.0 extends the original geometrical optics functionality with thin lens calculations, magnification, image classification, and reusable plotting components.

This guide describes the development environment, project structure, architecture, testing procedures, and contribution workflow.

## 2. Development Environment

### 2.1 Recommended Tools

- Python 3.14 or a compatible Python 3 version
- Visual Studio Code or another Python-compatible IDE
- Git
- GitHub
- Windows PowerShell or another supported terminal

Windows is the primary development environment.

### 2.2 Python Dependencies

| Package | Purpose |
|---|---|
| PySide6 | Desktop graphical interface |
| NumPy | Numerical computation |
| SciPy | Scientific computing |
| Matplotlib | Optical ray visualization |
| pytest | Automated testing |
| pytest-qt | Qt GUI testing |

The geometrical optics calculation modules primarily use Python's built-in `math` library.

## 3. Setting Up the Development Environment

### 3.1 Clone the Repository

```bash
git clone <repository-url>
cd Optik
```

Replace `<repository-url>` with the actual Optik repository address.

### 3.2 Create a Virtual Environment

```powershell
python -m venv .venv
```

### 3.3 Activate the Environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### 3.4 Install Dependencies

```bash
python -m pip install -r requirements.txt
```

Install testing dependencies if they are not already included:

```bash
python -m pip install pytest pytest-qt
```

### 3.5 Launch the Application

```bash
python main.py
```

The Optik desktop interface should open.

## 4. Project Architecture

Optik follows a modular architecture that separates optical calculations, scientific visualization, and graphical interface components.

```text
Optik/
│
├── main.py
├── pyproject.toml
├── requirements.txt
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
│
├── app/
│   ├── __init__.py
│   ├── main_window.py
│   └── config.py
│
├── ui/
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── home_page.py
│   │   ├── reflection_page.py
│   │   ├── refraction_page.py
│   │   ├── lens_page.py
│   │   └── settings_page.py
│   │
│   ├── widgets/
│   │   ├── __init__.py
│   │   ├── sidebar.py
│   │   ├── metric_card.py
│   │   └── input_panel.py
│   │
│   └── styles/
│       ├── main.qss
│       ├── light.qss
│       └── dark.qss
│
├── optics/
│   ├── __init__.py
│   ├── reflection.py
│   ├── refraction.py
│   ├── snells_law.py
│   ├── total_internal_reflection.py
│   ├── thin_lens.py
│   └── magnification.py
│
├── visualization/
│   ├── __init__.py
│   ├── ray_diagram.py
│   ├── lens_diagram.py
│   └── plot_manager.py
│
├── utils/
│   ├── __init__.py
│   ├── validators.py
│   └── constants.py
│
├── tests/
│   ├── __init__.py
│   ├── test_reflection.py
│   ├── test_refraction.py
│   ├── test_snells_law.py
│   ├── test_total_internal_reflection.py
│   ├── test_main_window.py
│   ├── test_reflection_page.py
│   ├── test_refraction_page.py
│   ├── test_ray_diagram.py
│   ├── test_thin_lens.py
│   ├── test_magnification.py
│   ├── test_lens_diagram.py
│   └── test_plot_manager.py
│
└── docs/
    ├── SRS.md
    ├── SDD.md
    ├── USER_GUIDE.md
    └── DEVELOPMENT.md
```

Some files may be placeholders or require further implementation and verification.

## 5. Application Components

### 5.1 Application Entry Point

**File:** `main.py`

Responsibilities:

- Initialize `QApplication`.
- Configure application metadata.
- Load the application stylesheet.
- Initialize the main window.
- Start the Qt event loop.

### 5.2 Main Window

**File:** `app/main_window.py`

The `MainWindow` class manages the main application interface.

Responsibilities:

- Initialize application pages.
- Manage sidebar navigation.
- Switch between pages.
- Connect Home dashboard shortcuts.
- Apply Light and Dark themes.
- Coordinate persistent application settings.

The implementation uses `QMainWindow` and `QStackedWidget`.

The v0.2.0 navigation structure contains five pages:

| Index | Page |
|---|---|
| 0 | Home |
| 1 | Reflection |
| 2 | Refraction |
| 3 | Thin Lens |
| 4 | Settings |

### 5.3 User Interface Pages

**Directory:** `ui/pages/`

**Home Page — `home_page.py`**

Provides the application's landing interface and shortcuts to optical calculators.

**Reflection Page — `reflection_page.py`**

Accepts incident angles, calculates reflected angles, and displays optical ray diagrams.

**Refraction Page — `refraction_page.py`**

Calculates refracted angles, critical angles, and total internal reflection conditions.

**Thin Lens Page — `lens_page.py`**

Provides the thin lens calculator introduced in v0.2.0.

Responsibilities:

- Accept focal length, object distance, and object height.
- Calculate image distance.
- Calculate magnification and image height.
- Display image orientation and size classification.
- Identify lens type.
- Generate and display lens ray diagrams.
- Maintain calculation defaults using `QSettings`.
- Apply the current plotting theme.

**Settings Page — `settings_page.py`**

Provides application preferences, including appearance settings.

### 5.4 Optical Calculation Modules

**Directory:** `optics/`

Calculation modules are independent of the graphical interface.

| Module | Responsibility |
|---|---|
| `reflection.py` | Law of reflection |
| `refraction.py` | Refraction calculations |
| `snells_law.py` | Snell's law |
| `total_internal_reflection.py` | Critical angles and total internal reflection |
| `thin_lens.py` | Thin lens image distance calculations |
| `magnification.py` | Magnification, image height, and image properties |

#### Thin Lens Equation

The ideal thin lens equation is:

**1/f = 1/dₒ + 1/dᵢ**

Where:

- `f` represents focal length.
- `dₒ` represents object distance.
- `dᵢ` represents image distance.

Under the application's real-object sign convention:

- Positive focal length represents a converging lens.
- Negative focal length represents a diverging lens.
- Positive image distance represents a real image.
- Negative image distance represents a virtual image.

An object at the focal point of a converging lens produces an image at infinity in the idealized model.

#### Magnification

Signed magnification is calculated using:

**m = −dᵢ / dₒ**

Image height is calculated using:

**hᵢ = m × hₒ**

The sign of magnification determines image orientation, while its absolute value determines relative image size.

### 5.5 Visualization Modules

**Directory:** `visualization/`

**Ray Diagram — `ray_diagram.py`**

Provides the reflection and refraction diagrams introduced in v0.1.0.

**Lens Diagram — `lens_diagram.py`**

Generates thin lens diagrams with principal rays, focal points, the optical axis, and object/image representations.

**Plot Manager — `plot_manager.py`**

Provides a reusable Matplotlib widget for PySide6 pages.

Features include:

- Embedded Matplotlib canvas.
- Navigation toolbar.
- Figure and axes management.
- Light and dark plotting themes.
- Plot refreshing and clearing.
- Line and scatter plotting utilities.
- Integration with existing diagram objects.
- Figure export to PNG, JPG, JPEG, SVG, and PDF.

The Plot Manager handles replacement of the canvas and toolbar when a different Matplotlib figure is loaded.

### 5.6 Shared UI Components

**Directory:** `ui/widgets/`

Reusable widgets support consistent interface behavior.

Examples include:

- `Sidebar`
- `MetricCard`
- `InputPanel`

Shared components should remain independent of individual optical calculation modules wherever practical.

### 5.7 Utilities

**Directory:** `utils/`

Utility modules provide shared validation, constants, and supporting functions.

Avoid duplicating common validation logic across calculation modules.

## 6. Development Principles

Optik follows these principles:

1. Separate optical physics from the graphical interface.
2. Keep numerical calculation functions independently testable.
3. Use reusable visualization components.
4. Validate numerical inputs and handle exceptional conditions.
5. Keep application navigation and appearance consistent.
6. Preserve existing functionality when adding new features.
7. Document new modules and changes.
8. Write automated tests for calculations and GUI behavior.

## 7. Testing

Optik uses pytest and pytest-qt.

### 7.1 Run the Complete Test Suite

```powershell
python -m pytest tests/ -v
```

### 7.2 Run Physics Tests

```powershell
python -m pytest tests/test_thin_lens.py -v
python -m pytest tests/test_magnification.py -v
```

### 7.3 Run Visualization Tests

```powershell
python -m pytest tests/test_lens_diagram.py -v
python -m pytest tests/test_plot_manager.py -v
```

### 7.4 Run Main Window Tests

```powershell
python -m pytest tests/test_main_window.py -v
```

### 7.5 GUI Testing

GUI tests should verify:

- Page initialization.
- Navigation between pages.
- Input controls.
- Calculation results.
- Error handling.
- Theme compatibility.
- Diagram updates.
- Persistent settings where applicable.

### 7.6 Numerical Boundary Conditions

Important thin lens test cases include:

- Converging lenses.
- Diverging lenses.
- Real image formation.
- Virtual image formation.
- Objects at the focal point.
- Objects inside the focal length.
- Magnification greater than one.
- Magnification less than one.
- Invalid or zero-valued inputs where prohibited.

### 7.7 Release Verification

Before publishing a version:

1. Run the complete automated test suite.
2. Perform manual GUI checks.
3. Verify navigation and theme switching.
4. Review the physics calculations and diagrams.
5. Update documentation.
6. Review Git changes.
7. Create the release commit and version tag.
8. Publish the release when ready.

## 8. Coding Standards

### 8.1 Python

- Follow PEP 8 conventions.
- Use descriptive function and variable names.
- Add type hints where appropriate.
- Write docstrings for public functions and classes.
- Prefer small, focused functions.
- Keep physics logic separate from GUI code.

### 8.2 Error Handling

- Validate inputs before performing calculations.
- Raise appropriate exceptions for invalid calculation inputs.
- Handle exceptional mathematical conditions explicitly.
- Display understandable error messages in the GUI.

### 8.3 Scientific Accuracy

- Document mathematical equations and assumptions.
- Use consistent sign conventions.
- Distinguish physical results from visualization approximations.
- Include boundary-condition tests.
- Avoid presenting idealized diagrams as full physical simulations.

## 9. Git and Version Control

Git is used to track Optik development.

### 9.1 Check Repository Status

```bash
git status
```

### 9.2 Create a Development Branch

Example:

```bash
git switch -c version-0.2
```

Create the branch only if it does not already exist.

### 9.3 Stage Changes

```bash
git add .
```

### 9.4 Commit Changes

```bash
git commit -m "docs: update Optik documentation for v0.2.0"
```

### 9.5 Push Changes

```bash
git push -u origin version-0.2
```

Use the branch that contains the current development work.

### 9.6 Version Tags

After release verification, create an annotated version tag:

```bash
git tag -a v0.2.0 -m "Optik v0.2.0 - Thin Lens Optics"
```

Push the tag:

```bash
git push origin v0.2.0
```

Do not create the final release tag until the version is ready for publication.

## 10. Contribution Workflow

Contributors should:

1. Review the README and contribution guidelines.
2. Create a feature or bug-fix branch.
3. Implement changes using the modular architecture.
4. Add or update relevant tests.
5. Run the test suite.
6. Update affected documentation.
7. Submit a pull request describing the changes.

For additional information, see `CONTRIBUTING.md`.

## 11. Version Development

### v0.1.0 — Initial Geometrical Optics

- Reflection.
- Refraction.
- Snell's law.
- Critical angles.
- Total internal reflection.
- Basic ray diagrams.
- Desktop application framework.

### v0.2.0 — Thin Lens Optics

- Thin lens calculations.
- Converging and diverging lenses.
- Magnification.
- Image classification.
- Lens ray diagrams.
- Reusable Plot Manager.
- Expanded navigation.
- Additional automated tests.

### v0.3.0 — Planned Mirror Optics

- Concave mirrors.
- Convex mirrors.
- Mirror equation calculations.
- Mirror magnification.
- Mirror ray diagrams.
- GUI integration and testing.

## 12. Known Development Limitations

Optik currently uses idealized geometrical optics models.

The thin lens calculations assume ideal thin lenses and paraxial rays.

Current limitations include:

- No diffraction simulation.
- No interference simulation.
- No polarization modeling.
- No optical aberration calculations.
- No advanced multi-element optical system modeling.
- No complete electromagnetic wave simulation.

Future versions may address these limitations.

## 13. License

Optik is distributed under the MIT License.

Refer to the repository's `LICENSE` file for the complete license terms.