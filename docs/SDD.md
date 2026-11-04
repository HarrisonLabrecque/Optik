# Optik — Software Design Document (SDD)

**Version:** 0.2.0  
**Status:** Release Candidate  
**Programming Language:** Python  
**GUI Framework:** PySide6  
**License:** MIT

---

## 1. Introduction

### 1.1 Purpose

This document describes the software architecture, major components, module responsibilities, data flow, and implementation design of Optik v0.2.0.

Optik is an open-source desktop application designed for optics and photonics calculations and scientific visualization.

Version 0.2.0 extends the original reflection and refraction functionality with thin lens calculations, magnification, image classification, and lens ray diagrams.

### 1.2 Design Objectives

Optik is designed to be:

- **Modular:** Separate optical calculations, graphical interface, and visualization.
- **Maintainable:** Organize functionality into independent modules.
- **Extensible:** Support additional optics and photonics calculations.
- **Testable:** Allow numerical and GUI components to be tested independently.
- **Accessible:** Provide an understandable graphical interface for scientific calculations.
- **Reusable:** Share visualization and interface components across multiple calculation pages.

### 1.3 Scope

The v0.2.0 architecture supports:

- Reflection calculations.
- Refraction and Snell's law.
- Critical-angle calculations.
- Total internal reflection detection.
- Thin lens calculations.
- Magnification and image height calculations.
- Image orientation and size classification.
- Two-dimensional ray visualization.
- Light and Dark application themes.
- Automated testing.

Advanced wave optics and multi-element optical simulations remain outside the current scope.

## 2. System Architecture

Optik uses a modular desktop application architecture.

The system consists of four primary layers:

1. Application layer
2. User interface layer
3. Optical computation layer
4. Visualization layer

Supporting utility and configuration modules provide shared functionality.

### 2.1 Architecture Overview

```text
                       Optik Application
                               |
                         Main Window
                               |
                     Sidebar / Navigation
                               |
                         QStackedWidget
                               |
          +--------------------+--------------------+
          |                    |                    |
    Reflection Page      Refraction Page        Lens Page
          |                    |                    |
    Reflection Module     Refraction Module    Thin Lens Module
          |                    |                    |
          |                Snell's Law         Magnification Module
          |                    |                    |
          |             Total Internal              |
          |             Reflection Module           |
          |                    |                    |
          +--------------------+                    |
                   |                                |
              Ray Diagram                      Lens Diagram
                   |                                |
                   |                           Plot Manager
                   |                                |
                   +---------------+----------------+
                                   |
                               Matplotlib
                                   |
                              PySide6 / Qt
```

The Home and Settings pages operate alongside the calculator pages.

### 2.2 Design Principles

- Optical calculations must remain independent of PySide6.
- Visualization modules must not duplicate physics calculations.
- GUI pages coordinate inputs, calculations, and result displays.
- Shared plotting functionality should be implemented through reusable components.
- Existing functionality must remain compatible with new modules.

## 3. Project Structure

```text
Optik/
|
|-- main.py
|-- pyproject.toml
|-- requirements.txt
|-- README.md
|-- CHANGELOG.md
|-- CONTRIBUTING.md
|-- LICENSE
|
|-- app/
|   |-- __init__.py
|   |-- main_window.py
|   |-- config.py
|
|-- ui/
|   |-- pages/
|   |   |-- home_page.py
|   |   |-- reflection_page.py
|   |   |-- refraction_page.py
|   |   |-- lens_page.py
|   |   |-- settings_page.py
|   |
|   |-- widgets/
|   |   |-- sidebar.py
|   |   |-- metric_card.py
|   |   |-- input_panel.py
|   |
|   |-- styles/
|       |-- main.qss
|       |-- light.qss
|       |-- dark.qss
|
|-- optics/
|   |-- reflection.py
|   |-- refraction.py
|   |-- snells_law.py
|   |-- total_internal_reflection.py
|   |-- thin_lens.py
|   |-- magnification.py
|
|-- visualization/
|   |-- ray_diagram.py
|   |-- lens_diagram.py
|   |-- plot_manager.py
|
|-- utils/
|   |-- validators.py
|   |-- constants.py
|
|-- tests/
|   |-- test_reflection.py
|   |-- test_refraction.py
|   |-- test_snells_law.py
|   |-- test_total_internal_reflection.py
|   |-- test_main_window.py
|   |-- test_reflection_page.py
|   |-- test_refraction_page.py
|   |-- test_ray_diagram.py
|   |-- test_thin_lens.py
|   |-- test_magnification.py
|   |-- test_lens_diagram.py
|   |-- test_plot_manager.py
|
|-- docs/
    |-- SRS.md
    |-- SDD.md
    |-- USER_GUIDE.md
    |-- DEVELOPMENT.md
```

