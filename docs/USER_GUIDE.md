# Optik — User Guide

**Project:** Optik — Open-Source Optics & Photonics Desktop Application  
**Current Development Version:** v0.4.0  
**Document Status:** Maintained  
**License:** MIT

---

## 1. Introduction

### 1.1 Purpose

Optik is an open-source scientific desktop application developed using Python and PySide6. It provides interactive tools for performing optical calculations and visualizing geometrical optics through ray diagrams and scientific graphs.

This User Guide explains how to install, navigate, and use Optik's scientific calculation modules.

### 1.2 Intended Users

Optik is designed for students studying physics, optics, and photonics; educators demonstrating optical principles; researchers exploring geometrical optics; engineers performing introductory optical calculations; and individuals interested in optical science.

### 1.3 Supported Features

Through v0.4.0, Optik includes:

| Module | Description | Introduced |
|---|---|---|
| Reflection | Law of reflection calculations and diagrams | v0.1.0 |
| Refraction | Snell's law, critical angles, and total internal reflection | v0.1.0 |
| Thin Lenses | Image formation and magnification for thin lenses | v0.2.0 |
| Mirror Optics | Image formation and magnification for spherical mirrors | v0.3.0 |
| Prism Optics & Dispersion | Prism refraction, deviation, Cauchy dispersion, and spectral plots | v0.4.0 |
| Settings | Application appearance and preferences | v0.1.0 |

---

## 2. Installation and Startup

### 2.1 System Requirements

To run Optik from source, you need a compatible Python 3 installation, PySide6, Matplotlib, other dependencies specified by the project, and a graphical desktop environment. The application is primarily developed for desktop use.

