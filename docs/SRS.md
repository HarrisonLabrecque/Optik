






Optik — Software Requirements Specification (SRS)
Project: Optik — Open-Source Optics & Photonics Desktop Application
Current Development Version: v0.4.0
Document Status: Maintained
License: MIT

1. Introduction
1.1 Purpose
This Software Requirements Specification (SRS) defines the functional and non-functional requirements for Optik, an open-source scientific desktop application developed using Python and PySide6.

Optik provides computational tools and graphical visualizations for studying optics and photonics.

This document establishes the core requirements of the application and maintains version-specific requirements for each software release.

1.2 Scope
Optik is designed to support:

Geometrical optics calculations.
Optical image formation analysis.
Prism optics and wavelength-dependent dispersion analysis.
Scientific visualization and ray diagrams.
Interactive desktop-based optical calculators.
Educational and engineering applications.
Future expansion into additional optics and photonics disciplines.
The application is intended for students, educators, researchers, engineers, and individuals interested in optical science.

1.3 Technology Overview
Component	Technology
Programming Language	Python
GUI Framework	PySide6
Scientific Computing	NumPy, SciPy
Visualization	Matplotlib
Unit Testing	pytest
GUI Testing	pytest-qt
Version Control	Git
Source Hosting	GitHub
1.4 Requirements Organization
Requirements are divided into two categories:

Core Requirements: Requirements that apply to the application across multiple releases.

Version-Specific Requirements: New functionality introduced in individual software versions.

Each requirement has a unique identifier to support traceability, implementation, and testing.

2. Core Functional Requirements
These requirements apply across Optik's supported calculation modules.

2.1 Application Interface
ID	Requirement
CORE-FR-001	The application shall provide a graphical desktop interface.
CORE-FR-002	The application shall provide navigation between supported calculation modules.
CORE-FR-003	The application shall display a Home dashboard.
CORE-FR-004	The application shall provide a Settings page.
CORE-FR-005	The application shall display the current software version.
CORE-FR-006	The application shall support light and dark themes.
CORE-FR-007	The application shall preserve supported user preferences between sessions.
2.2 Mathematical Calculations
ID	Requirement
CORE-FR-008	The application shall perform calculations using established optical equations.
CORE-FR-009	The application shall separate mathematical calculations from graphical interface components.
CORE-FR-010	The application shall display calculated results in a readable format.
CORE-FR-011	The application shall validate user inputs according to the applicable mathematical model.
CORE-FR-012	The application shall handle invalid mathematical operations without unexpectedly terminating.
2.3 Scientific Visualization
ID	Requirement
CORE-FR-013	The application shall provide ray diagrams for supported optical models.
CORE-FR-014	Ray diagrams shall represent the corresponding calculation results.
CORE-FR-015	Diagrams shall identify relevant optical components and reference points.
CORE-FR-016	The application shall support reusable visualization components where appropriate.
2.4 Application Testing
ID	Requirement
CORE-FR-017	Mathematical calculation modules shall have automated unit tests.
CORE-FR-018	Major graphical interface components shall have automated tests.
CORE-FR-019	New functionality shall be tested before release.
CORE-FR-020	Existing functionality shall be regression-tested after significant changes.
3. Non-Functional Requirements
3.1 Reliability
ID	Requirement
CORE-NFR-001	The application shall handle expected calculation errors without crashing.
CORE-NFR-002	Calculation results shall follow the documented equations and sign conventions.
CORE-NFR-003	Existing supported features shall remain functional following new feature integration.
3.2 Usability
ID	Requirement
CORE-NFR-004	The application shall provide clearly labeled input controls.
CORE-NFR-005	Calculation results shall be understandable to users familiar with introductory optics.
CORE-NFR-006	The interface shall provide consistent navigation between modules.
CORE-NFR-007	Supported themes shall maintain readable text and graphical elements.
3.3 Maintainability
ID	Requirement
CORE-NFR-008	Mathematical calculations shall be organized into independent modules.
CORE-NFR-009	GUI components shall be organized into reusable pages and widgets where appropriate.
CORE-NFR-010	Visualization logic shall remain separate from mathematical calculation logic.
CORE-NFR-011	The project shall use version control to track changes.
CORE-NFR-012	Project documentation shall be maintained for each release.
3.4 Portability
ID	Requirement
CORE-NFR-013	The application shall use Python and supported cross-platform libraries.
CORE-NFR-014	Platform-specific distribution packages shall be tested on their target operating systems before publication.
4. Version-Specific Requirements
The following sections define the functionality introduced during each development version. Historical requirements are preserved to maintain traceability.

4.1 Version 0.1.0 — Reflection and Refraction
Status: Completed