Some components may remain under development or require additional integration testing.

## 4. Application Layer

### 4.1 Application Entry Point

**File:** `main.py`

Responsibilities:

- Initialize `QApplication`.
- Configure application information.
- Load the application stylesheet.
- Create and display the main window.
- Start the Qt event loop.

### 4.2 Main Window

**File:** `app/main_window.py`

The `MainWindow` class manages the primary application interface.

Responsibilities:

- Initialize the sidebar.
- Register application pages.
- Manage page navigation.
- Connect Home dashboard shortcuts.
- Display the active page.
- Apply application themes.
- Coordinate persistent settings.

The implementation uses `QMainWindow` and `QStackedWidget`.

### 4.3 Page Registration

Version 0.2.0 contains five primary pages.

| Page | Stack Index | Module |
|---|---:|---|
| Home | 0 | `home_page.py` |
| Reflection | 1 | `reflection_page.py` |
| Refraction | 2 | `refraction_page.py` |
| Thin Lens | 3 | `lens_page.py` |
| Settings | 4 | `settings_page.py` |

Navigation requests are processed by the main window.

The sidebar emits navigation signals, while the main window updates the active page.

## 5. User Interface Layer

### 5.1 Sidebar

**File:** `ui/widgets/sidebar.py`

The sidebar provides navigation between application pages.

Responsibilities:

- Display navigation options.
- Emit page-selection signals.
- Indicate the active page.
- Support navigation to the Thin Lens calculator.

### 5.2 Home Page

**File:** `ui/pages/home_page.py`

The Home page provides the application's landing interface.

It contains feature cards for the available optical calculators.

Version 0.2.0 adds a Thin Lens feature card that opens the corresponding calculator page.

### 5.3 Reflection Page

**File:** `ui/pages/reflection_page.py`

Responsibilities:

- Accept an incident angle.
- Execute the reflection calculation.
- Display the reflected angle.
- Update the reflection ray diagram.
- Handle invalid inputs.

### 5.4 Refraction Page

**File:** `ui/pages/refraction_page.py`

Responsibilities:

- Accept two refractive indices.
- Accept an incident angle.
- Calculate the refracted angle.
- Calculate the critical angle when applicable.
- Detect total internal reflection.
- Update the ray visualization.

### 5.5 Thin Lens Page

**File:** `ui/pages/lens_page.py`

The `LensPage` class provides the graphical interface for thin lens calculations.

**Inputs**

- Focal length.
- Object distance.
- Object height.

**Outputs**

- Image distance.
- Magnification.
- Image height.
- Image orientation.
- Relative image size.
- Lens type.
- Lens ray diagram.

**Responsibilities**

- Read numerical inputs.
- Invoke the optical calculation modules.
- Update calculation results.
- Generate lens ray diagrams.
- Display diagrams using the Plot Manager.
- Load and save calculation defaults.
- Apply the current plotting theme.

The page uses PySide6 input widgets and `QSettings` for persistent defaults.

### 5.6 Settings Page

**File:** `ui/pages/settings_page.py`

The Settings page provides application configuration options.

The application supports Light and Dark appearance themes.

Settings are persisted using Qt's `QSettings` system.

## 6. Optical Computation Layer

The `optics/` package contains mathematical functions independent of the graphical interface.

### 6.1 Reflection Module

**File:** `optics/reflection.py`

Primary function:

`calculate_reflection(incident_angle)`

Implements the law of reflection:

**θᵣ = θᵢ**

### 6.2 Snell's Law Module

**File:** `optics/snells_law.py`

Primary function:

`calculate_snells_law(n1, n2, incident_angle)`

Implements:

**θ₂ = arcsin[(n₁ / n₂) sin(θ₁)]**

The calculation must account for conditions where no real refracted angle exists.

### 6.3 Refraction Module

**File:** `optics/refraction.py`

Primary function:

`calculate_refraction(n1, n2, incident_angle)`

Provides a higher-level interface to Snell's law calculations.

### 6.4 Total Internal Reflection Module

