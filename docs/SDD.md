
















Optik — Software Design Document (SDD)
Project: Optik — Open-Source Optics & Photonics Desktop Application
Current Development Version: v0.4.0
Document Status: Maintained
License: MIT
Primary Language: Python
GUI Framework: PySide6

1. Introduction
1.1 Purpose
This Software Design Document (SDD) describes the architecture, components, interfaces, mathematical models, and implementation strategy of Optik.

Optik is a modular scientific desktop application designed to perform optical calculations and generate graphical representations of optical phenomena. This document establishes the application's core architecture and records design additions introduced in each software version.

1.2 Design Objectives
Optik is designed to:

Separate scientific calculations from GUI components.
Provide reusable scientific visualization tools.
Support incremental feature development.
Maintain independently testable modules.
Provide a consistent graphical interface.
Support future expansion into additional optics and photonics disciplines.
Preserve architectural history between releases.
1.3 Technology Stack
Component	Technology
Programming Language	Python
GUI Framework	PySide6
Scientific Computing	NumPy, SciPy
Scientific Visualization	Matplotlib
Automated Testing	pytest
GUI Testing	pytest-qt
Version Control	Git
Repository Hosting	GitHub
Windows Packaging	PyInstaller, when applicable
2. Core System Architecture
2.1 Architectural Overview
Optik follows a modular, layered architecture. The application separates presentation, scientific calculations, visualization, and application configuration.

+----------------------------------------------------------+
|                      Optik Desktop                       |
+----------------------------------------------------------+
| Presentation Layer                                       |
| MainWindow | HomePage | Calculator Pages | SettingsPage   |
| Navigation | Input Controls                              |
+----------------------------------------------------------+
| Scientific Logic Layer                                   |
| Reflection | Refraction | Thin Lenses | Mirrors | Prisms  |
| Magnification | Image Classification | Dispersion        |
+----------------------------------------------------------+
| Visualization Layer                                      |
| Reflection | Refraction | Lens | Mirror | Prism Diagrams |
| Dispersion Graphs | PlotManager                          |
+----------------------------------------------------------+
| Application Services                                     |
| QSettings | Themes | Configuration | Export              |
+----------------------------------------------------------+
Scientific calculation modules should remain independent of GUI widgets. GUI components coordinate user input, calculation execution, and visualization.

2.2 Architectural Principles
Separation of Concerns: Scientific modules perform calculations; visualization modules construct optical diagrams; GUI pages collect inputs and display results; the main window manages navigation; settings components manage preferences.

Modularity: New optics modules should be introduced without extensive changes to existing calculation modules.

Reusability: Shared mathematical and visualization functionality should be implemented in reusable components where practical.

Testability: Scientific calculations should be testable without launching the graphical interface. GUI functionality should be tested using pytest-qt.

3. Project Directory Structure
The following structure represents the primary organization of Optik through v0.4.0. Names of additional helper and test modules may vary by implementation.

Optik/
├── app/
│   ├── __init__.py
│   └── [Application entry point, if used]
├── optics/
│   ├── __init__.py
│   ├── reflection.py
│   ├── refraction.py
│   ├── thin_lens.py
│   ├── magnification.py
│   ├── mirrors.py
│   ├── mirror_magnification.py
│   ├── prisms.py                  # v0.4.0
│   └── dispersion.py              # v0.4.0
├── visualization/
│   ├── __init__.py
│   ├── reflection_diagram.py
│   ├── refraction_diagram.py
│   ├── lens_diagram.py
│   ├── mirror_diagram.py
│   ├── prism_diagram.py            # v0.4.0
│   └── dispersion_diagram.py       # v0.4.0
├── ui/
│   ├── __init__.py
│   ├── main_window.py              # Current MainWindow implementation
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── home_page.py
│   │   ├── reflection_page.py
│   │   ├── refraction_page.py
│   │   ├── lens_page.py
│   │   ├── mirror_page.py
│   │   ├── prism_page.py           # v0.4.0
│   │   └── settings_page.py
│   └── widgets/
│       └── [Reusable GUI widgets]
├── tests/
│   ├── test_reflection.py
│   ├── test_refraction.py
│   ├── test_thin_lens.py
│   ├── test_magnification.py
│   ├── test_mirrors.py
│   ├── test_mirror_magnification.py
│   ├── test_mirror_diagram.py
│   ├── test_mirror_page.py
│   ├── test_main_window.py
│   └── [Prism, dispersion, visualization, and other tests]
├── docs/
│   ├── SRS.md
│   ├── SDD.md
│   ├── USER_GUIDE.md
│   ├── DEVELOPMENT.md
│   └── screenshots/
├── README.md
├── CHANGELOG.md
├── LICENSE
└── requirements.txt
The structure may be extended as additional optical modules are introduced.