4.1.1 Reflection Requirements
ID	Requirement
V010-FR-001	The application shall calculate reflected angles using the law of reflection.
V010-FR-002	The application shall accept an incident angle as input.
V010-FR-003	The application shall display the calculated reflection angle.
V010-FR-004	The application shall generate a reflection ray diagram.
V010-FR-005	The reflection diagram shall display incident and reflected rays.
4.1.2 Refraction Requirements
ID	Requirement
V010-FR-006	The application shall calculate refracted angles using Snell's law.
V010-FR-007	The application shall accept refractive indices for two optical media.
V010-FR-008	The application shall accept an incident angle.
V010-FR-009	The application shall calculate critical angles where applicable.
V010-FR-010	The application shall identify total internal reflection conditions.
V010-FR-011	The application shall generate a refraction ray diagram.
4.1.3 Interface Requirements
ID	Requirement
V010-FR-012	The application shall provide Reflection and Refraction pages.
V010-FR-013	The application shall provide navigation through a sidebar.
V010-FR-014	The application shall provide a Home page.
V010-FR-015	The application shall provide a Settings page.
V010-FR-016	The application shall support persistent appearance preferences.
4.1.4 Verification
Verification shall include reflection calculation tests, Snell's law calculation tests, critical-angle tests, total internal reflection tests, ray diagram tests, and GUI tests.

4.2 Version 0.2.0 — Thin Lens Optics
Status: Development Completed

4.2.1 Thin Lens Calculations
ID	Requirement
V020-FR-001	The application shall calculate image distance using the thin lens equation.
V020-FR-002	The application shall support converging lenses.
V020-FR-003	The application shall support diverging lenses.
V020-FR-004	The application shall accept focal length and object distance as inputs.
V020-FR-005	The application shall classify real and virtual images.
V020-FR-006	The application shall handle image formation at infinity.
4.2.2 Magnification Requirements
ID	Requirement
V020-FR-007	The application shall calculate optical magnification.
V020-FR-008	The application shall calculate image height.
V020-FR-009	The application shall classify upright and inverted images.
V020-FR-010	The application shall classify enlarged, reduced, and same-size images.
4.2.3 Visualization Requirements
ID	Requirement
V020-FR-011	The application shall generate thin lens ray diagrams.
V020-FR-012	The diagrams shall distinguish converging and diverging lenses.
V020-FR-013	The diagrams shall identify focal points and relevant image positions.
V020-FR-014	The visualization system shall support reusable Matplotlib plotting components.
4.2.4 Interface Requirements
ID	Requirement
V020-FR-015	The application shall provide a dedicated Thin Lens page.
V020-FR-016	The sidebar shall provide navigation to the Thin Lens page.
V020-FR-017	The Home dashboard shall provide access to Thin Lens calculations.
4.2.5 Verification
Verification shall include thin lens equation tests, magnification tests, image classification tests, ray diagram tests, Thin Lens GUI tests, and regression testing of v0.1.0 functionality.

4.3 Version 0.3.0 — Mirror Optics
Status: Development Completed

4.3.1 Spherical Mirror Calculations
ID	Requirement
V030-FR-001	The application shall support concave spherical mirrors.
V030-FR-002	The application shall support convex spherical mirrors.
V030-FR-003	The application shall calculate image distance using the spherical mirror equation.
V030-FR-004	The application shall calculate radius of curvature from focal length.
V030-FR-005	The application shall classify mirrors based on focal length sign.
V030-FR-006	The application shall classify real and virtual mirror images.
V030-FR-007	The application shall handle images formed at infinity.
4.3.2 Mirror Magnification Requirements
ID	Requirement
V030-FR-008	The application shall calculate spherical mirror magnification.
V030-FR-009	The application shall calculate mirror image height.
V030-FR-010	The application shall classify image orientation.
V030-FR-011	The application shall classify image size.
4.3.3 Mirror Visualization Requirements
ID	Requirement
V030-FR-012	The application shall generate concave mirror ray diagrams.
V030-FR-013	The application shall generate convex mirror ray diagrams.
V030-FR-014	Ray diagrams shall identify the mirror, focal point, and center of curvature.
V030-FR-015	Ray diagrams shall represent real and virtual image formation.
V030-FR-016	Virtual ray extensions shall be visually distinguishable from physical rays.
V030-FR-017	The visualization shall update when calculation inputs change and the calculation is executed.
4.3.4 Mirror Calculator Interface
ID	Requirement
V030-FR-018	The application shall provide a dedicated Mirror Optics page.
V030-FR-019	Users shall be able to select concave or convex mirrors.
V030-FR-020	Users shall be able to enter focal length magnitude, object distance, and object height.
V030-FR-021	The interface shall display image distance, radius of curvature, magnification, and image height.
V030-FR-022	The interface shall display image type, orientation, and size classification.
V030-FR-023	The interface shall provide Calculate and Reset controls.
V030-FR-024	The interface shall preserve supported mirror input preferences.
V030-FR-025	The interface shall support light and dark themes.
4.3.5 Main Application Integration
ID	Requirement
V030-FR-026	The main window shall support six application pages.
V030-FR-027	The sidebar shall provide access to Mirror Optics.
V030-FR-028	The Home dashboard shall provide a Mirror Optics feature card.
V030-FR-029	The application shall support keyboard shortcuts for navigation between its six pages.
4.3.6 Verification Requirements
ID	Requirement
V030-TEST-001	Concave mirror calculations shall be tested.
V030-TEST-002	Convex mirror calculations shall be tested.
V030-TEST-003	Mirror magnification calculations shall be tested.
V030-TEST-004	Mirror ray diagrams shall be tested.
V030-TEST-005	Mirror calculator GUI behavior shall be tested.
V030-TEST-006	Existing Optik calculation modules shall undergo regression testing.
V030-TEST-007	Manual GUI verification shall be completed before release.
4.3.7 Verification Status
Automated unit testing and regression testing were completed successfully during v0.3.0 development. Manual GUI verification was listed as a release-preparation item; its completion is not recorded in the supplied requirements history.