**File:** `optics/total_internal_reflection.py`

Primary functions:

- `calculate_critical_angle(n1, n2)`
- `is_total_internal_reflection(n1, n2, incident_angle)`

The critical angle is defined only when **n₁ > n₂**.

### 6.5 Thin Lens Module

**File:** `optics/thin_lens.py`

The module calculates image formation using the ideal thin lens equation.

**Primary function**

`calculate_image_distance(f, do)`

**Equation**

**1/f = 1/dₒ + 1/dᵢ**

Rearranged:

**dᵢ = (f × dₒ) / (dₒ − f)**

**Sign conventions**

| Parameter | Interpretation |
|---|---|
| f > 0 | Converging lens |
| f < 0 | Diverging lens |
| dₒ > 0 | Real object |
| dᵢ > 0 | Real image |
| dᵢ < 0 | Virtual image |

When `dₒ = f` for a converging lens, the image distance approaches infinity.

The module provides a `ThinLensResult` data structure for representing calculated lens properties.

### 6.6 Magnification Module

**File:** `optics/magnification.py`

The module calculates image magnification, image height, and image classification.

**Primary functions**

- `calculate_magnification(di, do)`
- `calculate_image_height(m, ho)`
- `classify_orientation(m)`
- `classify_image_size(m)`
- `calculate_image_properties(di, do, ho)`

**Magnification equation**

**m = −dᵢ / dₒ**

**Image height equation**

**hᵢ = m × hₒ**

**Orientation**

- Negative magnification: inverted.
- Positive magnification: upright.

**Image size**

- |m| > 1: enlarged.
- |m| < 1: reduced.
- |m| = 1: unchanged.

The module provides a `MagnificationResult` data structure for calculated image properties.

## 7. Visualization Layer

### 7.1 Ray Diagram

**File:** `visualization/ray_diagram.py`

The `RayDiagram` class inherits from `QWidget`.

It embeds a Matplotlib figure using `FigureCanvasQTAgg`.

Primary methods:

- `draw_reflection(incident_angle)`
- `draw_refraction(n1, n2, incident_angle)`

### 7.2 Reflection and Refraction Coordinate System

The diagram uses a two-dimensional Cartesian coordinate system.

- The optical interface is positioned at `y = 0`.
- The surface normal is positioned at `x = 0`.
- Incident rays originate above the interface and travel toward the origin.
- Reflected rays travel away from the origin into the upper medium.
- Refracted rays enter the lower medium when transmission is geometrically possible.

### 7.3 Total Internal Reflection Visualization

When total internal reflection occurs, the diagram displays incident and reflected rays without a refracted ray.

### 7.4 Lens Diagram

**File:** `visualization/lens_diagram.py`

The `LensDiagram` class generates two-dimensional thin lens ray diagrams.

Responsibilities:

- Draw the optical axis.
- Represent the lens position.
- Mark focal points.
- Draw the object.
- Draw the image when representable at a finite distance.
- Illustrate principal optical rays.
- Support converging and diverging lens configurations.

**Primary methods**

- `draw(f, do, ho)`
- `clear()`
- `save(...)`

The diagram uses Matplotlib's `Figure` and `Axes` objects.

For thin lens diagrams:

- The lens is located at `x = 0`.
- The optical axis is located at `y = 0`.
- The object is positioned at `x = −dₒ`.
- Real images appear on the opposite side of the lens.
- Virtual images appear on the object side.

The diagrams use idealized paraxial ray geometry.

### 7.5 Plot Manager

**File:** `visualization/plot_manager.py`

The `PlotManager` class provides reusable Matplotlib integration for PySide6 widgets.

**Responsibilities**

- Embed Matplotlib figures.
- Manage the plotting canvas.
- Manage the navigation toolbar.
- Apply Light and Dark themes.
- Refresh and clear plots.
- Configure axes.
- Display existing diagram objects.
- Export figures.

**Primary methods**

- `set_figure(figure)`
- `get_figure()`
- `get_axes()`
- `refresh()`
- `draw()`
- `clear()`
- `clear_figure()`
- `apply_theme(theme)`
- `set_title(title)`
- `set_labels(xlabel, ylabel)`
- `set_limits(xmin, xmax, ymin, ymax)`
- `set_grid(enabled)`
- `plot_line(...)`
- `plot_scatter(...)`
- `display_diagram(diagram)`
- `save_plot(filename, dpi)`
- `reset()`

