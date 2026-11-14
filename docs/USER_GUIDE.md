# Optik — User Guide

**Project:** Optik — Open-Source Optics & Photonics Desktop Application  
**Current Development Version:** v0.3.0  
**Document Status:** Maintained  
**License:** MIT

---

## 1. Introduction

### 1.1 Purpose

Optik is an open-source scientific desktop application developed using Python and PySide6.

It provides interactive tools for performing optical calculations and visualizing geometrical optics through ray diagrams.

This User Guide explains how to install, navigate, and use Optik's scientific calculation modules.

### 1.2 Intended Users

Optik is designed for:

- Students studying physics, optics, and photonics.
- Educators demonstrating optical principles.
- Researchers exploring geometrical optics.
- Engineers performing introductory optical calculations.
- Individuals interested in optical science.

### 1.3 Supported Features

Through v0.3.0, Optik includes:

| Module | Description | Introduced |
|---|---|---|
| Reflection | Law of reflection calculations and diagrams | v0.1.0 |
| Refraction | Snell's law, critical angles, and total internal reflection | v0.1.0 |
| Thin Lenses | Image formation and magnification for thin lenses | v0.2.0 |
| Mirror Optics | Image formation and magnification for spherical mirrors | v0.3.0 |
| Settings | Application appearance and preferences | v0.1.0 |

---

## 2. Installation and Startup

### 2.1 System Requirements

To run Optik from source, you need:

- A compatible Python 3 installation.
- PySide6.
- Matplotlib.
- Other dependencies specified by the project.
- A graphical desktop environment.

The application is primarily developed for desktop use.

### 2.2 Download the Source Code

Clone the Optik repository using Git:

```bash
git clone https://github.com/YOUR_USERNAME/Optik.git
cd Optik
```

Replace `YOUR_USERNAME` with the repository owner's GitHub username.

Alternatively, download the repository as a ZIP archive and extract it.

### 2.3 Create a Virtual Environment

On Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

On Linux or macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2.4 Install Dependencies

From the project directory, run:

```bash
python -m pip install -r requirements.txt
```

### 2.5 Launch Optik

Run the application using:

```bash
python -m app.main_window
```

The Optik main window should appear with the Home dashboard and navigation sidebar.

### 2.6 Windows Executable

If a Windows executable is included in a published release, use the installation or startup instructions provided with that release.

An executable is not assumed to be available for every development version.

---

## 3. Application Interface

### 3.1 Main Window

Optik's main window contains:

- A navigation sidebar.
- A Home dashboard.
- Dedicated scientific calculator pages.
- A Settings page.
- Calculation input controls.
- Numerical result displays.
- Scientific diagrams.

### 3.2 Navigation Sidebar

Use the sidebar to switch between calculation modules.

The available pages in v0.3.0 are:

| Page | Shortcut |
|---|---|
| Home | Ctrl+1 |
| Reflection | Ctrl+2 |
| Refraction | Ctrl+3 |
| Thin Lenses | Ctrl+4 |
| Mirror Optics | Ctrl+5 |
| Settings | Ctrl+6 |

### 3.3 Home Dashboard

The Home dashboard provides quick access to Optik's scientific calculators.

Each feature card identifies a calculation module and includes an Open Calculator button.

To open a module:

1. Navigate to Home.
2. Locate the desired feature card.
3. Select Open Calculator.
4. Enter the required optical parameters.

### 3.4 Calculation Workflow

Most Optik calculators follow a similar workflow:

1. Open the calculator.
2. Enter the required parameters.
3. Select Calculate.
4. Review the numerical results.
5. Examine the generated ray diagram, if available.
6. Modify the inputs and recalculate as needed.

### 3.5 Settings and Themes

Optik supports light and dark themes.

To change the appearance:

1. Open Settings.
2. Select the desired theme.
3. Return to the calculator.

Supported preferences are stored between sessions using Qt's application settings system.

---

# 4. Version-Specific User Instructions

This section documents features introduced by each Optik version.

New releases append additional sections without replacing the historical instructions.

---

## 4.1 Version 0.1.0 — Reflection and Refraction

**Status:** Completed

### 4.1.1 Reflection Calculator

The Reflection calculator determines the direction of reflected light using the law of reflection.

The governing equation is:

\[
\theta_r=\theta_i
\]

Where:

- \(\theta_i\) is the incident angle.
- \(\theta_r\) is the reflected angle.

Both angles are measured relative to the surface normal.

### How to Use Reflection

1. Open the Reflection page.
2. Enter the incident angle.
3. Select Calculate.
4. Review the reflected angle.
5. Examine the reflection ray diagram.

### Example

**Input:**

Incident angle: 35°

**Expected Result:**