4.3.8 Model Limitations
The v0.3.0 mirror module uses idealized spherical mirror equations under the paraxial approximation. Full non-paraxial ray tracing, spherical aberration analysis, diffraction, interference, and wave-optics simulations are outside its scope.

4.4 Version 0.4.0 — Prism Optics & Dispersion
Status: Development Completed

4.4.1 Prism Geometry and Refraction Requirements
ID	Requirement
V040-FR-001	The application shall calculate light refraction at the first prism surface using Snell's law.
V040-FR-002	The application shall calculate internal ray geometry and refraction at the second prism surface.
V040-FR-003	The application shall accept prism apex angle, incident angle, and applicable refractive index inputs.
V040-FR-004	The application shall calculate and display internal refraction angles.
V040-FR-005	The application shall calculate the emergent angle for a transmitted ray.
V040-FR-006	The application shall calculate total prism angular deviation.
V040-FR-007	The application shall calculate the minimum deviation angle when physically defined.
V040-FR-008	The application shall calculate the critical angle when applicable.
V040-FR-009	The application shall identify total internal reflection and prevent invalid transmitted-ray results.
V040-FR-010	The application shall validate prism geometry and optical input values.
4.4.2 Dispersion and Spectral Requirements
ID	Requirement
V040-FR-011	The application shall calculate wavelength-dependent refractive index using Cauchy's dispersion equation.
V040-FR-012	The application shall accept configurable Cauchy coefficients A, B, and C.
V040-FR-013	The application shall convert wavelength units consistently when evaluating the dispersion model.
V040-FR-014	The application shall calculate refractive indices across a selected wavelength range.
V040-FR-015	The application shall calculate wavelength-dependent prism deviation using the prism refraction model.
V040-FR-016	The application shall exclude wavelengths that do not produce valid transmitted rays from spectral deviation results.
V040-FR-017	The application shall report when no valid spectral deviation results can be produced.
V040-FR-018	The application shall reject invalid wavelength inputs and nonphysical refractive-index results according to the implemented model.
4.4.3 Visualization Requirements
ID	Requirement
V040-FR-019	The application shall provide a Prism Ray Diagram visualization mode.
V040-FR-020	The application shall provide a Refractive Index vs Wavelength graph.
V040-FR-021	The application shall provide a Prism Deviation vs Wavelength graph.
V040-FR-022	The application shall provide a Visible Spectrum visualization mode.
V040-FR-023	The prism calculator shall allow switching between visualization modes.
V040-FR-024	The visualizations shall represent calculation results and label relevant axes and optical quantities.
V040-FR-025	The visualization interface shall support figure export in available formats such as PNG, SVG, and PDF.
V040-FR-026	The visualization shall provide readable output under supported light and dark themes.
4.4.4 Prism Calculator Interface Requirements
ID	Requirement
V040-FR-027	The application shall provide a dedicated Prism Optics & Dispersion page.
V040-FR-028	The page shall expose prism geometry, wavelength, and dispersion coefficient inputs as applicable to the selected mode.
V040-FR-029	The page shall display calculated optical results and user-readable validation messages.
V040-FR-030	The page shall provide controls for calculation and resetting supported inputs.
V040-FR-031	The page shall preserve supported prism and dispersion input preferences between sessions.
4.4.5 Main Application Integration and Persistence
ID	Requirement
V040-FR-032	The main window shall support seven pages: Home, Reflection, Refraction, Thin Lenses, Mirror Optics, Prism Optics & Dispersion, and Settings.
V040-FR-033	The sidebar shall provide navigation to Prism Optics & Dispersion at page index 5.
V040-FR-034	The application shall provide Ctrl+6 for Prism Optics & Dispersion and Ctrl+7 for Settings.
V040-FR-035	The application shall always open on the Home page at startup, regardless of the previously selected page.
V040-FR-036	The application shall preserve the appearance theme without restoring the previously visited page.
V040-FR-037	The main window shall synchronize the active page, sidebar selection, and navigation signals.
Change to previous requirements: V040-FR-032 and V040-FR-034 supersede the six-page navigation scope of V030-FR-026 and V030-FR-029. The Home-first startup behavior in V040-FR-035 supersedes any earlier implementation that restored the last visited page; persistent appearance preferences required by CORE-FR-007 and V010-FR-016 remain supported.