**Figure replacement**

When a different Matplotlib figure is assigned, the Plot Manager replaces the associated canvas and navigation toolbar.

This avoids relying on the unsupported `NavigationToolbar2QT.set_canvas()` method.

## 8. Component Interaction and Data Flow

### 8.1 Thin Lens Calculation Workflow

```text
User enters lens parameters
            |
            v
       LensPage
            |
            v
    Input validation
            |
            v
    Thin Lens Module
            |
            v
  Image distance result
            |
            v
  Magnification Module
            |
            v
  Image classification
            |
            +-------------------+
            |                   |
            v                   v
      Result Labels        LensDiagram
                                |
                                v
                           PlotManager
                                |
                                v
                         Matplotlib Canvas
```

### 8.2 Navigation Workflow

```text
User selects page
        |
        v
Sidebar or Home feature card
        |
        v
MainWindow.change_page()
        |
        v
QStackedWidget
        |
        v
Selected calculator page
```

### 8.3 Theme Workflow

```text
User selects theme
        |
        v
Settings / QSettings
        |
        v
MainWindow
        |
        +-------------------+
        |                   |
        v                   v
Application stylesheet   PlotManager
                            |
                            v
                       Figure colors
```

## 9. Input Validation

Optical calculation modules validate numerical inputs.

### 9.1 Reflection and Refraction

Validation includes:

- Finite numeric values.
- Positive refractive indices.
- Incident angles between 0° and 90°.
- Valid critical-angle conditions.

### 9.2 Thin Lens Calculations

Validation includes:

- Finite focal lengths.
- Nonzero focal lengths.
- Positive object distances.
- Valid object heights.
- Handling of focal-point singularities.
- Prevention of division by zero.
- Appropriate handling of infinite image distances.

Invalid inputs raise appropriate exceptions, including `ValueError`.

The graphical interface handles calculation errors and presents understandable feedback.

## 10. Testing Architecture

Optik uses pytest and pytest-qt.

### 10.1 Unit Tests

Unit tests verify the mathematical correctness of optical calculation modules.

Relevant files include:

- `test_reflection.py`
- `test_refraction.py`
- `test_snells_law.py`
- `test_total_internal_reflection.py`
- `test_thin_lens.py`
- `test_magnification.py`

### 10.2 GUI Tests

GUI tests verify widget initialization, user interactions, calculation results, and page navigation.

Relevant files include:

- `test_main_window.py`
- `test_reflection_page.py`
- `test_refraction_page.py`

Additional Thin Lens page integration tests are part of v0.2.0 release verification.

### 10.3 Visualization Tests

Visualization tests verify ray geometry, diagram construction, figure management, and plotting behavior.

Relevant files include:

- `test_ray_diagram.py`
- `test_lens_diagram.py`
- `test_plot_manager.py`

### 10.4 Manual Verification

Manual testing verifies:

- Application startup.
- Navigation.
- Window resizing.
- Theme switching.
- Calculator interactions.
- Diagram rendering.
- Plot toolbar functionality.

### 10.5 Test Execution

Run the complete suite:

```bash
python -m pytest tests/ -v
```

## 11. Dependencies

The primary technologies include:

- Python
- PySide6
- Matplotlib
- NumPy
- SciPy
- pytest
- pytest-qt

The initial geometrical optics calculations primarily use Python's standard `math` module.

## 12. Design Constraints and Limitations

Optik v0.2.0 uses idealized geometrical optics models.

The thin lens implementation assumes:

- Thin lenses.
- Paraxial rays.
- Idealized image formation.
- Consistent distance sign conventions.
- No optical aberrations.

The application does not currently model diffraction, interference, polarization, or full electromagnetic wave behavior.

## 13. Future Architecture

Future releases may extend the computation and visualization layers with:

- Concave and convex mirrors.
- Multi-element optical systems.
- Optical materials and dispersion.
- Wave optics.
- Polarization.
- Interference and diffraction.
- Fourier optics.
- Advanced numerical simulations.

The modular architecture is intended to support these additions without requiring a complete redesign.

## 14. Conclusion

Optik v0.2.0 expands the application's geometrical optics capabilities while maintaining the modular architecture established in v0.1.0.

The addition of thin lens calculations, magnification analysis, reusable plotting components, and expanded GUI navigation provides a foundation for future optical system modeling.

The next planned development milestone is v0.3.0, focusing on mirror optics.