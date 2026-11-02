# Changelog

All notable changes to Optik will be documented in this file.

This project follows [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Planned
- Additional optics and photonics calculations.
- Expanded scientific visualization capabilities.
- Improvements to application settings.
- Further numerical and graphical testing.
- Additional optical simulation modules.

---

## [0.2.0] — In Development

### Planned

**Thin Lens Optics**
- Implement thin lens equation calculations.
- Add converging and diverging lens support.
- Calculate image distance and focal length.
- Calculate image magnification and orientation.
- Determine real and virtual image formation.
- Implement optical input validation.

**Scientific Visualization**
- Develop interactive thin lens ray diagrams.
- Visualize converging and diverging lenses.
- Display focal points and principal optical axes.
- Illustrate image formation and magnification.
- Support dynamic updates when calculation inputs change.

**Graphical Interface**
- Create a dedicated Thin Lenses page.
- Integrate the lens calculator with the main application.
- Extend sidebar navigation.
- Maintain compatibility with Light and Dark themes.

**Testing**
- Add thin lens physics unit tests.
- Add magnification calculation tests.
- Add lens visualization tests.
- Extend GUI tests for the Thin Lenses page.
- Verify numerical accuracy and boundary conditions.

**Documentation**
- Update the Software Requirements Specification.
- Update the Software Design Document.
- Update the User Guide.
- Update the development documentation.

---

## [0.1.0] — Development Release

### Added

**Application Framework**
- Created the Optik desktop application using Python and PySide6.
- Implemented the main application window.
- Added sidebar navigation.
- Created Home, Reflection, Refraction, and Settings pages.
- Implemented Light and Dark application themes.
- Added persistent application settings.

**Optical Calculations**
- Implemented the law of reflection.
- Implemented Snell's law.
- Added refraction calculations.
- Added critical-angle calculations.
- Implemented total internal reflection detection.
- Added numerical input validation.

**Graphical Interface**
- Created an interactive reflection calculator.
- Created an interactive refraction calculator.
- Added numerical input controls.
- Added calculation result displays.
- Integrated total internal reflection status indicators.
- Added scrollable calculator pages.
- Implemented theme selection in Settings.

**Scientific Visualization**
- Implemented two-dimensional optical ray diagrams.
- Added incident and reflected ray visualization.
- Added refracted ray visualization.
- Added total internal reflection visualization.
- Integrated Matplotlib with PySide6.
- Added dynamic diagram updates.

**Testing**
- Added physics unit tests using pytest.
- Added GUI tests using pytest-qt.
- Added ray visualization tests.
- Added input validation and boundary-condition tests.

**Documentation**
- Created the Software Requirements Specification.
- Created the Software Design Document.
- Created the User Guide.
- Added project licensing information.

### Notes

Version 0.1.0 establishes the foundation for future Optik development.

This development release focuses on fundamental geometrical optics, introductory scientific visualization, and application architecture.

Advanced optical simulations remain outside the scope of v0.1.0.

**Release status:** Development version tagged as `v0.1.0`.

---