4. Core Component Design
4.1 Main Application Window
Module: ui/main_window.py
Class: MainWindow

The main window creates the application interface, initializes calculator pages, manages sidebar navigation and the stacked page container, applies themes, maintains keyboard shortcuts, and restores supported preferences.

Page Management
Optik uses QStackedWidget to manage seven pages in v0.4.0:

Index	Page	Shortcut
0	Home	Ctrl+1
1	Reflection	Ctrl+2
2	Refraction	Ctrl+3
3	Thin Lenses	Ctrl+4
4	Mirror Optics	Ctrl+5
5	Prism Optics & Dispersion	Ctrl+6
6	Settings	Ctrl+7
Navigation
navigate_to(index: int)
This method updates the active page and sidebar selection. The Home dashboard emits a navigation signal handled by the main window. Navigation emits page_changed for observers.

Startup behavior (v0.4.0): Every application launch selects Home (index 0), regardless of the page visited during the previous session. The last selected page is no longer persisted by the main window.

4.2 Home Dashboard
Module: ui/pages/home_page.py
Classes: HomePage, FeatureCard

The Home dashboard provides entry points to Optik's calculation modules. Each feature card contains a module title, description, Open Calculator button, and destination page index.

navigate_to = Signal(int)
The signal communicates the selected destination to the main window. v0.4.0 includes the Prism Optics & Dispersion destination.

4.3 Settings Management
Optik uses PySide6 QSettings to preserve supported application preferences. Examples include:

appearance/theme
mirror/type
mirror/focal_length
mirror/object_distance
mirror/object_height
[Prism calculator parameters and dispersion coefficients]
Individual calculator pages restore their supported inputs when initialized. In v0.4.0, historical keys such as window/last_page and window/last_page_name do not determine startup navigation and are not written by current main-window navigation.

4.4 Theme Management
The application supports light and dark themes. The main window exposes:

set_theme(theme: str)
Pages implementing compatible set_theme() methods receive theme updates. The Prism page supports dark-mode propagation through set_dark_mode(bool). Visualization components may require additional styling to maintain readability.

5. Scientific Calculation Architecture
5.1 Calculation Module Responsibilities
Scientific calculation modules should:

Accept numerical inputs.
Validate inputs according to the mathematical model.
Perform the required calculations.
Return numerical results or structured result objects.
Raise appropriate exceptions for invalid operations.
Calculation modules should not directly create or manipulate PySide6 widgets.

5.2 Numerical Conventions
Optik uses documented sign conventions for optical calculations. Sign conventions must be consistent between mathematical equations, returned results, GUI labels, ray diagram coordinates, and automated tests. Different optical models may use different conventions, documented in their respective modules.

Angles are expressed in degrees at the application-facing prism calculation interface; wavelengths supplied to the dispersion interface are in nanometers and converted to micrometers for Cauchy's equation.

5.3 Error Handling
Expected invalid input conditions should be handled through appropriate exceptions. GUI pages should display user-readable error messages rather than allowing expected calculation errors to terminate the application. Spectral calculations must distinguish valid transmitted rays from wavelengths at which no transmitted solution exists.

6. Visualization Architecture
6.1 Matplotlib Integration
Optik uses Matplotlib for optical diagrams. Visualization modules construct scientific figures independently of GUI layout. PySide6 pages embed Matplotlib figures using FigureCanvasQTAgg or equivalent Qt-compatible canvases.

