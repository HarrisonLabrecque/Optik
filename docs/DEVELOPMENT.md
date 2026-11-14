# Optik — Development Guide

**Project:** Optik — Open-Source Optics & Photonics Desktop Application  
**Current Development Version:** v0.3.0  
**Document Status:** Maintained  
**Programming Language:** Python  
**GUI Framework:** PySide6  
**License:** MIT

---

## 1. Introduction

### 1.1 Purpose

This document describes the development practices, project organization, testing procedures, version control workflow, and release preparation process for Optik.

Optik is an open-source scientific desktop application for performing optical calculations and generating scientific visualizations.

The Development Guide is intended for project maintainers and contributors.

### 1.2 Development Objectives

The development process aims to:

- Maintain a modular software architecture.
- Separate scientific calculations from GUI components.
- Develop and test features incrementally.
- Preserve compatibility with existing functionality where practical.
- Maintain readable and maintainable Python code.
- Use automated testing to detect regressions.
- Document changes for each software release.
- Support public open-source development.

### 1.3 Development Philosophy

Optik follows an incremental, version-based development approach.

Each development version introduces a defined set of features.

The general workflow is:

1. Define requirements.
2. Design the scientific calculation modules.
3. Implement the mathematical calculations.
4. Write and execute unit tests.
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

Replace `YOUR_USERNAME` with the actual repository owner's username.

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

Install development dependencies if they are not included in the requirements file:

```bash
python -m pip install pytest pytest-qt
```

### 2.5 Launch the Application

```bash
python -m app.main_window
```

---

## 3. Project Organization

Optik separates application logic into distinct directories.

```text
Optik/
│
├── app/
│   └── main_window.py
│
├── optics/
│   ├── reflection.py
│   ├── refraction.py
│   ├── thin_lens.py
│   ├── magnification.py
│   ├── mirrors.py
│   └── mirror_magnification.py
│
├── visualization/
│   ├── reflection_diagram.py
│   ├── refraction_diagram.py
│   ├── lens_diagram.py
│   └── mirror_diagram.py
│
├── ui/
│   ├── pages/
│   │   ├── home_page.py
│   │   ├── reflection_page.py
│   │   ├── refraction_page.py
│   │   ├── lens_page.py
│   │   ├── mirror_page.py
│   │   └── settings_page.py
│   │
│   └── widgets/
│
├── tests/
│
├── docs/
│   ├── SRS.md
│   ├── SDD.md
│   ├── USER_GUIDE.md
│   ├── DEVELOPMENT.md
│   └── screenshots/
│
├── README.md
├── CHANGELOG.md
├── LICENSE
└── requirements.txt
```

The directory structure may expand as new features are introduced.

### 3.1 `app/`

Contains application initialization and main-window coordination.

### 3.2 `optics/`

Contains mathematical models and scientific calculations.

These modules should not depend on PySide6 widgets.

### 3.3 `visualization/`

Contains Matplotlib-based scientific diagrams.

Visualization modules should use calculation results rather than duplicate mathematical logic unnecessarily.

### 3.4 `ui/`

Contains graphical interface pages, reusable widgets, and user interaction logic.

### 3.5 `tests/`

Contains automated tests for scientific calculations, visualization, and GUI behavior.

### 3.6 `docs/`

Contains project specifications, design documentation, user instructions, and development procedures.

---

## 4. Coding Standards

### 4.1 Python Style

Optik should follow PEP 8 conventions where practical.

Recommended practices include:

- Four spaces for indentation.
- Descriptive variable and function names.
- Type hints for public functions.
- Docstrings for mathematical functions and public classes.
- Small, focused functions.
- Limited duplication.
- Clear exception handling.

### 4.2 Naming Conventions

| Element | Convention | Example |
|---|---|---|
| Modules | snake_case | `mirror_magnification.py` |
| Functions | snake_case | `calculate_mirror_image_distance()` |
| Variables | snake_case | `object_distance` |
| Classes | PascalCase | `MirrorDiagram` |
| Constants | UPPER_SNAKE_CASE | `DEFAULT_FOCAL_LENGTH` |
| Test Files | test_ prefix | `test_mirrors.py` |

