# Optik — Software Requirements Specification (SRS)

**Version:** 0.1.0  
**Status:** Initial Release Candidate  
**Application Type:** Desktop Optics and Photonics Reference Software  
**Primary Language:** Python  
**GUI Framework:** PySide6  

## 1. Introduction

### 1.1 Purpose

This document defines the software requirements for Optik, an open-source desktop application designed to provide educational and computational tools for optics and photonics.

Optik enables users to perform fundamental optical calculations and visualize light-ray behavior through an interactive graphical interface.

### 1.2 Scope

Optik v0.1.0 focuses on geometrical optics, including:

- Law of reflection
- Snell's law of refraction
- Critical-angle calculations
- Total internal reflection
- Two-dimensional optical ray visualization

Future versions may introduce additional optics and photonics calculations, advanced visualization, and simulation capabilities.

### 1.3 Intended Users

Optik is intended for students, educators, researchers, engineers, and individuals studying optics and photonics.

### 1.4 Development Technologies

The application uses Python, PySide6, NumPy, SciPy, Matplotlib, pytest, and pytest-qt.

Not every dependency is required by every calculation in v0.1.0. The initial physics models primarily use Python's standard mathematical functions.

## 2. Overall Description

### 2.1 Product Perspective

Optik is a standalone desktop application with a modular architecture.

The graphical interface communicates with independent optical calculation modules and visualization components.

### 2.2 Product Functions

The application shall provide:

1. A graphical main window.
2. Sidebar-based navigation.
3. A reflection calculator.
4. A refraction calculator.
5. Critical-angle and total internal reflection calculations.
6. Two-dimensional optical ray diagrams.
7. Input validation and error handling.

### 2.3 Operating Environment

The application is developed using Python and PySide6.

It is intended to run on supported desktop operating systems with compatible Python and Qt installations.

Windows is the primary development environment for v0.1.0. Cross-platform compatibility requires verification on each target operating system.

## 3. Functional Requirements

### FR-001: Main Window

The system shall provide a graphical main window containing application navigation and a content area.

### FR-002: Navigation

The system shall allow users to navigate between the Home, Reflection, Refraction, and Settings pages.

### FR-003: Reflection Calculation

The system shall calculate the reflected angle using the law of reflection:

θᵣ = θᵢ

The incident angle shall be measured relative to the surface normal.

### FR-004: Refraction Calculation

The system shall calculate the refracted angle using Snell's law:

n₁ sin(θ₁) = n₂ sin(θ₂)

The system shall accept two refractive indices and an incident angle.

### FR-005: Critical Angle

When n₁ > n₂, the system shall calculate the critical angle:

θc = arcsin(n₂ / n₁)

### FR-006: Total Internal Reflection

The system shall identify total internal reflection when light travels from a higher refractive index to a lower refractive index and the incident angle exceeds the critical angle.

### FR-007: Ray Visualization

The system shall display a two-dimensional ray diagram illustrating applicable incident, reflected, and refracted rays.

The diagram shall include an optical interface and surface normal.

### FR-008: Interactive Calculation

The system shall allow users to change numerical inputs and update calculation results and diagrams.

### FR-009: Input Validation

The system shall reject invalid optical parameters.

Incident angles shall be within the range of 0° to 90°, inclusive.

Refractive indices shall be positive and finite.

### FR-010: Error Handling

The system shall display appropriate error messages when calculations cannot be completed.

## 4. Nonfunctional Requirements

### NFR-001: Usability

The graphical interface should provide clearly labeled inputs, buttons, and results.

### NFR-002: Modularity

The application shall separate graphical interface components, physics calculations, and visualization logic.

### NFR-003: Maintainability

The source code should support incremental feature development and automated testing.

### NFR-004: Reliability

Valid numerical inputs shall produce results consistent with the implemented geometrical optics equations.

### NFR-005: Responsiveness

Routine optical calculations should complete without noticeable delays under normal operating conditions.

### NFR-006: Documentation

The project shall include user instructions, software requirements, architecture documentation, and version history.

### NFR-007: Open Source

The project shall be distributed under the MIT License.

## 5. Constraints and Limitations

Optik v0.1.0 uses idealized geometrical optics models.

The initial release does not model:

- Polarization-dependent reflectance
- Fresnel coefficients
- Diffraction
- Interference
- Wave propagation
- Absorption and scattering
- Three-dimensional optical systems

The ray diagrams are conceptual illustrations rather than full optical simulations.

## 6. Verification

Requirements shall be verified through automated unit tests, GUI tests, visualization tests, and manual application testing.

Release readiness requires successful execution of the applicable test suite and completion of manual verification.

## 7. Future Development

Potential future capabilities include:

- Lens and mirror calculations
- Optical system modeling
- Wave optics
- Polarization
- Interference and diffraction
- Additional numerical simulation methods

These features are outside the scope of v0.1.0.