6.2 Reusable Plotting Components
Reusable plotting functionality may include figure creation, axis configuration, plot clearing, diagram refresh, theme adaptation, and figure export. The PlotManager introduced during v0.2.0 provides a foundation for reusable visualization. Individual pages may also embed Matplotlib figures directly.

The v0.4.0 Prism page uses a shared figure/canvas to switch between prism ray geometry, dispersion curves, deviation curves, and visible-spectrum displays.

6.3 Diagram Design Principles
Optical diagrams should represent the mathematical model, identify components and reference points, distinguish ray paths, maintain readable labels, and handle special mathematical cases appropriately. Graphs should not silently present invalid or non-transmitting wavelengths as physically valid transmitted rays.

7. Version-Specific Design History
The following sections document architectural and implementation changes introduced by each development version.

7.1 Version 0.1.0 — Reflection and Refraction
Status: Completed

7.1.1 Overview
Version 0.1.0 established Optik's initial scientific calculation and visualization architecture.

7.1.2 Reflection Module
Module: optics/reflection.py

The reflection module implements the law of reflection:

θ
r
=
θ
i
θ 
r
​
 =θ 
i
​
 
Here, 
θ
r
θ 
r
​
  is the reflected angle and 
θ
i
θ 
i
​
  is the incident angle, both measured relative to the surface normal.

7.1.3 Refraction Module
Module: optics/refraction.py

The refraction module implements Snell's law:

n
1
sin
⁡
(
θ
1
)
=
n
2
sin
⁡
(
θ
2
)
n 
1
​
 sin(θ 
1
​
 )=n 
2
​
 sin(θ 
2
​
 )
Here, 
n
1
n 
1
​
  and 
n
2
n 
2
​
  are the refractive indices of the two media, and 
θ
1
θ 
1
​
  and 
θ
2
θ 
2
​
  are incident and refracted angles. The module also supports critical-angle calculations and total internal reflection detection.

7.1.4 Visualization Components
Version 0.1.0 introduced reflection and refraction ray diagrams representing incident, reflected, and refracted rays according to calculated optical behavior.

7.1.5 GUI Components
Initial pages included Home, Reflection, Refraction, and Settings. The interface established modular navigation and persistent settings.

7.1.6 Testing
Testing covered reflection, refraction, critical angles, total internal reflection, ray diagrams, and GUI functionality.

7.2 Version 0.2.0 — Thin Lens Optics
Status: Development Completed

7.2.1 Overview
Version 0.2.0 extended the scientific architecture to support geometrical image formation using thin lenses.

7.2.2 Thin Lens Calculation Module
Module: optics/thin_lens.py

The module implements the thin lens equation:

1
f
=
1
d
o
+
1
d
i
f
1
​
 = 
d 
o
​
 
1
​
 + 
d 
i
​
 
1
​
 
Here, 
f
f is focal length, 
d
o
d 
o
​
  object distance, and 
d
i
d 
i
​
  image distance. The module supports converging and diverging lenses.

7.2.3 Magnification Module
Module: optics/magnification.py

m
=
−
d
i
d
o
,
h
i
=
m
h
o
m=− 
d 
o
​
 
d 
i
​
 
​
 ,h 
i
​
 =mh 
o
​
 
Here, 
m
m is magnification, 
h
i
h 
i
​
  image height, and 
h
o
h 
o
​
  object height. The module supports signed numerical values according to implemented conventions.

7.2.4 Lens Visualization
Module: visualization/lens_diagram.py

The module illustrates converging/diverging lenses, principal rays, object and image positions, focal points, and real/virtual image formation.

7.2.5 PlotManager
Version 0.2.0 introduced reusable Matplotlib plotting functionality, reducing duplication between optical modules.

7.2.6 Thin Lens GUI
Module: ui/pages/lens_page.py

The page provides optical inputs, calculation execution, image properties, embedded ray diagrams, and theme-aware presentation.