### 2.2 Download the Source Code

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/Optik.git
cd Optik
```

Replace `YOUR_USERNAME` with the repository owner's GitHub username. Alternatively, download the repository as a ZIP archive and extract it.

### 2.3 Create a Virtual Environment

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

### 2.4 Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 2.5 Launch Optik

From the project root, run the current main-window module:

```bash
python -m ui.main_window
```

If the repository provides a separate application launcher, use its documented entry point instead. **Optik v0.4.0 always opens on the Home dashboard**, even if a different page was selected in the previous session. The appearance theme remains persistent.

### 2.6 Windows Executable

If a Windows executable is included in a published release, follow the instructions provided with that release. An executable is not assumed to be available for every development version.

---

## 3. Application Interface

### 3.1 Main Window

The main window contains a navigation sidebar, Home dashboard, scientific calculator pages, Settings page, input controls, numerical results, and scientific diagrams.

### 3.2 Navigation Sidebar

| Page | Shortcut |
|---|---|
| Home | Ctrl+1 |
| Reflection | Ctrl+2 |
| Refraction | Ctrl+3 |
| Thin Lenses | Ctrl+4 |
| Mirror Optics | Ctrl+5 |
| Prism Optics & Dispersion | Ctrl+6 |
| Settings | Ctrl+7 |

### 3.3 Home Dashboard

The Home dashboard provides quick access to scientific calculators. To open a module, navigate to Home, locate its feature card, and select **Open Calculator**. You can also select the module from the sidebar.

### 3.4 Calculation Workflow

1. Open the desired calculator.
2. Enter the required parameters.
3. Select **Calculate** (or the equivalent calculation control).
4. Review the numerical results.
5. Examine the generated diagram or graph, if available.
6. Modify the inputs and recalculate as needed.

### 3.5 Settings and Themes

Optik supports light and dark themes. Open Settings, select the desired theme, and return to the calculator. Supported preferences are stored between sessions using Qt application settings. Navigation does **not** resume on the last visited page: every launch starts on Home.

---

# 4. Version-Specific User Instructions

This section documents features introduced by each Optik version. New releases append sections without replacing historical instructions.

---

## 4.1 Version 0.1.0 — Reflection and Refraction

**Status:** Completed

### 4.1.1 Reflection Calculator

The Reflection calculator determines the direction of reflected light using the law of reflection:

\[
\theta_r=\theta_i
\]

Here, \(\theta_i\) is the incident angle and \(\theta_r\) is the reflected angle. Both are measured relative to the surface normal.

**How to use Reflection:** Open the Reflection page, enter the incident angle, select Calculate, review the reflected angle, and examine the ray diagram.

**Example:** An incident angle of **35°** produces a reflected angle of **35°**.

### 4.1.2 Refraction Calculator

The Refraction calculator determines how light changes direction between two optical media using Snell's law:

\[
n_1\sin(\theta_1)=n_2\sin(\theta_2)
\]

Here, \(n_1\) and \(n_2\) are the refractive indices of the two media, while \(\theta_1\) and \(\theta_2\) are the incident and refracted angles.

**How to use Refraction:** Open the Refraction page, enter both refractive indices and the incident angle, select Calculate, and review the numerical results and diagram.

| Example input | Value |
|---|---|
| First refractive index | 1.00 |
| Second refractive index | 1.50 |
| Incident angle | 45° |

**Expected result:** Refracted angle approximately **28.13°**. Light bends toward the normal when entering the higher-index medium.

### 4.1.3 Critical Angle

The critical angle is the incident angle at which the refracted ray travels along the interface:

\[
\theta_c=\sin^{-1}\left(\frac{n_2}{n_1}\right),\qquad n_1>n_2
\]

For glass with refractive index **1.50** and air with refractive index **1.00**, the critical angle is approximately **41.81°**.

### 4.1.4 Total Internal Reflection

Total internal reflection occurs when light travels from a higher-index medium to a lower-index medium and the incident angle exceeds the critical angle. The idealized model then has no transmitted refracted ray.

---

## 4.2 Version 0.2.0 — Thin Lens Optics

**Status:** Development Completed

### 4.2.1 Overview

The Thin Lenses module supports converging and diverging lenses, image distance, magnification, image height, image orientation and size, and ray diagrams.

### 4.2.2 Thin Lens Equation

\[
\frac{1}{f}=\frac{1}{d_o}+\frac{1}{d_i}
\]

Here, \(f\) is focal length, \(d_o\) is object distance, and \(d_i\) is image distance. Positive focal length denotes a converging lens and negative focal length a diverging lens. Positive image distance denotes a real image and negative image distance a virtual image under the calculator's convention.

### 4.2.3 How to Use Thin Lenses

1. Open Thin Lenses.
2. Select the lens type, if a selector is provided.
3. Enter focal length and object distance.
4. Enter object height, where supported.
5. Select Calculate.
6. Review image distance, magnification, and image properties.
7. Examine the ray diagram.

### 4.2.4 Converging Lens Example

| Parameter | Value |
|---|---|
| Focal length | +10 cm |
| Object distance | 30 cm |
| Object height | 5 cm |

| Result | Value |
|---|---|
| Image distance | +15 cm |
| Magnification | -0.50 |
| Image height | -2.50 cm |
| Image type | Real |
| Orientation | Inverted |
| Image size | Reduced |

### 4.2.5 Diverging Lens Example

| Parameter | Value |
|---|---|
| Focal length | -10 cm |
| Object distance | 30 cm |
| Object height | 5 cm |

| Result | Value |
|---|---|
| Image distance | -7.50 cm |
| Magnification | +0.25 |
| Image height | +1.25 cm |
| Image type | Virtual |
| Orientation | Upright |
| Image size | Reduced |

### 4.2.6 Magnification

\[
m=-\frac{d_i}{d_o},\qquad h_i=mh_o
\]

Positive magnification indicates an upright image; negative indicates an inverted image. Absolute magnification greater than 1 means enlarged, less than 1 means reduced, and equal to 1 means the same size.

### 4.2.7 Lens Ray Diagrams

Depending on the configuration, diagrams display the principal axis, lens, focal points, object and image positions, principal rays, and virtual ray extensions. These represent idealized thin lens optics.

---

## 4.3 Version 0.3.0 — Mirror Optics

**Status:** Development Completed

### 4.3.1 Overview

The Mirror Optics module supports concave and convex spherical mirrors, image distance, radius of curvature, magnification, image height, real/virtual and upright/inverted classification, image size classification, and ray diagrams.

### 4.3.2 Opening Mirror Optics

Open Mirror Optics from the sidebar or Home dashboard, enter parameters, and select Calculate. The keyboard shortcut is **Ctrl+5**.

### 4.3.3 Mirror Calculator Inputs

| Input | Description | Default |
|---|---|---|
| Mirror Type | Concave or Convex | Concave |
| Focal Length | Magnitude of focal length | 10 |
| Object Distance | Distance from object to mirror | 30 |
| Object Height | Height of object | 5 |

The calculator uses mirror type to determine focal-length sign. Use consistent distance units.

### 4.3.4 Spherical Mirror Equation

\[
\frac{1}{f}=\frac{1}{d_o}+\frac{1}{d_i},\qquad
 d_i=\frac{fd_o}{d_o-f}
\]

Here, \(f\) is focal length, \(d_o\) object distance, and \(d_i\) image distance.

### 4.3.5 Radius of Curvature

\[
R=2f
\]

Under the selected convention, concave mirrors have positive focal length and convex mirrors negative focal length.

### 4.3.6 Concave Mirror Example

| Parameter | Value |
|---|---|
| Mirror Type | Concave |
| Focal Length | 10 cm |
| Object Distance | 30 cm |
| Object Height | 5 cm |

| Result | Value |
|---|---|
| Image Distance | +15 cm |
| Radius of Curvature | +20 cm |
| Magnification | -0.50 |
| Image Height | -2.50 cm |
| Image Type | Real |
| Orientation | Inverted |
| Image Size | Reduced |

The real image forms in front of the mirror.

### 4.3.7 Convex Mirror Example

| Parameter | Value |
|---|---|
| Mirror Type | Convex |
| Focal Length | 10 cm (magnitude) |
| Object Distance | 30 cm |
| Object Height | 5 cm |

| Result | Value |
|---|---|
| Image Distance | -7.50 cm |
| Radius of Curvature | -20 cm |
| Magnification | +0.25 |
| Image Height | +1.25 cm |
| Image Type | Virtual |
| Orientation | Upright |
| Image Size | Reduced |

The virtual image appears behind the mirror.

### 4.3.8 Mirror Magnification

\[
m=-\frac{d_i}{d_o},\qquad h_i=mh_o
\]

Negative magnification indicates an inverted image; positive indicates an upright image. Absolute magnification determines relative size.

### 4.3.9 Mirror Ray Diagrams

The Matplotlib diagram may display the spherical mirror, principal axis, focal point (F), center of curvature (C), object and image arrows, incident/reflected rays, and dashed virtual ray extensions.

### 4.3.10 Image Formation at Infinity

For a concave mirror with \(d_o=f\), reflected rays are parallel in the idealized model and the image forms at infinity. Finite magnification and image height are undefined; the calculator displays special labels rather than ordinary finite values.

### 4.3.11 Resetting Mirror Inputs

Open Mirror Optics, select Reset, review restored default values, and select Calculate to generate a new result.

### 4.3.12 Persistent Mirror Settings

Supported mirror preferences include selected mirror type, focal length, object distance, and object height. Stored values may be restored when the calculator is reopened or the application restarted.

### 4.3.13 Limitations

The mirror module uses idealized spherical mirror equations and does not model spherical aberration, full non-paraxial ray tracing, diffraction, interference, surface manufacturing imperfections, or real optical coating behavior.

---

## 4.4 Version 0.4.0 — Prism Optics & Dispersion

**Status:** Development Completed

### 4.4.1 Overview

Prism Optics & Dispersion adds geometrical ray propagation through a prism and wavelength-dependent refractive index calculations. The module combines Snell's law, prism geometry, minimum deviation, critical-angle checks, and Cauchy's dispersion model.

### 4.4.2 Opening the Prism Calculator

1. Launch Optik; it opens on Home.
2. Select **Prism Optics & Dispersion** in the sidebar, or use its Home feature card if present.
3. Alternatively, press **Ctrl+6**.
4. Enter the desired prism geometry and optical parameters.
5. Select the visualization mode and calculate or refresh the result.

### 4.4.3 Input Parameters

| Input | Description | Notes |
|---|---|---|
| Prism apex angle | Angle between the prism's refracting faces | Degrees |
| Incident angle | Angle of incoming light relative to the first surface normal | Degrees |
| Prism refractive index | Refractive index for single-wavelength prism calculations | Dimensionless, positive |
| Wavelength | Optical wavelength | Nanometers in the interface |
| Cauchy A | Constant coefficient in the dispersion model | Dimensionless |
| Cauchy B | Second Cauchy coefficient | Consistent with wavelength in µm |
| Cauchy C | Fourth-order Cauchy coefficient | Consistent with wavelength in µm |
| Visualization mode | Selects diagram or spectral plot | Four supported modes |

Some values may be restored from your previous Prism page session. Select Reset to restore the calculator's defaults where supported.

### 4.4.4 Prism Refraction and Angular Deviation

A ray entering the prism refracts at the first surface and again when leaving the second surface. For a prism in air, the model uses Snell's law at both interfaces and the prism relation:

\[
r_1+r_2=A_p
\]

The total deviation is:

\[
\delta=i+e-A_p
\]

Where:

- \(A_p\) is the prism apex angle.
- \(i\) is the angle of incidence at the first face.
- \(r_1\) and \(r_2\) are internal angles relative to their respective surface normals.
- \(e\) is the emergent angle.
- \(\delta\) is the angular deviation.

At the symmetric minimum-deviation configuration, the ideal prism relation is:

\[
\delta_{\min}=2\sin^{-1}\left(n\sin\frac{A_p}{2}\right)-A_p
\]

This expression assumes the inverse-sine argument is within its valid domain and that a transmitted symmetric ray is possible.

### 4.4.5 Worked Prism Example

Use these illustrative inputs:

| Parameter | Value |
|---|---|
| Prism apex angle | 35° |
| Incident angle | 45° |
| Refractive index | 1.50 |

Expected approximate results for an air–prism–air model:

| Result | Approximate value |
|---|---|
| First internal refraction angle | 28.13° |
| Second internal angle | 6.87° |
| Emergent angle | 10.34° |
| Total deviation | 20.34° |
| Minimum deviation | 18.62° |
| Critical angle (prism to air) | 41.81° |

The displayed values may differ slightly due to numerical rounding.

### 4.4.6 Cauchy's Dispersion Equation

For wavelength-dependent refractive index, Optik uses:

\[
n(\lambda)=A+\frac{B}{\lambda^2}+\frac{C}{\lambda^4}
\]

**Important:** Enter wavelengths in **nanometers** in the GUI when requested, but the Cauchy calculation converts them to **micrometers** (µm). Coefficients must be compatible with that convention.

Illustrative coefficients for a glass-like model are:

| Coefficient | Example value |
|---|---|
| A | 1.5046 |
| B | 0.00420 |
| C | 0.00012 |

At **556 nm** (0.556 µm), these coefficients yield a refractive index of approximately **1.5195**. These are illustrative values, not a verified material calibration. For scientific work, use coefficients fitted to the actual material and wavelength range.

**Do not enter 1 for all three coefficients** as a general default: this can produce unrealistically high refractive indices and prevent valid transmitted prism rays.

### 4.4.7 Four Visualization Modes

| Mode | What it shows |
|---|---|
| Prism Ray Diagram | Incident, internal, and emergent ray paths |
| Refractive Index vs Wavelength | Cauchy refractive index across a wavelength range |
| Prism Deviation vs Wavelength | Angular deviation of transmitted wavelengths |
| Visible Spectrum | Visual representation of visible wavelengths |

To change the plot, select a different visualization mode and use the page's calculation or refresh control if necessary. The prism page reuses its embedded Matplotlib figure/canvas for these modes.

### 4.4.8 Exporting Diagrams

Where the export control or Matplotlib toolbar is available, use its save action to export the current diagram or graph. Supported output formats include PNG, SVG, and PDF. Check the chosen filename and extension before saving.

### 4.4.9 Total Internal Reflection and Missing Spectral Data

Not every combination of prism angle, incident angle, refractive index, and wavelength permits a transmitted emergent ray. When the second interface reaches a total-internal-reflection condition, the prism deviation calculation cannot produce an ordinary emergent angle.

For spectral deviation, wavelengths without valid transmitted rays may be omitted. If no wavelengths are valid, the calculator should display an error rather than an invented deviation curve.

If the deviation graph appears blank, verify that:

1. The selected visualization is **Prism Deviation vs Wavelength**.
2. The Cauchy coefficients produce realistic refractive indices.
3. The apex and incident angles allow transmission.
4. The selected wavelength range is appropriate for the coefficients.
5. The calculator has been refreshed or recalculated.

### 4.4.10 Persistent Settings and Startup Behavior

The Prism page stores supported parameters through `QSettings`. The application also preserves the light or dark theme. However, **Optik always starts on Home**, not on the previously visited Prism page or another calculator.

### 4.4.11 Model Limitations

- The surrounding medium is assumed to be air.
- The model uses idealized geometrical optics and a simple prism geometry.
- Cauchy's equation is reliable only within the wavelength range and material for which coefficients were fitted.
- The model does not simulate polarization, absorption, diffraction, interference, or advanced optical coatings.
- Spectral deviation results omit wavelengths without a valid transmitted ray.

---

# 5. Understanding Calculation Results

## 5.1 Real Images

A real image occurs when optical rays physically converge at an image location in the geometrical model. Under the current lens and mirror conventions, a positive image distance identifies a real image.

## 5.2 Virtual Images

A virtual image occurs when rays appear to originate from an image location when extended backward. Under the current conventions, a negative image distance identifies a virtual image.

## 5.3 Image Orientation

| Classification | Meaning |
|---|---|
| Upright | Same vertical orientation as the object |
| Inverted | Vertically reversed relative to the object |

## 5.4 Image Size

| Classification | Condition |
|---|---|
| Enlarged | Absolute magnification greater than 1 |
| Reduced | Absolute magnification less than 1 |
| Same Size | Absolute magnification equal to 1 |

## 5.5 Units

Optik's geometrical optics equations use consistent distance units. For example, if focal length and object distance are in centimeters, image distance and radius of curvature are also in centimeters. Magnification and refractive index are dimensionless. Prism angles are expressed in degrees; spectral wavelengths are entered in nanometers and converted to micrometers for Cauchy's equation.

---

# 6. Troubleshooting

## 6.1 Application Does Not Start

Check that Python and required dependencies are installed, the virtual environment is activated, and the command is run from the project root. Try:

```bash
python -m pip install -r requirements.txt
python -m ui.main_window
```

## 6.2 Invalid Calculation Inputs

Check input values, verify the selected model, avoid invalid denominators and unsupported values, use consistent units, and recalculate.

## 6.3 Diagram Does Not Update

Confirm inputs were changed, select Calculate again, check for a displayed error, and reopen the calculator if necessary. If the issue persists, record the inputs and application version.

## 6.4 Theme Does Not Update

Open Settings, select the theme, navigate between calculator pages, and restart if necessary.

## 6.5 Settings Are Not Restored

Verify the application runs under the same user account and its settings storage is accessible. Note that **last-page navigation is intentionally not restored in v0.4.0**; returning to Home on launch is expected behavior.

## 6.6 Prism Deviation Plot Is Blank

Review the prism geometry and Cauchy coefficients. Extremely large calculated refractive indices or total internal reflection may leave no valid transmitted wavelengths. Use physically appropriate coefficients, then recalculate. See Section 4.4.9.

---

# 7. Reporting Bugs and Requesting Features

When reporting a bug, include the Optik version, operating system, Python version (if running from source), steps to reproduce, expected and actual behavior, and relevant error messages or screenshots. Feature requests should describe the proposed functionality and its intended use.

---

# 8. User Guide Maintenance Policy

This document follows an append-only version history approach.

### 8.1 Permanent Sections

Introduction, Installation and Startup, Application Interface, Understanding Calculation Results, Troubleshooting, and Reporting Bugs and Requesting Features are maintained as current guidance and may be updated when application-wide behavior changes.

### 8.2 Version-Specific Sections

Each release receives a new section documenting calculator modules, inputs, calculations, visualization, worked examples, special cases, and known limitations.

### 8.3 Historical Preservation

Previous-release instructions remain documented. New sections identify changed workflows, and outdated general instructions are corrected so users of the latest release are not misled.

---

# 9. Document Revision History

| Revision | Software Version | Description |
|---|---|---|
| 1.0 | v0.1.0 | Initial reflection and refraction user instructions |
| 1.1 | v0.2.0 | Added thin lens calculator instructions |
| 1.2 | v0.3.0 | Added mirror optics instructions and versioned documentation structure |
| 1.3 | v0.4.0 | Added prism optics, Cauchy dispersion, spectral visualization, and updated navigation/startup instructions |

---

# 10. Additional Documentation

- `README.md` — Project overview and installation.
- `CHANGELOG.md` — Release changes.
- `docs/SRS.md` — Software Requirements Specification.
- `docs/SDD.md` — Software Design Document.
- `docs/DEVELOPMENT.md` — Development and testing procedures.

---

**Optik — Exploring Optics and Photonics Through Scientific Computing.**

**End of User Guide**