Reflected angle: 35°

The incident and reflected rays make equal angles with the surface normal.

### 4.1.2 Refraction Calculator

The Refraction calculator determines how light changes direction when traveling between two optical media.

It uses Snell's law:

\[
n_1\sin(\theta_1)=n_2\sin(\theta_2)
\]

Where:

- \(n_1\) is the refractive index of the first medium.
- \(n_2\) is the refractive index of the second medium.
- \(\theta_1\) is the incident angle.
- \(\theta_2\) is the refracted angle.

### How to Use Refraction

1. Open the Refraction page.
2. Enter the first refractive index.
3. Enter the second refractive index.
4. Enter the incident angle.
5. Select Calculate.
6. Review the refracted angle and any additional optical results.
7. Examine the refraction ray diagram.

### Example

**Inputs:**

| Parameter | Value |
|---|---|
| First refractive index | 1.00 |
| Second refractive index | 1.50 |
| Incident angle | 45° |

**Expected Result:**

Refracted angle: approximately 28.13°.

The light bends toward the normal because it enters a medium with a higher refractive index.

### 4.1.3 Critical Angle

The critical angle is the incident angle at which the refracted ray travels along the boundary between two media.

It is calculated using:

\[
\theta_c=\sin^{-1}\left(\frac{n_2}{n_1}\right)
\]

This equation applies when:

\[
n_1>n_2
\]

### Example

For light traveling from glass into air:

- Glass refractive index: 1.50.
- Air refractive index: 1.00.

The critical angle is approximately 41.81°.

### 4.1.4 Total Internal Reflection

Total internal reflection occurs when:

- Light travels from a higher refractive index to a lower refractive index.
- The incident angle exceeds the critical angle.

Under these conditions, the idealized model has no transmitted refracted ray.

---

## 4.2 Version 0.2.0 — Thin Lens Optics

**Status:** Development Completed

### 4.2.1 Overview

Version 0.2.0 introduces thin lens image formation calculations.

The calculator supports:

- Converging lenses.
- Diverging lenses.
- Image distance.
- Magnification.
- Image height.
- Image orientation.
- Image size.
- Ray diagrams.

### 4.2.2 Thin Lens Equation

The thin lens equation is:

\[
\frac{1}{f}=\frac{1}{d_o}+\frac{1}{d_i}
\]

Where:

- \(f\) is focal length.
- \(d_o\) is object distance.
- \(d_i\) is image distance.

For the convention used in the calculator:

- Positive focal length represents a converging lens.
- Negative focal length represents a diverging lens.
- Positive image distance represents a real image.
- Negative image distance represents a virtual image.

### 4.2.3 How to Use Thin Lenses

1. Open the Thin Lenses page.
2. Select the lens type, if a lens-type selector is provided.
3. Enter the focal length.
4. Enter the object distance.
5. Enter the object height, where supported.
6. Select Calculate.
7. Review the image distance and magnification.
8. Examine the ray diagram.

### 4.2.4 Converging Lens Example

**Inputs:**

| Parameter | Value |
|---|---|
| Focal length | +10 cm |
| Object distance | 30 cm |
| Object height | 5 cm |

**Expected Results:**

| Result | Value |
|---|---|
| Image distance | +15 cm |
| Magnification | -0.50 |
| Image height | -2.50 cm |
| Image type | Real |
| Orientation | Inverted |
| Image size | Reduced |

### 4.2.5 Diverging Lens Example

**Inputs:**

| Parameter | Value |
|---|---|
| Focal length | -10 cm |
| Object distance | 30 cm |
| Object height | 5 cm |

**Expected Results:**

| Result | Value |
|---|---|
| Image distance | -7.50 cm |
| Magnification | +0.25 |
| Image height | +1.25 cm |
| Image type | Virtual |
| Orientation | Upright |
| Image size | Reduced |

### 4.2.6 Magnification

Magnification is calculated using:

\[
m=-\frac{d_i}{d_o}
\]

Image height is calculated using:

\[
h_i=mh_o
\]

Interpretation:

| Magnification | Meaning |
|---|---|
| Positive | Upright image |
| Negative | Inverted image |
| Absolute value greater than 1 | Enlarged |
| Absolute value less than 1 | Reduced |
| Absolute value equal to 1 | Same size |

### 4.2.7 Lens Ray Diagrams

The Thin Lens page includes ray diagrams illustrating optical image formation.

Depending on the optical configuration, the diagrams may display:

- The principal optical axis.
- The lens.
- Focal points.
- Object position.
- Image position.
- Principal rays.
- Virtual ray extensions.

These diagrams represent idealized thin lens optics.

---

## 4.3 Version 0.3.0 — Mirror Optics

