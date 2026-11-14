# Changelog

All notable changes to **Optik — Open-Source Optics & Photonics Desktop Application** are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project follows [Semantic Versioning](https://semver.org/).

## Changelog Maintenance Policy

Each release has its own section. Previous release entries are preserved, except for factual corrections.

Changes are organized under the following categories when applicable:

- **Added:** New features, modules, and functionality.
- **Changed:** Updates to existing features or behavior.
- **Fixed:** Corrections to bugs and errors.
- **Deprecated:** Features scheduled for removal.
- **Removed:** Features removed from the application.
- **Security:** Security-related changes.

During development, changes are recorded under the upcoming version. When the release is published, its status is updated and the release date is added.

---

## [0.3.0] — Mirror Optics

**Status:** In Development  
**Release Date:** TBD

### Added

- Spherical mirror calculations supporting concave and convex mirrors.
- Mirror image distance calculations using the spherical mirror equation.
- Radius of curvature calculations from focal length.
- Mirror magnification calculations.
- Mirror image height calculations.
- Classification of real and virtual mirror images.
- Classification of upright and inverted images.
- Image size classification: enlarged, reduced, and same size.
- Mirror ray diagrams using Matplotlib.
- Dedicated Mirror Optics calculator page.
- Mirror Optics navigation in the application sidebar.
- Mirror Optics feature card on the Home dashboard.
- Keyboard shortcut `Ctrl+5` for Mirror Optics.
- Automated tests for mirror calculations, magnification, ray diagrams, and GUI functionality.

### Changed

- Updated the main application window to support six pages.
- Expanded Home dashboard navigation to include Mirror Optics.
- Updated page navigation shortcuts.
- Extended theme handling to the Mirror Optics page.
- Added persistent input settings for the mirror calculator.
- Updated the project version to v0.3.0.
- Reorganized documentation into version-specific sections.

### Fixed

- Updated magnification tests to reflect supported signed-distance and signed-height calculations.
- Corrected test expectations for negative object distances and zero or negative object heights.

### Testing

- Mirror optics calculation tests passed.
- Mirror magnification tests passed.
- Mirror diagram tests passed.
- Mirror calculator GUI tests passed.
- Existing Optik unit tests passed during regression testing.

### Release Preparation

- [x] Implement mirror optics calculations.
- [x] Implement mirror magnification.
- [x] Implement mirror ray diagrams.
- [x] Implement Mirror Optics GUI.
- [x] Integrate Mirror Optics into the main window.
- [x] Update Home dashboard navigation.
- [x] Run automated regression tests.
- [ ] Complete manual GUI verification.
- [ ] Finalize documentation.
- [ ] Validate distributable executable, if applicable.
- [ ] Create GitHub release and version tag.

---

## [0.2.0] — Thin Lens Optics

**Status:** Development Completed  
**Release Date:** Not recorded

### Added

- Thin lens calculations using the thin lens equation.
- Support for converging lenses.
- Support for diverging lenses.
- Image distance calculations.
- Optical magnification calculations.
- Image height calculations.
- Image orientation classification.
- Image size classification.
- Thin lens ray diagrams.
- Dedicated Thin Lens calculator page.
- Thin Lens navigation in the sidebar.
- Thin Lens feature card on the Home dashboard.
- Reusable Matplotlib PlotManager for scientific visualization.
- Plot export and refresh functionality.
- Unit tests for thin lens calculations.
- GUI tests for Thin Lens functionality.
- Visualization tests for lens ray diagrams.

### Changed

- Expanded the main window to support Thin Lens Optics.
- Updated the Home dashboard to display additional scientific modules.
- Improved the organization of calculation and visualization modules.
- Extended plotting functionality for reuse across optics modules.
- Updated application documentation for thin lens functionality.

### Fixed

- Corrected issues identified during thin lens calculation and ray diagram testing.
- Improved compatibility between plotting components and GUI pages.

### Testing

- Thin lens calculation tests completed.
- Thin lens ray diagram tests completed.
- GUI tests completed.
- Existing reflection and refraction functionality checked during development.

---

## [0.1.0] — Initial Release

**Status:** Completed  
**Release Date:** Not recorded

### Added

- Initial Optik desktop application.
- PySide6 graphical user interface.
- Home dashboard.
- Sidebar navigation.
- Reflection calculator.
- Refraction calculator.
- Law of reflection calculations.
- Snell's law calculations.
- Critical angle calculations.
- Total internal reflection detection.
- Reflection ray diagrams.
- Refraction ray diagrams.
- Application Settings page.
- Light and dark theme support.
- Persistent application preferences.
- Initial project architecture.
- Unit testing using pytest.
- GUI testing using pytest-qt.
- Project documentation.
- MIT License.

### Changed

- Established the modular architecture for separating optics calculations, visualizations, and GUI components.

### Testing

- Initial calculation tests completed.
- Reflection and refraction GUI tests completed.
- Ray diagram tests completed.
- Initial application functionality verified.

---

## Future Release Template

Copy this section to the top of the release history when beginning a new version.

```markdown
## [X.Y.Z] — Release Title

**Status:** In Development
**Release Date:** TBD

### Added

### Changed

### Fixed

### Deprecated

### Removed

### Security

### Testing

### Release Preparation

- [ ] Implement planned features.
- [ ] Complete unit tests.
- [ ] Complete regression testing.
- [ ] Complete manual GUI verification.
- [ ] Update documentation.
- [ ] Prepare release.
```

Only include categories that apply to the release.

---

## Versioning Policy

Optik follows Semantic Versioning:

**MAJOR.MINOR.PATCH**

- **MAJOR:** Incompatible API or significant architectural changes.
- **MINOR:** New functionality added while maintaining compatibility where practical.
- **PATCH:** Bug fixes and minor improvements.

During the `0.x.x` development period, the project may introduce changes that are not backward-compatible.

Release versions are tagged in Git when published.

## Release History Summary

| Version | Release Focus | Status |
|---|---|---|
| v0.3.0 | Mirror Optics | In Development |
| v0.2.0 | Thin Lens Optics | Development Completed |
| v0.1.0 | Reflection and Refraction | Completed |

---

**Optik — Exploring Optics and Photonics Through Scientific Computing.**