### 4.3 Mathematical Function Design

Mathematical functions should:

1. Accept clearly defined inputs.
2. Validate unsupported values.
3. Apply the documented equation.
4. Return results in predictable formats.
5. Raise meaningful exceptions for invalid calculations.

### 4.4 Data Structures

Use structured result objects when a calculation produces several related outputs.

Python dataclasses are suitable for immutable scientific results.

Example:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class OpticalResult:
    focal_length: float
    object_distance: float
    image_distance: float
```

### 4.5 Error Handling

Expected mathematical errors should be handled explicitly.

Examples include:

- Division by zero.
- Non-finite inputs.
- Invalid refractive indices.
- Unsupported optical configurations.
- Invalid distances under the selected model.

Avoid silently returning incorrect numerical results.

### 4.6 GUI Development

GUI pages should:

- Keep layout code separate from mathematical calculations.
- Use PySide6 signals and slots for interaction.
- Validate user input.
- Display readable results.
- Provide consistent styling.
- Support application themes where required.

---

## 5. Scientific Calculation Development

### 5.1 Implementation Workflow

For a new optical calculation module:

1. Identify the governing equations.
2. Document the sign conventions.
3. Determine valid input ranges.
4. Identify special mathematical cases.
5. Implement the calculation functions.
6. Create automated unit tests.
7. Verify numerical results against known examples.
8. Integrate the module into the GUI.

### 5.2 Numerical Accuracy

Calculation tests should use appropriate floating-point tolerances.

Example:

```python
import pytest

def test_example_calculation():
    result = 15.0
    assert result == pytest.approx(15.0)
```

### 5.3 Sign Conventions

Each optical model must clearly document its sign conventions.

For example, the current spherical mirror module uses:

- Positive focal length for concave mirrors.
- Negative focal length for convex mirrors.
- Positive image distance for real images.
- Negative image distance for virtual images.

### 5.4 Special Cases

Special cases should be explicitly considered during implementation.

Examples include:

- Images at infinity.
- Total internal reflection.
- Undefined magnification.
- Invalid denominators.
- Non-finite numerical inputs.

---

## 6. Visualization Development

### 6.1 Matplotlib

Optik uses Matplotlib for optical ray diagrams.

Visualization modules should manage:

- Figure creation.
- Optical axes.
- Object and image positions.
- Optical reference points.
- Ray geometry.
- Labels.
- Diagram clearing.
- Figure export, when supported.

### 6.2 Visualization Testing

Tests should verify that:

- Figures are created successfully.
- Expected optical elements are present.
- Ray geometry is consistent with the mathematical model.
- Special optical cases do not cause unexpected errors.
- Diagram export works where implemented.

### 6.3 GUI Integration

Matplotlib figures may be embedded into PySide6 pages using:

```python
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
```

A navigation toolbar may be included where appropriate.

---

## 7. Testing Standards

### 7.1 Testing Frameworks

Optik uses:

- pytest for mathematical and application logic tests.
- pytest-qt for GUI tests.
- Matplotlib-compatible tests for scientific diagrams.

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

Unit tests should include:

- Standard numerical cases.
- Boundary conditions.
- Invalid inputs.
- Special mathematical cases.
- Result classifications.

### 7.7 GUI Test Coverage

GUI tests should include:

- Widget initialization.
- Default input values.
- Button interactions.
- Calculation results.
- Navigation.
- Settings persistence.
- Theme behavior.

### 7.8 Regression Testing

Regression testing ensures that newly introduced features do not unintentionally break existing functionality.

The complete test suite should be executed after significant changes.

A passing regression suite is required before preparing a release.

### 7.9 Manual GUI Verification

Automated tests do not replace manual interface testing.

Before publishing a release, verify:

- Application startup.
- Sidebar navigation.
- Home dashboard navigation.
- Calculator functionality.
- Diagram rendering.
- Theme switching.
- Settings persistence.
- Error handling.

---

## 8. Git and GitHub Workflow

### 8.1 Branching Strategy

Optik may use version-specific development branches.

Example:

```text
main
version-0.1
version-0.2
version-0.3
```

The `main` branch should represent the intended stable project state.

Development branches allow new features to be implemented and tested before integration.

### 8.2 Create a Development Branch

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
```

