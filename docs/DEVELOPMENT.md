# Optik — Development Guide

**Project:** Optik — Open-Source Optics & Photonics Desktop Application  
**Current Development Version:** v0.4.0  
**Document Status:** Maintained  
**Programming Language:** Python  
**GUI Framework:** PySide6  
**License:** MIT

---

## 1. Introduction

### 1.1 Purpose

This document describes the development practices, project organization, testing procedures, version control workflow, and release preparation process for Optik.

Optik is an open-source scientific desktop application for performing optical calculations and generating scientific visualizations. This guide is intended for maintainers and contributors.

### 1.2 Development Objectives

- Maintain a modular software architecture.
- Separate scientific calculations from GUI components.
- Develop and test features incrementally.
- Preserve existing functionality where practical.
- Maintain readable, maintainable Python code.
- Use automated tests to detect regressions.
- Document changes for each software release.
- Support public open-source development.

### 1.3 Development Philosophy

Optik follows an incremental, version-based workflow:

1. Define requirements.
2. Design scientific calculation modules.
3. Implement mathematical calculations.
4. Write and run unit tests.
5. Implement scientific visualizations.
6. Write visualization tests.
7. Implement GUI components.
8. Write GUI tests.
9. Integrate features into the main application.
10. Run regression tests.
11. Perform manual verification.
12. Update documentation.
13. Prepare and publish the release.

---

## 2. Development Environment

### 2.1 Required Software

| Tool | Purpose |
|---|---|
| Python | Application development |
| PySide6 | Desktop GUI |
| NumPy | Numerical operations |
| SciPy | Scientific computing |
| Matplotlib | Optical visualization |
| pytest | Unit testing |
| pytest-qt | GUI testing |
| Git | Version control |
| GitHub | Repository hosting |
| PyInstaller | Windows executable packaging, when applicable |

### 2.2 Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Optik.git
cd Optik
```

Replace `YOUR_USERNAME` with the repository owner's GitHub username.

### 2.3 Create a Virtual Environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2.4 Install Dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If testing dependencies are not included:

```bash
python -m pip install pytest pytest-qt
```

### 2.5 Launch the Application

The v0.4.0 main window is maintained in `ui/main_window.py`. If it is configured as the executable module, launch with:

```bash
python -m ui.main_window
```

If the repository uses a separate entry-point script, launch that script instead. Confirm the actual entry point before publishing installation instructions.

---

## 3. Project Organization

The following is the principal source layout for v0.4.0; exact test filenames and optional supporting files may differ.

```text
Optik/
├── app/                         # Optional application bootstrap/compatibility code
├── optics/
│   ├── reflection.py
│   ├── refraction.py
│   ├── thin_lens.py
│   ├── magnification.py
│   ├── mirrors.py
│   ├── mirror_magnification.py
│   ├── prisms.py
│   └── dispersion.py
├── visualization/
│   ├── reflection_diagram.py
│   ├── refraction_diagram.py
│   ├── lens_diagram.py
│   ├── mirror_diagram.py
│   └── dispersion_diagram.py
├── ui/
│   ├── main_window.py
│   ├── pages/
│   │   ├── home_page.py
│   │   ├── reflection_page.py
│   │   ├── refraction_page.py
│   │   ├── lens_page.py
│   │   ├── mirror_page.py
│   │   ├── prism_page.py
│   │   └── settings_page.py
│   └── widgets/                 # Reusable GUI and plotting components
├── tests/
│   ├── test_main_window.py
│   ├── test_mirrors.py
│   ├── test_mirror_magnification.py
│   ├── test_mirror_diagram.py
│   ├── test_mirror_page.py
│   └── ...                      # Other calculation, visualization, and GUI tests
├── docs/
│   ├── SRS.md
│   ├── SDD.md
│   ├── USER_GUIDE.md
│   ├── DEVELOPMENT.md
│   └── screenshots/
├── README.md
├── CHANGELOG.md
├── LICENSE
└── requirements.txt
```

### 3.1 `app/` and Main Window

Application bootstrap code may reside in `app/`. The v0.4.0 `MainWindow` implementation is in `ui/main_window.py`; it coordinates pages, sidebar navigation, theme changes, and application startup.

### 3.2 `optics/`

Contains mathematical models and scientific calculations. These modules should not depend on PySide6 widgets. In v0.4.0, `prisms.py` and `dispersion.py` provide prism geometry and wavelength-dependent refractive index calculations.

### 3.3 `visualization/`

Contains Matplotlib scientific diagrams and graphs. Visualization should consume scientific results rather than unnecessarily duplicate calculation logic. `dispersion_diagram.py` supports prism and spectral visualizations.

### 3.4 `ui/`

Contains GUI pages, reusable widgets, user interaction logic, and the current main window.

### 3.5 `tests/`

Contains automated tests for calculations, diagrams, and GUI behavior.

### 3.6 `docs/`

Contains requirements, design, user instructions, and development procedures.

---

## 4. Coding Standards

### 4.1 Python Style

Follow PEP 8 where practical. Use four-space indentation, descriptive names, type hints, docstrings, focused functions, minimal duplication, and clear exception handling.

### 4.2 Naming Conventions

| Element | Convention | Example |
|---|---|---|
| Modules | snake_case | `mirror_magnification.py` |
| Functions | snake_case | `calculate_spectral_dispersion()` |
| Variables | snake_case | `object_distance` |
| Classes | PascalCase | `MirrorDiagram` |
| Constants | UPPER_SNAKE_CASE | `DEFAULT_FOCAL_LENGTH` |
| Test files | `test_` prefix | `test_mirrors.py` |

### 4.3 Mathematical Function Design

1. Accept clearly defined inputs.
2. Validate unsupported values.
3. Apply documented equations and units.
4. Return predictable results.
5. Raise meaningful exceptions for invalid calculations.

### 4.4 Data Structures

Use structured result objects for related outputs. Immutable dataclasses are suitable for scientific results:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class OpticalResult:
    focal_length: float
    object_distance: float
    image_distance: float
```

