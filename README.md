# Optik

**Open-Source Optics & Photonics Desktop Application**

Optik is an open-source scientific desktop application developed using Python and PySide6. It provides interactive tools for studying, calculating, and visualizing optical phenomena.

The project is designed for students, educators, researchers, engineers, and anyone interested in optics and photonics.

Optik combines mathematical calculations with interactive graphical interfaces and ray diagrams to make geometrical optics easier to explore.

## Project Information

| Property | Description |
|---|---|
| Project Name | Optik |
| Current Development Version | v0.3.0 |
| Application Type | Scientific Desktop Application |
| Programming Language | Python |
| GUI Framework | PySide6 |
| Visualization | Matplotlib |
| Testing | pytest, pytest-qt |
| License | MIT |
| Development Model | Open Source |

## Features

Optik currently includes the following optical calculation modules:

- **Reflection:** Calculate reflected angles using the law of reflection and visualize incident and reflected rays.
- **Refraction:** Apply Snell's law, calculate refracted angles and critical angles, and investigate total internal reflection.
- **Thin Lens Optics:** Calculate image distance, magnification, image height, and image characteristics for converging and diverging lenses.
- **Mirror Optics:** Calculate image formation, magnification, radius of curvature, and image characteristics for concave and convex spherical mirrors.
- **Scientific Visualization:** Generate ray diagrams to illustrate optical calculations.
- **Application Settings:** Configure supported appearance preferences, including light and dark themes.

## Installation

### Requirements

- Python 3.11 or newer, subject to compatibility with the installed dependencies
- PySide6
- NumPy
- SciPy
- Matplotlib
- pytest and pytest-qt for development and testing

### Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Optik.git
cd Optik
```

Replace `YOUR_USERNAME` with the repository owner's GitHub username.

### Create a Virtual Environment

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

### Install Dependencies

If the repository includes a `requirements.txt` file:

```bash
python -m pip install -r requirements.txt
```

### Run Optik

From the project root directory:

```bash
python -m app.main_window
```

## Application Navigation

Optik provides a sidebar with access to its primary scientific modules.

| Page | Description | Shortcut |
|---|---|---|
| Home | Application dashboard | Ctrl+1 |
| Reflection | Law of reflection calculator | Ctrl+2 |
| Refraction | Snell's law and critical-angle calculator | Ctrl+3 |
| Thin Lenses | Lens calculations and ray diagrams | Ctrl+4 |
| Mirror Optics | Concave and convex mirror calculations | Ctrl+5 |
| Settings | Application preferences | Ctrl+6 |

## Testing

Optik uses pytest for mathematical unit tests and pytest-qt for graphical interface testing.

Run the complete test suite:

```bash
python -m pytest tests/ -v
```

Run a specific module:

```bash
python -m pytest tests/test_mirrors.py -v
```

Run the test discovery check:

```bash
python -m pytest --collect-only -q
```

Regression testing is performed by rerunning the existing test suite after implementing new features. Manual GUI verification is also recommended before each release.

---

# Development and Release History

This section is maintained chronologically. Each new release adds a new version section while preserving the history of previous releases.

## Version 0.1.0 — Initial Optics Release

**Status:** Completed

### Overview

Version 0.1.0 established the foundation of the Optik desktop application.

### Features Introduced

- Reflection calculations using the law of reflection.
- Refraction calculations using Snell's law.
- Critical-angle calculations.
- Total internal reflection detection.
- Reflection and refraction ray diagrams.
- Home dashboard and sidebar navigation.
- Application settings and theme support.
- Initial automated unit and GUI tests.

### Technical Foundation

- Python calculation modules.
- PySide6 graphical interface.
- Matplotlib-based ray visualization.
- Modular application architecture.
- pytest and pytest-qt testing.

---

## Version 0.2.0 — Thin Lens Optics

**Status:** Development completed

### Overview

Version 0.2.0 expanded Optik to include geometrical optics calculations for thin lenses.

### Features Introduced

- Thin lens equation calculations.
- Converging lens support.
- Diverging lens support.
- Image distance calculations.
- Optical magnification.
- Image height calculations.
- Image orientation classification.
- Image size classification.
- Thin lens ray diagrams.
- Dedicated Thin Lens calculator page.

### Visualization Improvements

A reusable Matplotlib-based plotting system was developed to support scientific visualization across optical modules.

The plotting functionality supports capabilities such as diagram rendering, refresh, and export where implemented by the relevant module.

### Interface Improvements

- Thin Lens navigation added to the application.
- Home dashboard expanded with Thin Lens functionality.
- Additional calculation results displayed in the GUI.
- Continued light and dark theme support.

### Testing

Unit tests and GUI tests were developed for thin lens calculations and visualization.

---

## Version 0.3.0 — Mirror Optics

**Status:** In Development

### Overview

Version 0.3.0 expands Optik with spherical mirror calculations and visualization.

The new module supports both concave and convex mirrors and uses the spherical mirror equation to determine image formation.

### Features Introduced

- Concave spherical mirror calculations.
- Convex spherical mirror calculations.
- Mirror focal length and radius of curvature relationships.
- Mirror image distance calculations.
- Mirror magnification calculations.
- Mirror image height calculations.
- Real and virtual image classification.
- Upright and inverted image classification.
- Enlarged, reduced, and same-size image classification.
- Mirror ray diagrams.
- Dedicated Mirror Optics calculator page.

### Application Improvements

- Mirror Optics added to the sidebar.
- Mirror Optics added to the Home dashboard.
- Navigation shortcuts expanded to six pages.
- Main window updated for the new calculator.
- Mirror calculator settings persistence.
- Light and dark theme integration.

### Testing and Validation

The automated unit test suite has passed, including the mirror optics tests and existing calculation tests.

The following checks remain part of release preparation:

- Complete manual GUI verification.
- Documentation review.
- Windows executable packaging and validation, if distributed.
- Final release commit and GitHub tag.

### Known Limitations

- The mirror module uses the paraxial approximation for ideal spherical mirrors.
- The diagrams represent idealized geometrical optics rather than full physical ray tracing.
- Wave-optics effects and optical aberration analysis are outside the current mirror module's scope.

---

## Future Releases

Future Optik versions may introduce additional optics and photonics calculations, improved visualization, and more advanced scientific simulation capabilities.

Specific features and release dates will be documented when their scope is established.

### Documentation Update Policy

Starting with v0.3.0, Optik follows a versioned documentation approach:

1. Preserve previous release history.
2. Add a new version section for each subsequent release.
3. Document new features, improvements, and limitations under that version.
4. Update general installation and usage instructions when necessary.
5. Correct or clearly supersede outdated information without silently rewriting historical release records.

For example, when v0.4.0 is developed, append:

```markdown
## Version 0.4.0 — Release Title

**Status:** In Development

### Overview

### Features Introduced

### Application Improvements

### Testing and Validation

### Known Limitations
```

---

## Additional Documentation

Detailed project documentation is available in the `docs/` directory:

- **SRS.md:** Software Requirements Specification.
- **SDD.md:** Software Design Document.
- **USER_GUIDE.md:** Instructions for using Optik.
- **DEVELOPMENT.md:** Development workflow, implementation notes, and testing practices.

Release changes are recorded in `CHANGELOG.md`.

## Contributing

Optik is an open-source project. Contributions, bug reports, feature suggestions, documentation improvements, and test enhancements are welcome.

Before submitting a pull request:

1. Review the project structure and development documentation.
2. Create a branch for your changes.
3. Add or update tests where appropriate.
4. Run the complete test suite.
5. Describe the changes clearly in your pull request.

## License

Optik is distributed under the MIT License.

See the `LICENSE` file for the full license text.

---

**Optik — Exploring Optics and Photonics Through Scientific Computing.**