4.4.6 Testing and Verification Requirements
ID	Requirement
V040-TEST-001	Prism refraction, deviation, minimum deviation, and critical-angle calculations shall be tested against known numerical cases.
V040-TEST-002	Total internal reflection and invalid prism geometry shall be tested.
V040-TEST-003	Cauchy refractive-index calculations shall be tested using documented wavelength units and coefficients.
V040-TEST-004	Spectral dispersion and spectral prism deviation shall be tested, including cases with no transmitted rays.
V040-TEST-005	Each of the four visualization modes shall be tested for successful rendering and appropriate labeling.
V040-TEST-006	The Prism Optics & Dispersion page shall undergo GUI testing for inputs, results, mode switching, and errors.
V040-TEST-007	Main window tests shall verify seven-page navigation, shortcuts, and sidebar synchronization.
V040-TEST-008	Main window tests shall verify Home-first startup even when legacy last-page settings exist.
V040-TEST-009	Theme persistence and supported prism input persistence shall be tested.
V040-TEST-010	Existing reflection, refraction, lens, and mirror modules shall undergo regression testing.
V040-TEST-011	Manual GUI verification shall be performed before publication.
4.4.7 Verification Status
The v0.4.0 feature implementation is complete. Main window tests were revised to match Home-first startup behavior. The supplied documentation does not record a final full-suite regression result or completed release publication, so these are not asserted here.

4.4.8 Model Limitations
Prism calculations use idealized geometrical optics with air as the surrounding medium.
Cauchy's equation is applicable within the fitted wavelength range for the selected material; arbitrary coefficients may produce unrealistic refractive indices.
Spectral deviation results exclude wavelengths without a valid transmitted ray.
The current prism model does not include diffraction, interference, polarization, absorption, or advanced multi-element prism assemblies.
5. Requirements Traceability
Requirements shall be traceable to their corresponding software modules and tests.

Requirement Area	Primary Module	Test Area
Reflection	optics/reflection.py	Reflection tests
Refraction	optics/refraction.py	Refraction tests
Thin Lens Optics	optics/thin_lens.py	Thin lens tests
Magnification	optics/magnification.py	Magnification tests
Mirror Optics	optics/mirrors.py	Mirror calculation tests
Mirror Magnification	optics/mirror_magnification.py	Mirror magnification tests
Mirror Visualization	visualization/mirror_diagram.py	Mirror diagram tests
Mirror GUI	ui/pages/mirror_page.py	Mirror page tests
Prism Optics	optics/prisms.py	Prism calculation tests
Dispersion and Spectral Prism Calculations	optics/dispersion.py	Dispersion and spectral deviation tests
Prism Visualization	visualization/prism_diagram.py, visualization/dispersion_diagram.py	Prism and dispersion visualization tests
Prism GUI	ui/pages/prism_page.py	Prism page tests
Main Navigation	ui/main_window.py	Main window tests
Module paths should be updated if the project architecture changes.

6. Requirements Maintenance Policy
Optik uses version-based requirements documentation.

6.1 Adding New Requirements
Each future software release shall receive a new section containing:

Version identifier.
Release title.
Development status.
Functional requirements.
Visualization requirements, when applicable.
Interface requirements.
Testing and verification requirements.
Known limitations.
6.2 Requirement Identification
Requirements shall use the following naming convention: VXYZ-FR-NNN.

XYZ identifies the software version.
FR identifies a functional requirement.
NNN identifies the requirement number.
Testing requirements use the TEST designation.

6.3 Modifying Existing Requirements
Historical requirements should not be silently removed or rewritten.

If a requirement changes, the new version shall identify:

The original requirement ID.
The reason for the change.
The new or replacement requirement.
Any compatibility implications.
6.4 Verification
Requirements should be verified through appropriate combinations of automated unit testing, GUI testing, integration testing, regression testing, and manual application verification.

7. Document Revision History
Document Revision	Software Version	Description
1.0	v0.1.0	Initial reflection and refraction requirements
1.1	v0.2.0	Added thin lens optics requirements
1.2	v0.3.0	Added mirror optics requirements and versioned documentation structure
1.3	v0.4.0	Added prism optics, dispersion, visualization, and Home-first navigation requirements
End of Software Requirements Specification

