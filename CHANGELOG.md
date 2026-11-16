Changelog

All notable changes to Optik — Open-Source Optics & Photonics Desktop Application are documented in this file.

The format is based on Keep a Changelog, and the project follows Semantic Versioning.

Changelog Maintenance Policy

Each release has its own section. Previous release entries are preserved, except for factual corrections.

Changes are organized under the following categories when applicable:

Added: New features, modules, and functionality.

Changed: Updates to existing features or behavior.

Fixed: Corrections to bugs and errors.

Deprecated: Features scheduled for removal.

Removed: Features removed from the application.

Security: Security-related changes.

During development, changes are recorded under the upcoming version. When the release is published, its status is updated and the release date is added.

[0.4.0] — Prism Optics & Dispersion

Status: Development Completed
Release Date: Not recorded

Added

Prism refraction calculations using Snell's law at both prism surfaces.

Incident, internal refraction, emergent, and total deviation angle calculations.

Minimum deviation and critical angle calculations.

Detection and handling of total internal reflection in prism calculations.

Cauchy's dispersion equation with configurable coefficients for wavelength-dependent refractive indices.

Spectral dispersion and prism deviation calculations across selectable wavelengths.

Dedicated Prism Optics & Dispersion calculator page.

Four prism visualization modes:

Prism Ray Diagram.

Refractive Index vs Wavelength.

Prism Deviation vs Wavelength.

Visible Spectrum.

Prism-related input persistence using application settings.

Diagram and graph export in supported Matplotlib formats, including PNG, SVG, and PDF.

Prism Optics & Dispersion navigation entry and Ctrl+6 shortcut.

Changed

Expanded the main application window to seven pages.

Moved the Settings keyboard shortcut to Ctrl+7.

Updated application startup behavior to always open the Home page instead of restoring the last visited page.

Continued to preserve the selected light or dark appearance theme between sessions.

Updated prism visualization management to switch between multiple plots on the shared Matplotlib canvas.

Updated main window tests to reflect Home-first startup and revised navigation persistence behavior.

Updated project documentation to include the v0.4.0 features and navigation changes.

Fixed

Improved handling of invalid prism geometry and optical input values.

Improved error reporting when spectral prism calculations cannot produce transmitted rays.

Addressed prism deviation-versus-wavelength plotting behavior for invalid or non-transmitting wavelengths.

Corrected the unintended reopening of the last visited page at application startup.

Scientific Model and Limitations

Cauchy's model uses n(λ) = A + B/λ² + C/λ⁴, with wavelength λ expressed in micrometers.

Prism calculations assume an air surrounding medium and idealized geometrical optics.

Cauchy coefficients must be appropriate for the material and wavelength range; arbitrary coefficients can produce physically unrealistic refractive indices.

Wavelengths without a valid transmitted ray are excluded from spectral prism deviation results.

Diffraction, polarization, absorption, and interference are outside the scope of this module.

Testing

Updated main window navigation and persistence tests for the new startup behavior.

Prism calculations, dispersion, visualizations, and GUI behavior were exercised during development.

Final full-suite regression results are not recorded in this changelog.

Release Preparation

Implement prism optics calculations.

Implement Cauchy dispersion calculations.

Implement four prism visualization modes.

Integrate the Prism Optics & Dispersion page into the main window.

Update Home startup behavior and associated test expectations.

Complete v0.4.0 feature development.

Record final full-suite test results.

Record manual GUI verification, if performed.

Record release tag and publication date, if published.

[0.3.0] — Mirror Optics

Status: Development Completed
Release Date: Not recorded

Added

Spherical mirror calculations supporting concave and convex mirrors.

Mirror image distance calculations using the spherical mirror equation.

Radius of curvature calculations from focal length.

Mirror magnification calculations.

Mirror image height calculations.

Classification of real and virtual mirror images.

Classification of upright and inverted images.

Image size classification: enlarged, reduced, and same size.

Mirror ray diagrams using Matplotlib.

Dedicated Mirror Optics calculator page.

Mirror Optics navigation in the application sidebar.