The v0.4.0 dispersion module also uses structured coefficient and result types, including `CauchyCoefficients`, `DispersionResult`, and `SpectralPrismResult`.

### 4.5 Error Handling

Handle division by zero, non-finite values, invalid refractive indices, unsupported configurations, invalid distances, and prism conditions that prevent transmission. Do not silently return misleading numerical results.

### 4.6 GUI Development

GUI pages should separate layout and calculations, use signals and slots, validate input, display readable results, and support application themes.

---

## 5. Scientific Calculation Development

### 5.1 Implementation Workflow

1. Identify governing equations.
2. Document sign conventions and units.
3. Determine valid input ranges.
4. Identify special cases.
5. Implement calculation functions.
6. Create automated unit tests.
7. Compare results with known numerical examples.
8. Integrate into the GUI.

### 5.2 Numerical Accuracy

Use floating-point tolerances where appropriate:

```python
import pytest

def test_example_calculation():
    result = 15.0
    assert result == pytest.approx(15.0)
```

### 5.3 Sign Conventions

Each model must document its conventions. For spherical mirrors, positive focal length denotes concave mirrors, negative focal length denotes convex mirrors, positive image distance denotes real images, and negative image distance denotes virtual images.

### 5.4 Special Cases

Consider images at infinity, total internal reflection, undefined magnification, invalid denominators, non-finite inputs, and prism configurations that do not yield an emergent ray.

### 5.5 Wavelength-Dependent Models (v0.4.0)

Document wavelength units explicitly. Cauchy's equation is:

\[
n(\lambda)=A+\frac{B}{\lambda^2}+\frac{C}{\lambda^4}
\]

Here `λ` is in **micrometers**, even if the user interface accepts wavelengths in nanometers. Convert units at the calculation boundary and validate the coefficient range and resulting refractive indices. Cauchy coefficients are empirical and should only be used within their fitted wavelength range.

---

## 6. Visualization Development

### 6.1 Matplotlib

Visualization modules manage figure creation, optical axes, object/image positions, reference points, ray geometry, labels, clearing, and supported exports.

### 6.2 Visualization Testing

Verify successful figure creation, expected elements, model-consistent geometry, special-case handling, and exports where implemented. For dispersion graphs, ensure wavelength and refractive-index/deviation arrays remain aligned when non-transmitting wavelengths are excluded.

### 6.3 GUI Integration

Matplotlib can be embedded using:

```python
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
```

A navigation toolbar may be included. Reuse the shared plotting canvas and update its styling when the application theme changes.

### 6.4 Prism Visualization Modes (v0.4.0)

The Prism page provides:

1. Prism Ray Diagram.
2. Refractive Index vs Wavelength.
3. Prism Deviation vs Wavelength.
4. Visible Spectrum.

The page should refresh the selected visualization after calculation and support PNG, SVG, and PDF export where implemented.

---

## 7. Testing Standards

### 7.1 Testing Frameworks

- `pytest` for calculations and application logic.
- `pytest-qt` for GUI tests.
- Matplotlib-compatible tests for diagrams.

### 7.2 Run All Tests

```bash
python -m pytest tests/ -v
```

### 7.3 Run a Specific Test File

```bash
python -m pytest tests/test_mirrors.py -v
```

### 7.4 Run Tests Quietly

```bash
python -m pytest tests/ -q
```

### 7.5 Test Discovery

```bash
python -m pytest --collect-only -q
```

### 7.6 Unit Test Coverage

Cover ordinary numerical cases, boundaries, invalid inputs, special cases, and classifications. Prism/dispersion tests should additionally cover Snell refraction at both faces, deviation, minimum deviation, total internal reflection, Cauchy indices, wavelength conversion, and spectral filtering.

### 7.7 GUI Test Coverage

Cover widget initialization, default values, buttons, results, navigation, settings, and theme behavior. Verify that the seven navigation shortcuts select the intended pages.

### 7.8 Regression Testing

Run the complete suite after significant changes. A passing suite is required before release; **a final v0.4.0 full-suite result has not yet been recorded in this guide**.

### 7.9 Manual GUI Verification

Before publishing, verify startup, sidebar and Home navigation, calculations, diagrams, theme switching, settings persistence, export, and error handling. In v0.4.0, verify **Home opens on every startup** even after closing on another page, while the selected theme persists.

---

## 8. Git and GitHub Workflow

### 8.1 Branching Strategy

Version-specific branches may be used:

```text
main
version-0.1
version-0.2
version-0.3
version-0.4
```

`main` should represent the intended stable project state.

### 8.2 Create a Development Branch

If the branch does not already exist:

```bash
git switch -c version-0.4
```

### 8.3 Check Repository Status

```bash
git status
```

### 8.4 Stage Changes

```bash
git add .
git diff --cached
```

### 8.5 Commit Changes

Use descriptive commit messages:

```bash
git commit -m "feat: add prism optics and dispersion"
git commit -m "test: update main window navigation tests"
git commit -m "docs: update v0.4.0 project documentation"
```

### 8.6 Push Changes

```bash
git push -u origin version-0.4
```

### 8.7 Commit Message Conventions

| Prefix | Purpose |
|---|---|
| feat | New functionality |
| fix | Bug correction |
| test | Test changes |
| docs | Documentation |
| refactor | Code restructuring |
| chore | Maintenance |
| build | Packaging and build changes |

### 8.8 Version Tags

Create an annotated tag only after validation and commit:

```bash
git tag -a v0.4.0 -m "Optik v0.4.0 - Prism Optics and Dispersion"
git push origin v0.4.0
```

Do not repeat tag creation if the tag already exists. A completed development milestone is not, by itself, confirmation of publication.

---

## 9. Release Preparation

### 9.1 Release Checklist

Before publishing a new version:

- [ ] Complete planned functionality.
- [ ] Verify mathematical calculations.
- [ ] Complete unit tests.
- [ ] Complete GUI tests.
- [ ] Complete visualization tests.
- [ ] Run and record the full regression suite.
- [ ] Perform manual GUI verification.
- [ ] Review error handling.
- [ ] Update application version labels.
- [ ] Update `README.md`.
- [ ] Update `CHANGELOG.md`.
- [ ] Update `docs/SRS.md`.
- [ ] Update `docs/SDD.md`.
- [ ] Update `docs/USER_GUIDE.md`.
- [ ] Update `docs/DEVELOPMENT.md`.
- [ ] Verify distribution packages, if applicable.
- [ ] Commit final changes.
- [ ] Merge or integrate the release branch.
- [ ] Create the Git version tag.
- [ ] Publish the GitHub release.

Check boxes should be marked only after the corresponding activity is confirmed.

### 9.2 Windows Packaging

PyInstaller may be used to create a Windows executable. For a repository whose executable entry point is `ui/main_window.py`, an example is:

```bash
python -m PyInstaller --noconfirm --windowed --name Optik ui/main_window.py
```