**Status:** In Development

### 4.3.1 Overview

Version 0.3.0 introduces spherical mirror calculations.

The Mirror Optics module supports:

- Concave mirrors.
- Convex mirrors.
- Image distance.
- Radius of curvature.
- Magnification.
- Image height.
- Real and virtual image classification.
- Upright and inverted image classification.
- Image size classification.
- Mirror ray diagrams.

### 4.3.2 Opening Mirror Optics

To access the Mirror Optics calculator:

1. Launch Optik.
2. Select Mirror Optics from the sidebar, or select its feature card on Home.
3. Enter the optical parameters.
4. Select Calculate.

You can also press `Ctrl+5` to navigate directly to the Mirror Optics page.

### 4.3.3 Mirror Calculator Inputs

| Input | Description | Default |
|---|---|---|
| Mirror Type | Concave or Convex | Concave |
| Focal Length | Magnitude of focal length | 10 |
| Object Distance | Distance from object to mirror | 30 |
| Object Height | Height of object | 5 |

The calculator uses the selected mirror type to determine the focal length sign.

Use consistent distance units for all inputs.

### 4.3.4 Spherical Mirror Equation

The spherical mirror equation is:

\[
\frac{1}{f}=\frac{1}{d_o}+\frac{1}{d_i}
\]

The image distance can be calculated as:

\[
d_i=\frac{fd_o}{d_o-f}
\]

Where:

- \(f\) is focal length.
- \(d_o\) is object distance.
- \(d_i\) is image distance.

### 4.3.5 Radius of Curvature

The relationship between focal length and radius of curvature is:

\[
R=2f
\]

A concave mirror has a positive focal length under the selected sign convention.

A convex mirror has a negative focal length.

### 4.3.6 Concave Mirror Example

**Inputs:**

| Parameter | Value |
|---|---|
| Mirror Type | Concave |
| Focal Length | 10 cm |
| Object Distance | 30 cm |
| Object Height | 5 cm |

Select Calculate.

**Expected Results:**

| Result | Value |
|---|---|
| Mirror Type | Concave |
| Image Distance | +15 cm |
| Radius of Curvature | +20 cm |
| Magnification | -0.50 |
| Image Height | -2.50 cm |
| Image Type | Real |
| Orientation | Inverted |
| Image Size | Reduced |

The real image forms in front of the mirror.

### 4.3.7 Convex Mirror Example

**Inputs:**

| Parameter | Value |
|---|---|
| Mirror Type | Convex |
| Focal Length | 10 cm (magnitude) |
| Object Distance | 30 cm |
| Object Height | 5 cm |

Select Calculate.

**Expected Results:**

| Result | Value |
|---|---|
| Mirror Type | Convex |
| Image Distance | -7.50 cm |
| Radius of Curvature | -20 cm |
| Magnification | +0.25 |
| Image Height | +1.25 cm |
| Image Type | Virtual |
| Orientation | Upright |
| Image Size | Reduced |

The virtual image appears behind the mirror.

### 4.3.8 Mirror Magnification

Mirror magnification uses:

\[
m=-\frac{d_i}{d_o}
\]

Image height uses:

\[
h_i=mh_o
\]

A negative magnification indicates an inverted image.

A positive magnification indicates an upright image.

The absolute value of magnification determines the relative image size.

### 4.3.9 Mirror Ray Diagrams

The Mirror Optics page includes a Matplotlib ray diagram.

Depending on the configuration, the diagram displays:

- The spherical mirror.
- The principal axis.
- The focal point (F).
- The center of curvature (C).
- The object arrow.
- The image arrow.
- Incident and reflected rays.
- Dashed virtual ray extensions.

### 4.3.10 Image Formation at Infinity

For a concave mirror, when the object is positioned at the focal point:

\[
d_o=f
\]

The reflected rays are parallel in the idealized model.

The image is formed at infinity.

In this configuration, finite image height and magnification are not defined.

The calculator displays special result labels such as Infinity or Undefined rather than an ordinary finite value.

### 4.3.11 Resetting Mirror Inputs

To restore the calculator's default inputs:

1. Open Mirror Optics.
2. Select Reset.
3. Review the restored default values.
4. Select Calculate to generate a new result.

### 4.3.12 Persistent Mirror Settings

The Mirror Optics page stores supported input preferences.

These include:

- Selected mirror type.
- Focal length.
- Object distance.
- Object height.

Stored values may be restored when the calculator is reopened or the application is restarted.

### 4.3.13 Limitations

The v0.3.0 Mirror Optics calculator uses idealized spherical mirror equations.

It does not model:

- Spherical aberration.
- Full non-paraxial ray tracing.
- Diffraction.
- Interference.
- Surface manufacturing imperfections.
- Real optical coating behavior.