Mirror Optics feature card on the Home dashboard.

Keyboard shortcut Ctrl+5 for Mirror Optics.

Automated tests for mirror calculations, magnification, ray diagrams, and GUI functionality.

Changed

Updated the main application window to support six pages.

Expanded Home dashboard navigation to include Mirror Optics.

Updated page navigation shortcuts.

Extended theme handling to the Mirror Optics page.

Added persistent input settings for the mirror calculator.

Updated the project version to v0.3.0.

Reorganized documentation into version-specific sections.

Fixed

Updated magnification tests to reflect supported signed-distance and signed-height calculations.

Corrected test expectations for negative object distances and zero or negative object heights.

Testing

Mirror optics calculation tests passed.

Mirror magnification tests passed.

Mirror diagram tests passed.

Mirror calculator GUI tests passed.

Existing Optik unit tests passed during regression testing.

Release Preparation

Implement mirror optics calculations.

Implement mirror magnification.

Implement mirror ray diagrams.

Implement Mirror Optics GUI.

Integrate Mirror Optics into the main window.

Update Home dashboard navigation.

Run automated regression tests.

Complete manual GUI verification (not recorded).

Finalize documentation (not recorded).

Validate distributable executable, if applicable (not recorded).

Create Git version tag v0.3.0.

[0.2.0] — Thin Lens Optics

Status: Development Completed
Release Date: Not recorded

Added

Thin lens calculations using the thin lens equation.

Support for converging lenses.

Support for diverging lenses.

Image distance calculations.

Optical magnification calculations.

Image height calculations.

Image orientation classification.

Image size classification.

Thin lens ray diagrams.

Dedicated Thin Lens calculator page.

Thin Lens navigation in the sidebar.

Thin Lens feature card on the Home dashboard.

Reusable Matplotlib PlotManager for scientific visualization.

Plot export and refresh functionality.

Unit tests for thin lens calculations.

GUI tests for Thin Lens functionality.

Visualization tests for lens ray diagrams.

Changed

Expanded the main window to support Thin Lens Optics.

Updated the Home dashboard to display additional scientific modules.

Improved the organization of calculation and visualization modules.

Extended plotting functionality for reuse across optics modules.

Updated application documentation for thin lens functionality.

Fixed

Corrected issues identified during thin lens calculation and ray diagram testing.

Improved compatibility between plotting components and GUI pages.

Testing

Thin lens calculation tests completed.

Thin lens ray diagram tests completed.

GUI tests completed.

Existing reflection and refraction functionality checked during development.

[0.1.0] — Initial Release

Status: Completed
Release Date: Not recorded

Added

Initial Optik desktop application.

PySide6 graphical user interface.

Home dashboard.

Sidebar navigation.

Reflection calculator.

Refraction calculator.

Law of reflection calculations.

Snell's law calculations.

Critical angle calculations.

Total internal reflection detection.

Reflection ray diagrams.

Refraction ray diagrams.

Application Settings page.

Light and dark theme support.

Persistent application preferences.

Initial project architecture.

Unit testing using pytest.

GUI testing using pytest-qt.

Project documentation.

MIT License.

Changed

Established the modular architecture for separating optics calculations, visualizations, and GUI components.

Testing

Initial calculation tests completed.

Reflection and refraction GUI tests completed.

Ray diagram tests completed.

Initial application functionality verified.

Versioning Policy

Optik follows Semantic Versioning:

MAJOR.MINOR.PATCH

MAJOR: Incompatible API or significant architectural changes.

MINOR: New functionality added while maintaining compatibility where practical.

PATCH: Bug fixes and minor improvements.

During the 0.x.x development period, the project may introduce changes that are not backward-compatible.

Release versions are tagged in Git when published.

Release History Summary

Version

Release Focus

Status

v0.4.0

Prism Optics & Dispersion

Development Completed

v0.3.0

Mirror Optics

Development Completed

v0.2.0

Thin Lens Optics

Development Completed

v0.1.0

Reflection and Refraction

Completed

Optik — Exploring Optics and Photonics Through Scientific Computing.