Confirm the script is runnable as a standalone entry point; use a dedicated launcher instead if needed. Packaging may require additional configuration for resources and dependencies. Test the resulting executable before distribution.

### 9.3 Release Notes

Summarize features, improvements, fixes, testing status, limitations, and installation considerations.

---

## 10. Version-Specific Development History

These sections preserve the development history of each release.

### 10.1 Version 0.1.0 — Initial Optics Release

**Status:** Completed

**Development Scope:** Establish the initial application architecture.

**Implemented Features:** Reflection and refraction calculations, critical angles, total internal reflection, ray diagrams, Home dashboard, sidebar navigation, Settings, and light/dark themes.

**Architecture:** Separated mathematical calculations, visualization components, GUI pages, and main application management.

**Testing:** Initial unit and GUI tests for reflection and refraction functionality.

**Development Outcome:** Established the foundation for future optical calculation modules.

---

### 10.2 Version 0.2.0 — Thin Lens Optics

**Status:** Development Completed

**Development Scope:** Extend the application to thin lens image formation and reusable visualization.

**Implemented Features:** Thin lens equation, converging/diverging lenses, magnification, image height/classification, ray diagrams, dedicated GUI page, and PlotManager.

**Architecture Changes:** Added thin lens and magnification calculation modules, extended visualization, and integrated the page into the main window and Home dashboard.

**Testing:** Thin lens, magnification, image classification, diagram, and GUI tests.

**Development Outcome:** Expanded Optik into optical image formation.

---

### 10.3 Version 0.3.0 — Mirror Optics

**Status:** Development Completed

**Development Scope:** Introduced spherical mirror calculations and ray diagrams.

**Implemented Features:** Concave/convex mirrors, image distance, radius of curvature, magnification, image height, image classifications, mirror diagrams, dedicated page, navigation, and persistent mirror inputs.

**New Scientific Modules:**

- `optics/mirrors.py` — spherical mirror equations, mirror classification, image distance, and radius of curvature.
- `optics/mirror_magnification.py` — magnification, image height, orientation, and size classification.

**New Visualization Module:** `visualization/mirror_diagram.py`, containing `MirrorDiagram` for concave and convex ray diagrams.

**New GUI Module:** `ui/pages/mirror_page.py`.

**Main Window Integration:** Expanded navigation to six pages and added the Mirror Optics Home feature card and keyboard navigation.

**Testing:** Developed `tests/test_mirrors.py`, `tests/test_mirror_magnification.py`, `tests/test_mirror_diagram.py`, and `tests/test_mirror_page.py`; updated magnification tests for supported conventions. The complete automated regression suite passed during v0.3.0 development.

**Release Preparation Record:** Manual GUI verification, Windows packaging (if applicable), and final publication details were not recorded in the original development notes. A v0.3.0 Git tag was previously created; development completion should not be confused with a verified published release.

**Development Outcome:** Mirror calculation and GUI modules implemented and automated tests passed.

---

### 10.4 Version 0.4.0 — Prism Optics & Dispersion

**Status:** Development Completed

#### Development Scope

Extend geometrical optics with prism refraction, angular deviation, and wavelength-dependent dispersion, including scientific graphs and an integrated Prism page.

#### Implemented Features

- Refraction at the entry and exit faces of a prism using Snell's law.
- Incident, internal refracted, emergent, and total deviation angles.
- Minimum deviation and critical-angle calculations.
- Total internal reflection and invalid-geometry handling.
- Cauchy dispersion with configurable coefficients.
- Wavelength-dependent refractive index and spectral prism deviation.
- Four visualization modes: Prism Ray Diagram, Refractive Index vs Wavelength, Prism Deviation vs Wavelength, and Visible Spectrum.
- Prism page input persistence and PNG/SVG/PDF plot export.
- Sidebar and Home dashboard integration with seven total pages.

#### New Scientific Modules

**`optics/prisms.py`** — prism ray geometry, refraction, angular deviation, minimum deviation, and total internal reflection conditions. The total deviation for a transmitting ray is:

\[
\delta=i+e-A_p
\]

where `i` is incidence angle, `e` is emergence angle, and `A_p` is prism apex angle.

**`optics/dispersion.py`** — Cauchy index calculations and wavelength-dependent spectral prism analysis:

\[
n(\lambda)=A+\frac{B}{\lambda^2}+\frac{C}{\lambda^4}
\]

