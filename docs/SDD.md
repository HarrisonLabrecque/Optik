# Optik — Software Design Document (SDD)

**Version:** 0.1.0  
**Status:** Initial Release Candidate  
**Programming Language:** Python  
**GUI Framework:** PySide6  

## 1. Introduction

### 1.1 Purpose

This document describes the software architecture, major components, module responsibilities, and implementation design of Optik v0.1.0.

### 1.2 Design Objectives

Optik is designed to be modular, maintainable, extensible, testable, and accessible through a graphical interface.

The architecture separates optical calculations from interface presentation and visualization.

## 2. System Architecture

Optik uses a modular desktop application architecture.

The system consists of four primary layers:

1. Application layer
2. User interface layer
3. Optical computation layer
4. Visualization layer

### 2.1 Architecture Overview

```text
                  Optik Application
                         |
                    Main Window
                         |
                       Sidebar
                         |
                    Page Manager
                         |
          +--------------+--------------+
          |                             |
    Reflection Page               Refraction Page
          |                             |
    Reflection Module            Refraction Module
          |                             |
          |                       Snell's Law
          |                             |
          |                    Total Internal
          |                    Reflection Module
          |                             |
          +--------------+--------------+
                         |
                    Ray Diagram
                         |
                     Matplotlib
```

## 3. Project Structure

```text
Optik/
|
|-- main.py
|-- pyproject.toml
|-- requirements.txt
|-- README.md
|-- CHANGELOG.md
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
|   |   |-- settings_page.py
|   |
|   |-- widgets/
|   |   |-- sidebar.py
|   |   |-- metric_card.py
|   |   |-- input_panel.py
|   |
|   |-- styles/
|       |-- main.qss
|
|-- optics/
|   |-- reflection.py
|   |-- refraction.py
|   |-- snells_law.py
|   |-- total_internal_reflection.py
|
|-- visualization/
|   |-- ray_diagram.py
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
|
|-- docs/
    |-- SRS.md
    |-- SDD.md
    |-- USER_GUIDE.md
    |-- DEVELOPMENT.md
```

Some modules are reserved for future functionality and may not contain complete implementations in v0.1.0.

## 4. Application Layer

### 4.1 Application Entry Point

**File:** `main.py`

Responsibilities:

- Initialize the Qt application.
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
- Display the active page.

The implementation uses `QMainWindow` and `QStackedWidget`.

## 5. User Interface Layer

### 5.1 Sidebar

**File:** `ui/widgets/sidebar.py`

The sidebar provides navigation between application pages.

It communicates navigation requests through Qt signals.

### 5.2 Reflection Page

**File:** `ui/pages/reflection_page.py`

Responsibilities:

- Accept an incident angle.
- Execute the reflection calculation.
- Display the reflected angle.
- Update the reflection ray diagram.
- Handle invalid inputs.

### 5.3 Refraction Page

**File:** `ui/pages/refraction_page.py`

Responsibilities:

- Accept two refractive indices.
- Accept an incident angle.
- Calculate the refracted angle.
- Calculate the critical angle when applicable.
- Detect total internal reflection.
- Update the ray visualization.

### 5.4 Home and Settings Pages

The Home page serves as the application landing page.

The Settings page provides a foundation for future configuration features.

## 6. Optical Computation Layer

The optics package contains independent mathematical functions.

### 6.1 Reflection Module

**File:** `optics/reflection.py`

Primary function:

`calculate_reflection(incident_angle)`

Implements:

θᵣ = θᵢ

### 6.2 Snell's Law Module

**File:** `optics/snells_law.py`

Primary function:

`calculate_snells_law(n1, n2, incident_angle)`

Implements:

θ₂ = arcsin[(n₁ / n₂) sin(θ₁)]

### 6.3 Refraction Module

**File:** `optics/refraction.py`

Primary function:

`calculate_refraction(n1, n2, incident_angle)`

Provides a higher-level interface to the Snell's law calculation.

### 6.4 Total Internal Reflection Module

**File:** `optics/total_internal_reflection.py`

Primary functions:

- `calculate_critical_angle(n1, n2)`
- `is_total_internal_reflection(n1, n2, incident_angle)`

The critical angle is defined only when n₁ > n₂.

## 7. Visualization Layer

### 7.1 Ray Diagram

**File:** `visualization/ray_diagram.py`

The `RayDiagram` class inherits from `QWidget`.

It embeds a Matplotlib figure using `FigureCanvasQTAgg`.

Primary methods:

- `draw_reflection(incident_angle)`
- `draw_refraction(n1, n2, incident_angle)`

### 7.2 Coordinate System

The diagram uses a two-dimensional Cartesian coordinate system.

The optical interface is positioned at y = 0.

The surface normal is positioned at x = 0.

Incident rays originate above the interface and travel toward the origin.

Reflected rays travel away from the origin into the upper medium.

Refracted rays enter the lower medium when transmission is geometrically possible.

### 7.3 Total Internal Reflection

When total internal reflection occurs, the diagram displays incident and reflected rays without a refracted ray.

## 8. Input Validation

Optical calculation modules validate numerical inputs.

Validation includes:

- Finite numeric values
- Positive refractive indices
- Incident angles between 0° and 90°
- Valid critical-angle conditions

Invalid inputs raise `ValueError`.

The graphical interface catches calculation errors and displays messages to the user.

## 9. Testing Architecture

Optik uses pytest and pytest-qt.

### 9.1 Unit Tests

Unit tests verify the mathematical correctness of the optical calculation modules.

### 9.2 GUI Tests

GUI tests verify widget initialization, user interactions, calculation results, and page navigation.

### 9.3 Visualization Tests

Visualization tests inspect ray annotations, geometry, and diagram updates.

### 9.4 Manual Verification

Manual testing verifies application startup, navigation, resizing, and visualization behavior.

## 10. Dependencies

The primary technologies include:

- Python
- PySide6
- Matplotlib
- NumPy
- SciPy
- pytest
- pytest-qt

The initial optical calculations use Python's standard `math` module.

## 11. Future Architecture

Future releases may extend the computation layer with:

- Lens and mirror models
- Optical materials
- Wave optics
- Polarization
- Numerical simulation
- Advanced plotting

The modular architecture is intended to support these additions without requiring a complete redesign.

## 12. Conclusion

Optik v0.1.0 establishes the architectural foundation for an extensible optics and photonics desktop application.

Its separation of interface, mathematical computation, and visualization supports future scientific functionality.