7.2.7 Testing
Tests were developed for thin lens equations, magnification, image classification, diagrams, and GUI behavior.

7.3 Version 0.3.0 — Mirror Optics
Status: Development Completed

7.3.1 Overview
Version 0.3.0 introduced spherical mirror calculations and visualization, maintaining separation between calculations, diagrams, and GUI components.

7.3.2 Mirror Calculation Module
Module: optics/mirrors.py
Primary Result Structure: MirrorResult

The module supports concave and convex mirrors, image distance, radius of curvature, mirror type, real/virtual image classification, and image formation at infinity.

Spherical mirror equation:

1
f
=
1
d
o
+
1
d
i
f
1
​
 = 
d 
o
​
 
1
​
 + 
d 
i
​
 
1
​
 
Radius of curvature:

R
=
2
f
R=2f
Sign convention:

Quantity	Convention
Positive focal length	Concave mirror
Negative focal length	Convex mirror
Positive image distance	Real image
Negative image distance	Virtual image
Positive object distance	Real object in front of mirror
The calculation module validates numerical inputs and handles special mathematical conditions.

7.3.3 Mirror Magnification Module
Module: optics/mirror_magnification.py
Primary Result Structure: MirrorMagnificationResult

The module calculates magnification, image height, orientation, and size classification:

m
=
−
d
i
d
o
,
h
i
=
m
h
o
m=− 
d 
o
​
 
d 
i
​
 
​
 ,h 
i
​
 =mh 
o
​
 
Images are classified as upright/inverted and enlarged/reduced/same-size. At image formation at infinity, finite magnification is undefined.

7.3.4 Mirror Visualization Module
Module: visualization/mirror_diagram.py
Class: MirrorDiagram

The diagram includes the spherical mirror, principal axis, focal point, center of curvature, object and image arrows, incident and reflected rays, and virtual extensions.

draw(focal_length, object_distance, object_height)
clear()
save(filename, dpi=150)
The diagram uses mirror calculation results to determine geometry and supplies a Matplotlib figure for embedding.

7.3.5 Mirror GUI Module
Module: ui/pages/mirror_page.py
Class: MirrorPage

Inputs: Mirror type, focal length magnitude, object distance, object height.

Outputs: Mirror type, image distance, radius of curvature, magnification, image height, classification, orientation, size.

Controls: Calculate, Reset, Matplotlib navigation toolbar.

The page persists supported inputs using QSettings.

7.3.6 Main Window Integration
In v0.3.0, the main window expanded from five to six pages. Mirror Optics was assigned index 4, and Settings moved to index 5. The Home dashboard's navigation signal was connected to the main window.

7.3.7 Home Dashboard Integration
A Mirror Optics feature card was added to ui/pages/home_page.py, emitting the destination index when opened.

7.3.8 Theme Integration
The MirrorPage supports light/dark themes. Matplotlib figures require separate theme-aware styling for backgrounds, axes, and labels.

7.3.9 Testing Architecture
Module	Test File
Mirror calculations	tests/test_mirrors.py
Mirror magnification	tests/test_mirror_magnification.py
Mirror diagrams	tests/test_mirror_diagram.py
Mirror GUI	tests/test_mirror_page.py
The complete automated regression suite passed during v0.3.0 development. Manual GUI verification remained part of release preparation.

7.3.10 Design Limitations
The mirror module uses the paraxial approximation. Full non-paraxial ray tracing, spherical aberration, diffraction, interference, and wave-optics mirror modeling were outside the v0.3.0 scope.

7.4 Version 0.4.0 — Prism Optics & Dispersion
Status: Development Completed

7.4.1 Overview
Version 0.4.0 adds prism refraction and wavelength-dependent optical dispersion. The design separates prism geometry, material dispersion, visualization, and GUI orchestration so that numerical models can be tested without the desktop interface.

7.4.2 Prism Calculation Module
Module: optics/prisms.py

The module evaluates refraction at the entry and exit faces of an idealized prism. For a prism apex angle 
A
p
A 
p
​
 , incident angle 
