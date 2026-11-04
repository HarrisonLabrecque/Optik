# Optik — Software Requirements Specification (SRS)

**Version:** 0.2.0  
**Status:** Release Candidate  
**Application Type:** Desktop Optics and Photonics Reference Software  
**Primary Language:** Python  
**GUI Framework:** PySide6  
**License:** MIT

---

## 1. Introduction

### 1.1 Purpose

This document defines the software requirements for Optik, an open-source desktop application designed to provide educational and computational tools for optics and photonics.

Optik enables users to perform optical calculations and visualize light-ray behavior through an interactive graphical interface.

Version 0.2.0 extends the initial geometrical optics functionality with thin lens calculations, magnification, image classification, and enhanced scientific visualization.

### 1.2 Scope

Optik v0.2.0 focuses on geometrical optics, including:

- Law of reflection.
- Snell's law of refraction.
- Critical-angle calculations.
- Total internal reflection.
- Thin lens equation calculations.
- Converging and diverging lenses.
- Image magnification and image height.
- Real and virtual image formation.
- Image orientation and size classification.
- Two-dimensional optical ray visualization.
- Reusable Matplotlib plotting components.

Future versions may introduce additional optics and photonics calculations, advanced visualization, and simulation capabilities.

### 1.3 Intended Users

Optik is intended for students, educators, researchers, engineers, and individuals studying optics and photonics.

### 1.4 Development Technologies

The application uses Python, PySide6, NumPy, SciPy, Matplotlib, pytest, and pytest-qt.

Not every dependency is required by every calculation. Current geometrical optics models primarily use Python's standard mathematical functions.

## 2. Overall Description

### 2.1 Product Perspective

Optik is a standalone desktop application with a modular architecture.

The graphical interface communicates with independent optical calculation modules and visualization components.

The architecture separates application control, interface presentation, optical computation, and scientific visualization.

### 2.2 Product Functions

The application shall provide:

1. A graphical main window.
2. Sidebar-based navigation.
3. A reflection calculator.
4. A refraction calculator.
5. Critical-angle and total internal reflection calculations.
6. A thin lens calculator.
7. Image magnification and image height calculations.
8. Real and virtual image classification.
9. Two-dimensional optical ray diagrams.
10. Reusable Matplotlib plotting functionality.
11. Light and Dark application themes.
12. Persistent application settings.
13. Input validation and error handling.

### 2.3 Operating Environment

The application is developed using Python and PySide6.

It is intended to run on supported desktop operating systems with compatible Python and Qt installations.

Windows is the primary development environment. Cross-platform compatibility requires verification on each target operating system.

### 2.4 Assumptions

The application assumes:

- Users provide numerical values in the units indicated by the interface.
- Optical calculations use consistent mathematical sign conventions.
- Thin lenses are idealized.
- Lens ray diagrams use the paraxial approximation.
- Scientific diagrams illustrate idealized optical behavior.

## 3. Functional Requirements

### FR-001: Main Window

The system shall provide a graphical main window containing application navigation and a content area.

### FR-002: Navigation

The system shall allow users to navigate between the Home, Reflection, Refraction, Thin Lens, and Settings pages.

The Home page shall provide a shortcut to the Thin Lens calculator.

### FR-003: Reflection Calculation

The system shall calculate the reflected angle using the law of reflection:

**θᵣ = θᵢ**

The incident angle shall be measured relative to the surface normal.

### FR-004: Refraction Calculation

The system shall calculate the refracted angle using Snell's law:

**n₁ sin(θ₁) = n₂ sin(θ₂)**

The system shall accept two refractive indices and an incident angle.

### FR-005: Critical Angle

When n₁ > n₂, the system shall calculate the critical angle:

**θc = arcsin(n₂ / n₁)**

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

### FR-011: Thin Lens Calculation

The system shall calculate image distance using the ideal thin lens equation:

**1/f = 1/dₒ + 1/dᵢ**

The system shall accept:

- Focal length.
- Object distance.
- Object height.

The system shall calculate image distance using:

**dᵢ = (f × dₒ) / (dₒ − f)**

### FR-012: Converging and Diverging Lenses

The system shall support converging and diverging thin lenses.

The following sign conventions shall apply:

- Positive focal length: converging lens.
- Negative focal length: diverging lens.
- Positive object distance: real object.
- Positive image distance: real image.
- Negative image distance: virtual image.

### FR-013: Magnification Calculation

The system shall calculate signed image magnification using:

**m = −dᵢ / dₒ**

The system shall calculate image height using:

**hᵢ = m × hₒ**

### FR-014: Image Orientation

The system shall determine image orientation from the sign of magnification.

- Negative magnification indicates an inverted image.
- Positive magnification indicates an upright image.

### FR-015: Image Size Classification

The system shall classify image size using the magnitude of magnification.

- |m| > 1: enlarged.
- |m| < 1: reduced.
- |m| = 1: unchanged.

### FR-016: Real and Virtual Images

The system shall distinguish real and virtual images using the calculated image distance.

For a real object under the adopted sign convention:

- Positive image distance indicates a real image.
- Negative image distance indicates a virtual image.

### FR-017: Focal-Point Conditions

The system shall handle the mathematical condition where an object is located at the focal point of a converging lens.

Under this condition, the idealized image distance approaches infinity.

The system shall not produce an unhandled division-by-zero error.

### FR-018: Thin Lens Ray Visualization

The system shall provide a two-dimensional diagram of thin lens image formation.

The diagram shall include, where applicable:

- Optical axis.
- Lens position.
- Focal points.
- Object representation.
- Image representation.
- Principal optical rays.

The system shall support both converging and diverging lens configurations.

### FR-019: Dynamic Lens Diagram Updates

The system shall update the lens diagram when a new calculation is performed.

The diagram shall correspond to the current focal length, object distance, and object height.

### FR-020: Plot Manager

The system shall provide a reusable Matplotlib plotting component.

The Plot Manager shall support:

- Embedded Matplotlib figures.
- Figure and axes management.
- Plot refreshing.
- Plot clearing.
- Light and Dark plotting themes.
- Optional navigation toolbar.
- Integration with existing diagram objects.

### FR-021: Figure Export

The Plot Manager shall support exporting figures in the following formats:

- PNG.
- JPG/JPEG.
- SVG.
- PDF.

This requirement applies to the plotting component API. A dedicated export button is not required in the Thin Lens page for v0.2.0.

### FR-022: Application Themes

The system shall support Light and Dark appearance themes.

The Thin Lens visualization shall use a plotting theme compatible with the selected application appearance.

### FR-023: Persistent Settings

The system shall preserve supported application settings between sessions using Qt's `QSettings`.

The Thin Lens page shall support saving and loading calculation defaults.

### FR-024: Thin Lens Input Validation

The system shall validate thin lens calculation inputs.

Validation shall include:

- Finite numerical values.
- Nonzero focal lengths.
- Positive object distances.
- Valid object heights.
- Handling of mathematical singularities.

Invalid inputs shall not cause an unhandled application error.

### FR-025: Calculation Results

The Thin Lens page shall display:

- Image distance.
- Magnification.
- Image height.
- Image orientation.
- Image size classification.
- Lens type.

## 4. Nonfunctional Requirements

### NFR-001: Usability

The graphical interface should provide clearly labeled inputs, buttons, and results.

The Thin Lens calculator should present numerical results and visualization together.

### NFR-002: Modularity

The application shall separate graphical interface components, physics calculations, and visualization logic.

### NFR-003: Maintainability

The source code should support incremental feature development and automated testing.

### NFR-004: Reliability

Valid numerical inputs shall produce results consistent with the implemented geometrical optics equations.

### NFR-005: Responsiveness

Routine optical calculations should complete without noticeable delays under normal operating conditions.

### NFR-006: Documentation

The project shall include user instructions, software requirements, architecture documentation, development documentation, and version history.

### NFR-007: Open Source

The project shall be distributed under the MIT License.

### NFR-008: Testability

Optical calculation modules shall be independently testable without requiring the graphical interface.

GUI and visualization components should support automated testing.

### NFR-009: Extensibility

The architecture should support additional optics modules without requiring substantial changes to existing calculation modules.

### NFR-010: Consistency

Application pages should follow consistent navigation, layout, and appearance conventions.

### NFR-011: Scientific Accuracy

The application shall use documented mathematical equations and sign conventions.

Idealized models and simulation limitations shall be identified in the documentation.

## 5. Constraints and Limitations

Optik v0.2.0 uses idealized geometrical optics models.

The thin lens calculations assume ideal thin lenses and paraxial rays.

The current version does not model:

- Polarization-dependent reflectance.
- Fresnel coefficients.
- Diffraction.
- Interference.
- Wave propagation.
- Absorption and scattering.
- Optical aberrations.
- Thick lens effects.
- Complex multi-element optical systems.
- Three-dimensional optical systems.

Ray diagrams are conceptual illustrations rather than full electromagnetic or physical-optics simulations.

## 6. Verification

Requirements shall be verified through automated unit tests, GUI tests, visualization tests, and manual application testing.

### 6.1 Physics Verification

Physics tests shall verify:

- Reflection calculations.
- Refraction calculations.
- Critical-angle calculations.
- Total internal reflection.
- Thin lens equation calculations.
- Magnification and image height.
- Image classification.
- Boundary conditions and invalid inputs.

### 6.2 GUI Verification

GUI tests shall verify:

- Main window initialization.
- Navigation between pages.
- Thin Lens page accessibility.
- Home dashboard navigation.
- Calculation result updates.
- Input handling.
- Theme integration.

### 6.3 Visualization Verification

Visualization tests shall verify:

- Reflection and refraction diagrams.
- Lens diagram construction.
- Optical ray geometry.
- Figure and canvas management.
- Plotting theme behavior.
- Figure export functionality.

### 6.4 Manual Verification

Manual verification shall include:

- Application startup.
- Page navigation.
- Window resizing.
- Theme switching.
- Lens calculations.
- Diagram rendering.
- Matplotlib toolbar behavior.

### 6.5 Release Readiness

Release readiness requires:

1. Successful execution of the complete applicable automated test suite.
2. Completion of manual GUI verification.
3. Review of numerical accuracy and exceptional conditions.
4. Completion of documentation updates.
5. Review of the release version and Git repository state.

## 7. Future Development

Planned development areas include:

- v0.3.0: Concave and convex mirror calculations.
- v0.4.0: Multi-element optical systems.
- v0.5.0: Wave optics.
- v0.6.0: Interference and diffraction.
- v0.7.0: Polarization.
- v0.8.0: Optical materials.
- v0.9.0: Numerical and Fourier optics.
- v1.0.0: Stable application release.

Future requirements will be defined as each version enters development.

## 8. Conclusion

Optik v0.2.0 expands the software requirements established in v0.1.0 by introducing thin lens optics, magnification, image classification, reusable scientific plotting, and additional GUI functionality.

The modular requirements support continued development toward more advanced optics and photonics applications.