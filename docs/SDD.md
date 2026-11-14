# Optik — Software Design Document (SDD)

**Project:** Optik — Open-Source Optics & Photonics Desktop Application  
**Current Development Version:** v0.3.0  
**Document Status:** Maintained  
**License:** MIT  
**Primary Language:** Python  
**GUI Framework:** PySide6

---

## 1. Introduction

### 1.1 Purpose

This Software Design Document (SDD) describes the architecture, components, interfaces, mathematical models, and implementation strategy of Optik.

Optik is a modular scientific desktop application designed to perform optical calculations and generate graphical representations of optical phenomena.

This document establishes the application's core architecture and records design additions introduced in each software version.

### 1.2 Design Objectives

Optik is designed to:

- Separate scientific calculations from GUI components.
- Provide reusable scientific visualization tools.
- Support incremental feature development.
- Maintain independently testable modules.
- Provide a consistent graphical interface.
- Support future expansion into additional optics and photonics disciplines.
- Preserve architectural history between releases.

### 1.3 Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| GUI Framework | PySide6 |
| Scientific Computing | NumPy, SciPy |
| Scientific Visualization | Matplotlib |
| Automated Testing | pytest |
| GUI Testing | pytest-qt |
| Version Control | Git |
| Repository Hosting | GitHub |
| Windows Packaging | PyInstaller, when applicable |

---

# 2. Core System Architecture

## 2.1 Architectural Overview

Optik follows a modular, layered architecture.

The application separates presentation, scientific calculations, visualization, and application configuration.

```text
+--------------------------------------------------+
|                  Optik Desktop                   |
+--------------------------------------------------+
|              Presentation Layer                  |
|                                                  |
| MainWindow | HomePage | Calculator Pages         |
| SettingsPage | Navigation | Input Controls       |
+--------------------------------------------------+
|              Scientific Logic Layer              |
|                                                  |
| Reflection | Refraction | Thin Lenses | Mirrors   |
| Magnification | Image Classification             |
+--------------------------------------------------+
|              Visualization Layer                 |
|                                                  |
| Reflection Diagrams | Refraction Diagrams        |
| Lens Diagrams | Mirror Diagrams | PlotManager    |
+--------------------------------------------------+
|              Application Services                |
|                                                  |
| QSettings | Themes | Configuration | Export      |
+--------------------------------------------------+
```

Scientific calculation modules should remain independent of GUI widgets.

GUI components coordinate user input, calculation execution, and visualization.

## 2.2 Architectural Principles

### Separation of Concerns

Each component has a defined responsibility.

- Scientific modules perform calculations.
- Visualization modules construct optical diagrams.
- GUI pages collect inputs and display results.
- The main window manages application navigation.
- Settings components manage supported preferences.

### Modularity

New optics modules should be introduced without requiring extensive modifications to existing calculation modules.

### Reusability

Shared mathematical and visualization functionality should be implemented in reusable components where practical.

### Testability

Scientific calculations should be testable without launching the graphical interface.

GUI functionality should be tested using pytest-qt.

---

# 3. Project Directory Structure

The following structure represents the primary organization of Optik through v0.3.0.