i
i, internal angles 
r
1
r 
1
​
  and 
r
2
r 
2
​
 , and emergent angle 
e
e:

sin
⁡
r
1
=
sin
⁡
i
n
,
r
1
+
r
2
=
A
p
sinr 
1
​
 = 
n
sini
​
 ,r 
1
​
 +r 
2
​
 =A 
p
​
 
sin
⁡
e
=
n
sin
⁡
r
2
sine=nsinr 
2
​
 
Here, 
n
n is the prism's refractive index relative to surrounding air. A transmitted emergent ray requires 
∣
n
sin
⁡
r
2
∣
≤
1
∣nsinr 
2
​
 ∣≤1. The total angular deviation is:

δ
=
i
+
e
−
A
p
δ=i+e−A 
p
​
 
At the symmetric minimum-deviation condition:

δ
min
⁡
=
2
arcsin
⁡
 ⁣
(
n
sin
⁡
A
p
2
)
−
A
p
δ 
min
​
 =2arcsin(nsin 
2
A 
p
​
 
​
 )−A 
p
​
 
This minimum-deviation expression applies only when its inverse-sine argument is physically valid. The critical angle for an interface from prism material into air is:

θ
c
=
arcsin
⁡
(
1
n
)
,
n
>
1
θ 
c
​
 =arcsin( 
n
1
​
 ),n>1
The module validates input angles and refractive indices and raises a prism-specific exception for unsupported or non-transmitting geometry.

7.4.3 Dispersion Calculation Module
Module: optics/dispersion.py

Data structures: CauchyCoefficients, DispersionResult, SpectralPrismResult
Exception: DispersionError

The module implements Cauchy's dispersion equation:

n
(
λ
)
=
A
+
B
λ
2
+
C
λ
4
n(λ)=A+ 
λ 
2
 
B
​
 + 
λ 
4
 
C
​
 
The public wavelength input is in nanometers and is converted to micrometers before applying the coefficients:

λ
μ
m
=
λ
n
m
1000
λ 
μm
​
 = 
1000
λ 
nm
​
 
​
 
The coefficients are material-dependent and must correspond to the chosen wavelength units and fitted spectral range. The module exposes calculations for a single refractive index, a wavelength series, and spectral prism deviation through the prism geometry module.

calculate_spectral_prism_deviation evaluates a prism solution for each wavelength. Wavelengths that fail prism transmission checks are excluded; when no wavelength produces a valid solution, the calculation reports a DispersionError rather than an empty successful result.

7.4.4 Prism Visualization Module
Module: visualization/prism_diagram.py
Class: PrismDiagram

The prism diagram illustrates the incident ray, refraction inside the prism, emergent ray, and prism geometry. It uses calculation outputs rather than implementing a separate physical model. Its Matplotlib figure can be displayed inside the Prism page.

7.4.5 Dispersion Visualization Module
Module: visualization/dispersion_diagram.py
Class: DispersionDiagram

The dispersion visualization supports wavelength-dependent plots and visible-spectrum presentation. It receives calculated spectral data, configures axes/labels, and draws on the page's Matplotlib figure. Plotting must handle the absence of valid transmitted wavelengths without presenting misleading numerical curves.

7.4.6 Prism GUI Module
Module: ui/pages/prism_page.py
Class: PrismPage

The page coordinates prism inputs, dispersion coefficients, calculation requests, results, and visualization selection. It provides four modes:

Prism Ray Diagram — geometrical ray paths through the prism.
Refractive Index vs Wavelength — the Cauchy refractive-index curve.
Prism Deviation vs Wavelength — calculated deviation for transmitting wavelengths.
Visible Spectrum — visible-wavelength representation.
The page embeds a shared Matplotlib figure and Qt canvas and supports export in formats supported by its plotting controls, including PNG, SVG, and PDF. It uses QSettings("Optik", "Optik") to preserve supported prism parameters and Cauchy coefficients.

Invalid parameter combinations and total internal reflection are communicated as user-readable errors or unavailable results rather than uncaught exceptions.