Review the staged changes before committing:

```bash
git diff --cached
```

### 8.5 Commit Changes

Use descriptive commit messages.

Examples:

```bash
git commit -m "feat: add spherical mirror calculations"
```

```bash
git commit -m "test: add mirror optics regression tests"
```

```bash
git commit -m "docs: update versioned project documentation"
```

### 8.6 Push Changes

```bash
git push -u origin version-0.4
```

### 8.7 Commit Message Conventions

Recommended prefixes:

| Prefix | Purpose |
|---|---|
| feat | New functionality |
| fix | Bug correction |
| test | Test additions or changes |
| docs | Documentation |
| refactor | Code restructuring |
| chore | Maintenance |
| build | Packaging and build changes |

### 8.8 Version Tags

Create an annotated tag after a release has been validated and committed.

```bash
git tag -a v0.3.0 -m "Optik v0.3.0 - Mirror Optics"
```

Push the tag:

```bash
git push origin v0.3.0
```

Do not create the final release tag until the release is ready.

---

## 9. Release Preparation

### 9.1 Release Checklist

Before publishing a new version:

- [ ] Complete planned functionality.
- [ ] Verify mathematical calculations.
- [ ] Complete unit tests.
- [ ] Complete GUI tests.
- [ ] Complete visualization tests.
- [ ] Run the regression suite.
- [ ] Perform manual GUI verification.
- [ ] Review error handling.
- [ ] Update application version labels.
- [ ] Update README.md.
- [ ] Update CHANGELOG.md.
- [ ] Update SRS.md.
- [ ] Update SDD.md.
- [ ] Update USER_GUIDE.md.
- [ ] Update DEVELOPMENT.md.
- [ ] Verify distribution packages, if applicable.
- [ ] Commit the final changes.
- [ ] Merge or integrate the release branch.
- [ ] Create the Git version tag.
- [ ] Publish the GitHub release.

### 9.2 Windows Packaging

PyInstaller may be used to create a Windows executable.

An example build command is:

```bash
python -m PyInstaller --noconfirm --windowed --name Optik app/main_window.py
```

Packaging settings may require additional adjustments for dependencies, resources, and application entry points.

The resulting executable should be tested before distribution.

### 9.3 Release Notes

Release notes should summarize:

- New features.
- Important improvements.
- Bug fixes.
- Testing status.
- Known limitations.
- Installation or upgrade considerations.

---

# 10. Version-Specific Development History

The following sections record implementation decisions and testing milestones for each development version.

---

## 10.1 Version 0.1.0 — Initial Optics Release

**Status:** Completed

### Development Scope

Version 0.1.0 established Optik's core application architecture.

### Implemented Features

- Reflection calculations.
- Refraction calculations.
- Critical-angle calculations.
- Total internal reflection detection.
- Reflection ray diagrams.
- Refraction ray diagrams.
- Home dashboard.
- Sidebar navigation.
- Settings page.
- Light and dark themes.

### Architecture

The initial architecture separated:

- Mathematical calculations.
- Visualization components.
- GUI pages.
- Main application management.

### Testing

Initial unit tests and GUI tests were developed for reflection and refraction functionality.

### Development Outcome

Version 0.1.0 established the foundation for future optical calculation modules.

---

## 10.2 Version 0.2.0 — Thin Lens Optics

**Status:** Development Completed

### Development Scope

Version 0.2.0 introduced thin lens image formation calculations and expanded scientific visualization capabilities.

### Implemented Features

- Thin lens equation.
- Converging lenses.
- Diverging lenses.
- Magnification.
- Image height.
- Image classification.
- Thin lens ray diagrams.
- Dedicated Thin Lens GUI page.
- Reusable PlotManager functionality.

### Architecture Changes

New scientific modules were introduced for thin lens calculations and magnification.

The visualization architecture was extended to support additional optical diagrams.

The main window and Home dashboard were updated to include the Thin Lens page.

### Testing

Testing covered:

- Thin lens calculations.
- Magnification.
- Image classification.
- Lens ray diagrams.
- Thin Lens GUI functionality.