`λ` is in micrometers. Key result structures include `CauchyCoefficients`, `DispersionResult`, and `SpectralPrismResult`. Non-transmitting wavelengths are omitted from spectral deviation results; a calculation error is raised when none produce valid transmission.

#### New Visualization Module

**`visualization/dispersion_diagram.py`** — prism ray diagrams, dispersion graphs, spectral deviation graphs, and visible-spectrum visualization using Matplotlib.

#### New GUI Component

**`ui/pages/prism_page.py`** — prism parameter inputs, calculation execution, results, plot-mode selection, export, and persistent supported inputs.

#### Main Window and Startup Changes

**`ui/main_window.py`** coordinates seven pages:

| Index | Page | Shortcut |
|---|---|---|
| 0 | Home | Ctrl+1 |
| 1 | Reflection | Ctrl+2 |
| 2 | Refraction | Ctrl+3 |
| 3 | Thin Lenses | Ctrl+4 |
| 4 | Mirror Optics | Ctrl+5 |
| 5 | Prism Optics & Dispersion | Ctrl+6 |
| 6 | Settings | Ctrl+7 |

The application **always opens Home on startup**. The previous last-page restoration behavior has been discontinued. The selected light/dark theme remains persistent through `QSettings` (`appearance/theme`). Legacy `window/last_page` and `window/last_page_name` values are no longer saved or used to select the startup page.

#### Testing

The main-window tests were updated to reflect seven-page navigation, the new shortcut assignments, Home-first startup, and persistent theme behavior. Prism calculation, dispersion, visualization, and GUI behavior were exercised during development. The **final full-suite regression outcome has not been recorded**; do not report it as passed until verified.

Recommended targeted verification includes:

- Prism refraction and deviation at representative angles.
- Critical angle and total internal reflection handling.
- Cauchy calculations with realistic material coefficients and correct wavelength conversion.
- Valid and non-transmitting spectral wavelengths.
- All four visualization modes and supported export formats.
- Input persistence and readable light/dark plots.
- Home-first startup after navigating away and closing.
- `Ctrl+1` through `Ctrl+7` navigation.

#### Known Limitations

- Idealized geometrical optics and air as the surrounding medium.
- Cauchy coefficients are empirical and valid only over their fitted wavelength range.
- Non-transmitting wavelengths are omitted from spectral deviation plots.
- Diffraction, interference, polarization, absorption, and full non-paraxial optical modeling are not implemented.

#### Remaining Release Tasks

- [x] Complete v0.4.0 feature implementation.
- [x] Update main-window navigation and startup test expectations.
- [ ] Execute and record final full regression suite.
- [ ] Record manual GUI verification.
- [ ] Finish and review documentation updates.
- [ ] Validate distribution packaging, if applicable.
- [ ] Confirm Git release tag and publication details.

#### Development Outcome

Prism and dispersion functionality has been implemented and integrated. Public release readiness remains subject to the outstanding validation and release tasks.

---

## 11. Documentation Maintenance Policy

Optik maintains versioned development documentation.

### 11.1 Permanent Development Sections

Development environment, project organization, coding standards, calculation and visualization development, testing, Git workflow, and release preparation are updated when general practices change.

### 11.2 Version-Specific Development Sections

Each release records its scope, features, modules, architectural changes, tests, limitations, and development outcome.

### 11.3 Historical Preservation

Preserve previous version sections. Record replacements or behavior changes in the version that introduces them, and correct historical inaccuracies with appropriate notes.

---

## 12. Document Revision History

| Revision | Software Version | Description |
|---|---|---|
| 1.0 | v0.1.0 | Initial development practices and architecture |
| 1.1 | v0.2.0 | Thin lens development and visualization workflow |
| 1.2 | v0.3.0 | Mirror optics development and versioned documentation structure |
| 1.3 | v0.4.0 | Prism optics and dispersion development, seven-page navigation, Home-first startup, and updated release guidance |

---

## 13. Additional Documentation

- `README.md` — Project overview and installation.
- `CHANGELOG.md` — Version-specific release changes.
- `docs/SRS.md` — Software Requirements Specification.
- `docs/SDD.md` — Software Design Document.
- `docs/USER_GUIDE.md` — Application usage instructions.
- `LICENSE` — MIT License.

---

**Optik — Exploring Optics and Photonics Through Scientific Computing.**

**End of Development Guide**
