# Changelog

All notable changes to Optik will be documented in this file.

This project follows [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Planned

- Expand geometrical optics with mirror calculations in v0.3.0.
- Add concave and convex mirror support.
- Implement mirror image formation and magnification.
- Develop mirror ray diagrams.
- Expand scientific visualization and automated testing.
- Continue improving application settings and usability.

---

## [0.2.0] — Release Candidate

### Added

**Thin Lens Optics**
- Implemented the thin lens equation for image distance calculations.
- Added support for converging and diverging lenses.
- Added positive and negative focal length conventions.
- Implemented image magnification calculations.
- Added image height calculations.
- Implemented image orientation classification.
- Added enlarged, reduced, and unchanged image size classifications.
- Added real and virtual image classification.
- Added handling for image formation at infinity.
- Expanded numerical input validation.

**Scientific Visualization**
- Implemented two-dimensional thin lens ray diagrams.
- Added visualization of converging and diverging lenses.
- Added principal optical axes and focal points.
- Added object and image representations.
- Integrated lens ray diagrams with Matplotlib.
- Added dynamic diagram updates following calculations.
- Created a reusable `PlotManager` component.
- Added light and dark plotting themes.
- Added Matplotlib navigation toolbar support.
- Added figure management and plot configuration utilities.
- Added figure export functionality supporting PNG, JPG, JPEG, SVG, and PDF.

**Graphical Interface**
- Created the dedicated Thin Lens calculator page.
- Integrated the Thin Lens page into the main application window.
- Extended sidebar navigation to include Thin Lens.
- Added a Thin Lens feature card to the Home dashboard.
- Added focal length, object distance, and object height input controls.
- Added calculation result displays for image distance, magnification, image height, orientation, and image size.
- Integrated the lens ray diagram into the calculator interface.
- Added persistent calculation defaults using `QSettings`.
- Integrated plotting with Light and Dark application themes.

**Testing**
- Added thin lens physics unit tests.
- Added magnification calculation tests.
- Added lens diagram tests.
- Added Plot Manager tests.
- Updated Main Window tests for the new five-page navigation structure.
- Added navigation coverage for the Thin Lens page and Home dashboard shortcut.
- Expanded coverage of numerical calculations and boundary conditions.

### Fixed

- Corrected Main Window test expectations after adding the Thin Lens page.
- Fixed Matplotlib toolbar integration when replacing figures in the Plot Manager.
- Corrected Thin Lens Home dashboard card initialization.
- Connected the Thin Lens Home dashboard shortcut to application navigation.

### Changed

- Expanded Optik from reflection and refraction calculations to include thin lens optics.
- Updated the application navigation structure.
- Extended the visualization architecture with a reusable plotting component.
- Improved separation between optical calculations, visualization, and graphical interface components.

### Documentation

- Updated the project README with v0.2.0 functionality.
- Prepared updates to the Software Requirements Specification.
- Prepared updates to the Software Design Document.
- Prepared updates to the User Guide.
- Prepared updates to the development documentation.

### Release Verification

- Main Window tests passed.
- Complete test suite verification remains pending.
- Final documentation review remains pending.

**Release status:** v0.2.0 release candidate; not yet tagged or published.

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