### Development Outcome

Version 0.2.0 expanded Optik from reflection and refraction into optical image formation.

---

## 10.3 Version 0.3.0 — Mirror Optics

**Status:** In Development

### Development Scope

Version 0.3.0 introduces spherical mirror calculations and ray diagrams.

### Implemented Features

- Concave mirror calculations.
- Convex mirror calculations.
- Mirror image distance.
- Radius of curvature.
- Mirror magnification.
- Mirror image height.
- Real and virtual image classification.
- Image orientation classification.
- Image size classification.
- Mirror ray diagrams.
- Dedicated Mirror Optics page.
- Mirror navigation integration.
- Persistent mirror calculator settings.

### New Scientific Modules

**`optics/mirrors.py`**

Implements spherical mirror equations, mirror classification, image distance, and radius of curvature.

**`optics/mirror_magnification.py`**

Implements magnification, image height, orientation, and image size classification.

### New Visualization Module

**`visualization/mirror_diagram.py`**

Provides the `MirrorDiagram` class for generating concave and convex mirror ray diagrams.

### New GUI Module

**`ui/pages/mirror_page.py`**

Provides the Mirror Optics calculator interface.

### Main Window Integration

The main window was updated to support six pages.

The Home dashboard was expanded with a Mirror Optics feature card.

Keyboard navigation was updated to include the new page.

### Testing

The following test modules were developed:

- `tests/test_mirrors.py`
- `tests/test_mirror_magnification.py`
- `tests/test_mirror_diagram.py`
- `tests/test_mirror_page.py`

Existing magnification tests were also updated to match the supported calculation conventions.

### Regression Testing

The complete automated unit test suite has passed.

### Remaining Release Tasks

- [ ] Complete manual GUI verification.
- [ ] Finalize project documentation.
- [ ] Validate Windows packaging, if applicable.
- [ ] Complete release preparation.
- [ ] Publish the final GitHub release and tag.

### Development Outcome

The Mirror Optics calculation and GUI modules have been implemented and have passed automated testing.

Version 0.3.0 remains in development until release preparation is completed.

---

# 11. Documentation Maintenance Policy

Optik uses a versioned, append-only documentation strategy.

### 11.1 Permanent Development Sections

The following sections establish the current development workflow:

- Development environment.
- Project organization.
- Coding standards.
- Scientific calculation development.
- Visualization development.
- Testing standards.
- Git and GitHub workflow.
- Release preparation.

These sections should be updated when the project's general development practices change.

### 11.2 Version-Specific Development Sections

Each release receives a new section documenting:

- Development scope.
- Implemented features.
- New scientific modules.
- New visualization modules.
- New GUI components.
- Architecture changes.
- Testing results.
- Known limitations.
- Development outcome.

### 11.3 Historical Preservation

Previous version sections should be preserved.

If a future version replaces an earlier implementation, document the change in the new version section.

Historical errors may be corrected with appropriate revision notes.

---

# 12. Future Version Template

Append the following section when beginning a new development version.

```markdown
## 10.X Version X.Y.Z — Release Title

**Status:** In Development

### Development Scope

### Implemented Features

### New Scientific Modules

### New Visualization Modules

### New GUI Components

### Architecture Changes

### Testing

### Regression Testing

### Known Limitations

### Remaining Release Tasks

### Development Outcome
```

Only include headings that apply to the release.

---

# 13. Document Revision History

| Revision | Software Version | Description |
|---|---|---|
| 1.0 | v0.1.0 | Initial development practices and architecture |
| 1.1 | v0.2.0 | Thin lens development and visualization workflow |
| 1.2 | v0.3.0 | Mirror optics development and versioned documentation structure |

---

# 14. Additional Documentation

The following documents provide further project information:

- `README.md` — Project overview and installation.
- `CHANGELOG.md` — Version-specific release changes.
- `docs/SRS.md` — Software Requirements Specification.
- `docs/SDD.md` — Software Design Document.
- `docs/USER_GUIDE.md` — Application usage instructions.
- `LICENSE` — MIT License.

---

**Optik — Exploring Optics and Photonics Through Scientific Computing.**

**End of Development Guide**