7.4.7 Main Window and Dashboard Integration
Module: ui/main_window.py
Class: MainWindow

The main window expands from six to seven pages. Prism Optics & Dispersion is index 5, with shortcut Ctrl+6; Settings moves to index 6, with shortcut Ctrl+7. The Home dashboard offers navigation to the Prism page.

The application now always starts on Home. _restore_settings() restores the appearance theme and selects HOME; it no longer restores window/last_page or window/last_page_name. The navigate_to() method updates session navigation but does not persist a last-page preference. closeEvent() saves the theme without saving the active page.

7.4.8 Theme and Persistence Design
The main window stores the appearance preference under appearance/theme. The Prism page accepts dark-mode updates through set_dark_mode(bool) so Matplotlib rendering can match the active theme. Calculator inputs persist independently of main-window navigation.

7.4.9 Testing Architecture
The v0.4.0 test strategy covers:

Area	Validation
Prism geometry	Entry/exit refraction, deviation, minimum deviation, critical angle, invalid geometry
Dispersion	Cauchy index calculations, wavelength units, spectral series, coefficient validation
Spectral prism	Valid transmission, non-transmitting wavelengths, empty valid-result handling
Visualization	Figure generation, labels, wavelength plots, mode switching, export
Prism GUI	Input validation, calculation display, mode selection, persistence, theme behavior
Main window	Seven-page navigation, shortcuts, Home-first startup, theme persistence
tests/test_main_window.py has been revised to test that historical last-page settings do not override the Home startup behavior. The final full-suite execution result should be recorded separately in release validation records.

Run regression tests with:

python -m pytest tests/ -v
7.4.10 Design Limitations
The prism model assumes idealized geometrical optics and surrounding air.
Cauchy's equation is empirical and should be used only with coefficients appropriate to the material and spectral range.
Invalid or non-transmitting wavelength solutions are omitted from spectral deviation output.
Dispersion plots are numerical models, not full electromagnetic simulations.
Absorption, polarization, diffraction, interference, and detailed material databases are outside v0.4.0 scope.
8. Testing and Quality Assurance Architecture
8.1 Unit Testing
Optik uses pytest to verify scientific calculations. Tests should cover expected numerical results, boundary conditions, invalid inputs, special mathematical cases, and classifications.

8.2 GUI Testing
Optik uses pytest-qt to verify PySide6 components. GUI tests should cover widget initialization, inputs, calculations, buttons, navigation, theme behavior, and persistent settings.

8.3 Visualization Testing
Visualization tests should verify figure creation, optical component placement, ray geometry, diagram labels, special optical cases, and export functionality.

8.4 Regression Testing
The complete test suite should be executed following significant feature changes:

python -m pytest tests/ -v
Regression testing helps ensure previously supported functionality continues to operate after new modules are introduced.

8.5 Manual Verification
Before release, Optik should be tested interactively for calculator operation, page navigation, theme switching, diagram rendering, input handling, and settings persistence.

9. Design Maintenance Policy
Optik follows a versioned software design documentation policy.

9.1 Permanent Sections
The Introduction, Core Architecture, Project Structure, Core Component Design, Scientific Calculation Architecture, Visualization Architecture, and Testing Architecture are maintained as the current reference.

9.2 Version-Specific Sections
Each release receives a section documenting new calculations, GUI components, visualizations, architectural changes, mathematical models, design decisions, testing strategy, and known limitations.

9.3 Historical Design Preservation
Previous version sections remain intact in substance. If a later release replaces an existing component, its new version section identifies the change. Historical inaccuracies may be corrected with appropriate revision notes.

10. Document Revision History
Revision	Software Version	Description
1.0	v0.1.0	Initial reflection and refraction architecture
1.1	v0.2.0	Thin lens calculations and visualization architecture
1.2	v0.3.0	Mirror optics architecture and versioned documentation structure
1.3	v0.4.0	Prism optics, Cauchy dispersion, spectral visualization, seven-page navigation, and Home-first startup
End of Software Design Document