```text
Optik/
│
├── app/
│   ├── __init__.py
│   └── main_window.py
│
├── optics/
│   ├── __init__.py
│   ├── reflection.py
│   ├── refraction.py
│   ├── thin_lens.py
│   ├── magnification.py
│   ├── mirrors.py
│   └── mirror_magnification.py
│
├── visualization/
│   ├── __init__.py
│   ├── reflection_diagram.py
│   ├── refraction_diagram.py
│   ├── lens_diagram.py
│   └── mirror_diagram.py
│
├── ui/
│   ├── __init__.py
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── home_page.py
│   │   ├── reflection_page.py
│   │   ├── refraction_page.py
│   │   ├── lens_page.py
│   │   ├── mirror_page.py
│   │   └── settings_page.py
│   │
│   └── widgets/
│       └── [Reusable GUI widgets]
│
├── tests/
│   ├── test_reflection.py
│   ├── test_refraction.py
│   ├── test_thin_lens.py
│   ├── test_magnification.py
│   ├── test_mirrors.py
│   ├── test_mirror_magnification.py
│   ├── test_mirror_diagram.py
│   ├── test_mirror_page.py
│   └── [Additional test modules]
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

The structure may be extended as additional optical modules are introduced.

---

# 4. Core Component Design

## 4.1 Main Application Window

**Module:** `app/main_window.py`

**Class:** `MainWindow`

The main window is responsible for:

- Creating the primary application interface.
- Initializing calculator pages.
- Managing sidebar navigation.
- Managing the stacked page container.
- Applying supported application themes.
- Maintaining navigation shortcuts.
- Restoring supported user preferences.

### Page Management

Optik uses `QStackedWidget` to manage application pages.

The current v0.3.0 page organization is:

| Index | Page |
|---|---|
| 0 | Home |
| 1 | Reflection |
| 2 | Refraction |
| 3 | Thin Lenses |
| 4 | Mirror Optics |
| 5 | Settings |

### Navigation

The main window exposes:

```python
navigate_to(index: int)
```

This method updates the active page and sidebar selection.

The Home dashboard emits a navigation signal that the main window handles.

## 4.2 Home Dashboard

**Module:** `ui/pages/home_page.py`

**Classes:** `HomePage`, `FeatureCard`

The Home dashboard provides entry points to Optik's calculation modules.

Each feature card contains:

- A module title.
- A short description.
- An Open Calculator button.
- A destination page index.

### Navigation Signal

```python
navigate_to = Signal(int)
```

The signal communicates the selected destination to the main window.

## 4.3 Settings Management

Optik uses PySide6 `QSettings` to preserve supported application preferences.

Examples include:

```text
appearance/theme
window/last_page
mirror/type
mirror/focal_length
mirror/object_distance
mirror/object_height
```

Settings are restored when the relevant application component initializes.

## 4.4 Theme Management

The application supports:

- Light theme.
- Dark theme.

The main window exposes:

```python
set_theme(theme: str)
```

Pages implementing compatible `set_theme()` methods receive theme updates.

Visualization components may require additional styling to maintain readability.

---

# 5. Scientific Calculation Architecture

## 5.1 Calculation Module Responsibilities

Scientific calculation modules should:

1. Accept numerical inputs.
2. Validate inputs according to the mathematical model.
3. Perform the required calculations.
4. Return numerical results or structured result objects.
5. Raise appropriate exceptions for invalid operations.

Calculation modules should not directly create or manipulate PySide6 widgets.

## 5.2 Numerical Conventions

Optik uses documented sign conventions for optical calculations.

Sign conventions must be consistent between:

- Mathematical equations.
- Returned calculation results.
- GUI result labels.
- Ray diagram coordinates.
- Automated tests.

Different optical models may use different conventions, which must be documented within their respective modules.

## 5.3 Error Handling

Expected invalid input conditions should be handled through appropriate exceptions.

GUI pages should display user-readable error messages rather than allowing expected calculation errors to terminate the application.

---

# 6. Visualization Architecture

## 6.1 Matplotlib Integration

Optik uses Matplotlib for optical diagrams.

Visualization modules are responsible for constructing scientific figures independently of the GUI page layout.

PySide6 pages embed Matplotlib figures using the Qt-compatible canvas.

## 6.2 Reusable Plotting Components

Reusable plotting functionality may include:

- Figure creation.
- Axis configuration.
- Plot clearing.
- Diagram refresh.
- Theme adaptation.
- Figure export.

The PlotManager introduced during v0.2.0 provides a foundation for reusable scientific visualization.

Individual calculator pages may also embed Matplotlib figures directly.

## 6.3 Diagram Design Principles

Optical diagrams should:

- Represent the corresponding mathematical model.
- Identify optical components and reference points.
- Distinguish relevant ray paths.
- Show object and image positions where applicable.
- Maintain readable labels.
- Handle special mathematical cases appropriately.

---

# 7. Version-Specific Design History

The following sections document architectural and implementation changes introduced by each development version.

---

## 7.1 Version 0.1.0 — Reflection and Refraction

**Status:** Completed

### 7.1.1 Overview

Version 0.1.0 established Optik's initial scientific calculation and visualization architecture.

### 7.1.2 Reflection Module

**Module:** `optics/reflection.py`

The reflection module implements the law of reflection.

The fundamental relationship is:

\[
\theta_r = \theta_i
\]

Where:

- \(\theta_r\) is the reflected angle.
- \(\theta_i\) is the incident angle.

The angles are measured relative to the surface normal.

### 7.1.3 Refraction Module

**Module:** `optics/refraction.py`

The refraction module implements Snell's law:

\[
n_1\sin(\theta_1)=n_2\sin(\theta_2)
\]

Where:

- \(n_1\) is the refractive index of the incident medium.
- \(n_2\) is the refractive index of the second medium.
- \(\theta_1\) is the incident angle.
- \(\theta_2\) is the refracted angle.

The module also supports critical-angle calculations and total internal reflection detection.

### 7.1.4 Visualization Components

Version 0.1.0 introduced reflection and refraction ray diagrams.

These diagrams represent incident, reflected, and refracted rays according to the calculated optical behavior.

### 7.1.5 GUI Components

Initial GUI pages included:

- Home.
- Reflection.
- Refraction.
- Settings.

The interface established the foundation for modular navigation and persistent settings.

### 7.1.6 Testing

Testing covered:

- Reflection calculations.
- Refraction calculations.
- Critical-angle calculations.
- Total internal reflection.
- Ray diagrams.
- GUI functionality.

---

## 7.2 Version 0.2.0 — Thin Lens Optics

**Status:** Development Completed

### 7.2.1 Overview

Version 0.2.0 extended the scientific architecture to support geometrical image formation using thin lenses.

### 7.2.2 Thin Lens Calculation Module

**Module:** `optics/thin_lens.py`

The module implements the thin lens equation:

\[
\frac{1}{f}=\frac{1}{d_o}+\frac{1}{d_i}
\]

Where:

- \(f\) is focal length.
- \(d_o\) is object distance.
- \(d_i\) is image distance.

The module supports converging and diverging lenses.

### 7.2.3 Magnification Module

**Module:** `optics/magnification.py`

The magnification relationship is:

\[
m=-\frac{d_i}{d_o}
\]

Image height is calculated using:

\[
h_i=mh_o
\]

Where:

- \(m\) is magnification.
- \(h_i\) is image height.
- \(h_o\) is object height.

The magnification module supports signed numerical values according to its implemented calculation conventions.

### 7.2.4 Lens Visualization

**Module:** `visualization/lens_diagram.py`

The lens diagram module illustrates:

- Converging lens behavior.
- Diverging lens behavior.
- Principal rays.
- Object and image positions.
- Focal points.
- Real and virtual image formation.

### 7.2.5 PlotManager

Version 0.2.0 introduced reusable Matplotlib plotting functionality.

The PlotManager supports common scientific visualization operations and reduces duplication between optical modules.

### 7.2.6 Thin Lens GUI

**Module:** `ui/pages/lens_page.py`

The Thin Lens page provides:

- Optical input controls.
- Calculation execution.
- Image properties.
- Embedded ray diagrams.
- Theme-aware presentation.

### 7.2.7 Testing

Tests were developed for:

- Thin lens equations.
- Magnification calculations.
- Image classification.
- Lens ray diagrams.
- Thin Lens GUI behavior.

---

## 7.3 Version 0.3.0 — Mirror Optics

**Status:** In Development

### 7.3.1 Overview

Version 0.3.0 introduces spherical mirror calculations and visualization.

The design extends Optik's geometrical optics capabilities while maintaining separation between mathematical calculations, diagrams, and GUI components.

### 7.3.2 Mirror Calculation Module

**Module:** `optics/mirrors.py`

**Primary Result Structure:** `MirrorResult`

The mirror calculation module supports:

- Concave mirrors.
- Convex mirrors.
- Mirror image distance.
- Radius of curvature.
- Mirror type classification.
- Real and virtual image classification.
- Image formation at infinity.

### Spherical Mirror Equation

\[
\frac{1}{f}=\frac{1}{d_o}+\frac{1}{d_i}
\]

### Radius of Curvature

\[
R=2f
\]

### Sign Convention

| Quantity | Convention |
|---|---|
| Positive focal length | Concave mirror |
| Negative focal length | Convex mirror |
| Positive image distance | Real image |
| Negative image distance | Virtual image |
| Positive object distance | Real object in front of mirror |

The calculation module validates numerical inputs and handles special mathematical conditions.

### 7.3.3 Mirror Magnification Module

**Module:** `optics/mirror_magnification.py`

**Primary Result Structure:** `MirrorMagnificationResult`

The module calculates:

- Magnification.
- Image height.
- Image orientation.
- Image size classification.

### Magnification Equation

\[
m=-\frac{d_i}{d_o}
\]

### Image Height Equation

\[
h_i=mh_o
\]

The module classifies images as upright or inverted and enlarged, reduced, or the same size.

When an image is formed at infinity, finite magnification is undefined.

### 7.3.4 Mirror Visualization Module

**Module:** `visualization/mirror_diagram.py`

**Class:** `MirrorDiagram`

The MirrorDiagram component is responsible for generating spherical mirror ray diagrams.

#### Principal Components

- Spherical mirror representation.
- Principal optical axis.
- Focal point.
- Center of curvature.
- Object arrow.
- Image arrow.
- Incident rays.
- Reflected rays.
- Virtual ray extensions.

#### Main Methods

```python
draw(focal_length, object_distance, object_height)
clear()
save(filename, dpi=150)
```

The diagram uses the mirror calculation module to determine optical geometry.

The plotting component returns a Matplotlib figure that can be embedded in the GUI.

### 7.3.5 Mirror GUI Module

**Module:** `ui/pages/mirror_page.py`

**Class:** `MirrorPage`

The MirrorPage component provides the user interface for spherical mirror calculations.

#### Inputs

- Mirror type.
- Focal length magnitude.
- Object distance.
- Object height.

#### Outputs

- Mirror type.
- Image distance.
- Radius of curvature.
- Magnification.
- Image height.
- Image classification.
- Image orientation.
- Image size.

#### Controls

- Calculate.
- Reset.
- Matplotlib navigation toolbar.

#### Persistent Settings

The MirrorPage stores supported input values using `QSettings`.

### 7.3.6 Main Window Integration

**Module:** `app/main_window.py`

Version 0.3.0 expands the main application window from five to six pages.

Mirror Optics is assigned page index `4`, and Settings moves to page index `5`.

The main window connects the Home dashboard's navigation signal to its page-navigation method.

### 7.3.7 Home Dashboard Integration

**Module:** `ui/pages/home_page.py`

Version 0.3.0 introduces a Mirror Optics feature card.

The card emits the destination page index when its Open Calculator button is activated.

### 7.3.8 Theme Integration

The MirrorPage supports light and dark themes.

The main window propagates supported theme changes to calculator pages.

Matplotlib figures require separate theme-aware styling for backgrounds, axes, and labels.

### 7.3.9 Testing Architecture

Version 0.3.0 includes automated tests for:

| Module | Test File |
|---|---|
| Mirror calculations | `tests/test_mirrors.py` |
| Mirror magnification | `tests/test_mirror_magnification.py` |
| Mirror diagrams | `tests/test_mirror_diagram.py` |
| Mirror GUI | `tests/test_mirror_page.py` |

The complete automated regression suite has passed.

Manual GUI verification remains part of release preparation.

### 7.3.10 Design Limitations

The mirror module uses the paraxial approximation.

The current implementation does not provide:

- Full non-paraxial ray tracing.
- Spherical aberration analysis.
- Diffraction calculations.
- Interference simulations.
- Wave-optics mirror modeling.

These capabilities are outside the scope of v0.3.0.

---

# 8. Testing and Quality Assurance Architecture

## 8.1 Unit Testing

Optik uses pytest to verify scientific calculations.

Unit tests should cover:

- Expected numerical results.
- Boundary conditions.
- Invalid inputs.
- Special mathematical cases.
- Image classifications.

## 8.2 GUI Testing

Optik uses pytest-qt to verify PySide6 components.

GUI tests should cover:

- Widget initialization.
- Input controls.
- Calculation results.
- Button actions.
- Navigation.
- Theme behavior.
- Persistent settings.

## 8.3 Visualization Testing

Visualization tests should verify:

- Figure creation.
- Optical component placement.
- Ray geometry.
- Diagram labels.
- Special optical cases.
- Export functionality.

## 8.4 Regression Testing

The complete test suite should be executed following significant feature changes.

```bash
python -m pytest tests/ -v
```

Regression testing ensures previously supported functionality continues to operate after new modules are introduced.

## 8.5 Manual Verification

Before release, the application should be launched and tested interactively.

Manual verification should include:

- Calculator operation.
- Page navigation.
- Theme switching.
- Diagram rendering.
- Input handling.
- Settings persistence.

---

# 9. Design Maintenance Policy

Optik follows a versioned software design documentation policy.

### 9.1 Permanent Sections

The following sections are maintained as the current architectural reference:

- Introduction.
- Core architecture.
- Project structure.
- Core component design.
- Scientific calculation architecture.
- Visualization architecture.
- Testing architecture.

### 9.2 Version-Specific Sections

Each release receives a new section documenting:

- New calculation modules.
- New GUI components.
- New visualization components.
- Architectural changes.
- Mathematical models.
- Design decisions.
- Testing strategy.
- Known limitations.

### 9.3 Historical Design Preservation

Previous version sections should remain intact.

If a future release replaces an existing component, the new version section should document the replacement and identify the affected previous design.

Historical inaccuracies may be corrected with appropriate revision notes.

---

# 10. Future Version Template

Append the following structure when developing a new release.

```markdown
## 7.X Version X.Y.Z — Release Title

**Status:** In Development

### X.1 Overview

### X.2 Scientific Calculation Design

### X.3 Visualization Design

### X.4 GUI Design

### X.5 Main Application Integration

### X.6 Architectural Changes

### X.7 Testing Architecture

### X.8 Known Limitations
```

Future versions should be appended without rewriting the historical design sections.

---

# 11. Document Revision History

| Revision | Software Version | Description |
|---|---|---|
| 1.0 | v0.1.0 | Initial reflection and refraction architecture |
| 1.1 | v0.2.0 | Thin lens calculations and visualization architecture |
| 1.2 | v0.3.0 | Mirror optics architecture and versioned documentation structure |

---

**End of Software Design Document**