The diagrams are intended for geometrical optics calculations and educational visualization.

---

# 5. Understanding Calculation Results

## 5.1 Real Images

A real image occurs when optical rays physically converge at an image location in the geometrical model.

Under the sign conventions used by the current lens and mirror modules, a positive image distance identifies a real image.

## 5.2 Virtual Images

A virtual image occurs when rays appear to originate from an image location when extended backward.

Under the current conventions, a negative image distance identifies a virtual image.

## 5.3 Image Orientation

| Classification | Meaning |
|---|---|
| Upright | Image has the same vertical orientation as the object |
| Inverted | Image is vertically reversed relative to the object |

## 5.4 Image Size

| Classification | Condition |
|---|---|
| Enlarged | Absolute magnification greater than 1 |
| Reduced | Absolute magnification less than 1 |
| Same Size | Absolute magnification equal to 1 |

## 5.5 Units

Optik's geometrical optics equations work with consistent distance units.

For example, if focal length and object distance are entered in centimeters, image distance and radius of curvature are also expressed in centimeters.

Magnification is dimensionless.

---

# 6. Troubleshooting

## 6.1 Application Does Not Start

Check that:

- Python is installed.
- The virtual environment is activated.
- Required dependencies are installed.
- The application is launched from the correct project directory.

Try:

```bash
python -m pip install -r requirements.txt
python -m app.main_window
```

## 6.2 Invalid Calculation Inputs

If a calculation cannot be performed:

1. Check the input values.
2. Verify that the selected optical model is appropriate.
3. Avoid invalid denominators and unsupported values.
4. Confirm that distances use consistent units.
5. Recalculate.

## 6.3 Diagram Does Not Update

If a diagram does not reflect the current inputs:

1. Confirm that the inputs were changed successfully.
2. Select Calculate again.
3. Check for a displayed calculation error.
4. Reopen the calculator if necessary.

If the issue persists, record the input values and application version when reporting the problem.

## 6.4 Theme Does Not Update

If the appearance is inconsistent:

1. Open Settings.
2. Select the desired theme.
3. Navigate between calculator pages.
4. Restart the application if necessary.

## 6.5 Settings Are Not Restored

Optik uses Qt application settings to preserve supported preferences.

If settings are not restored, verify that the application is running under the same user account and that its settings storage is accessible.

---

# 7. Reporting Bugs and Requesting Features

When reporting a bug, include:

- Optik version.
- Operating system.
- Python version, if running from source.
- A description of the issue.
- Steps to reproduce the issue.
- Expected behavior.
- Actual behavior.
- Relevant error messages or screenshots.

Feature requests should describe the proposed functionality and its intended use.

---

# 8. User Guide Maintenance Policy

This document follows an append-only version history approach.

### 8.1 Permanent Sections

The following sections are maintained as current user guidance:

- Introduction.
- Installation and Startup.
- Application Interface.
- Understanding Calculation Results.
- Troubleshooting.
- Reporting Bugs and Requesting Features.

These sections may be updated when application-wide behavior changes.

### 8.2 Version-Specific Sections

Each release receives a new section documenting:

- New calculator modules.
- New user inputs.
- New calculations.
- New visualization features.
- Worked examples.
- Special cases.
- Known limitations.

### 8.3 Historical Preservation

Instructions for previous releases remain documented.

If a future version changes an existing workflow, the new version section should identify the change.

Outdated general instructions should be updated so users of the latest release are not misled.

---

# 9. Future Version Template

Append the following section when introducing a new release:

```markdown
## 4.X Version X.Y.Z — Release Title

**Status:** In Development

### X.1 Overview

### X.2 New Features

### X.3 Accessing the Module

### X.4 Input Parameters

### X.5 Calculation Instructions

### X.6 Worked Examples

### X.7 Visualization

### X.8 Special Cases

### X.9 Known Limitations
```

Only include headings relevant to the release.

---

# 10. Document Revision History

| Revision | Software Version | Description |
|---|---|---|
| 1.0 | v0.1.0 | Initial reflection and refraction user instructions |
| 1.1 | v0.2.0 | Added thin lens calculator instructions |
| 1.2 | v0.3.0 | Added mirror optics instructions and versioned documentation structure |

---

# 11. Additional Documentation

For more information, consult:

- `README.md` — Project overview and installation.
- `CHANGELOG.md` — Release changes.
- `docs/SRS.md` — Software Requirements Specification.
- `docs/SDD.md` — Software Design Document.
- `docs/DEVELOPMENT.md` — Development and testing procedures.

---

**Optik — Exploring Optics and Photonics Through Scientific Computing.**

**End of User Guide**