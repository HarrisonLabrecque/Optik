# Optik — User Guide

**Version:** 0.1.0  
**Application:** Optik  
**Category:** Optics and Photonics Desktop Software  

## 1. Introduction

Optik is an open-source desktop application designed to help users perform fundamental optical calculations and visualize light-ray behavior.

Version 0.1.0 includes calculators for reflection, refraction, critical angles, and total internal reflection.

The application also provides two-dimensional optical ray diagrams.

## 2. System Requirements

### Software

- Compatible Python 3 installation
- PySide6
- Matplotlib
- NumPy
- SciPy

Python 3.14 is the development environment used for the initial project. Compatibility with other Python versions depends on the installed package versions.

### Operating System

Windows is the primary development environment.

Other desktop operating systems may be supported if compatible Python and Qt dependencies are available.

## 3. Installation

### Step 1: Obtain the Source Code

Download or clone the Optik repository.

### Step 2: Open a Terminal

Navigate to the Optik project directory.

### Step 3: Create a Virtual Environment

On Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

### Step 4: Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

### Step 5: Launch Optik

```powershell
python main.py
```

The Optik main window should appear.

## 4. Application Navigation

The application provides four main pages.

### Home

The Home page serves as the application's landing page.

### Reflection

The Reflection page calculates and visualizes the law of reflection.

### Refraction

The Refraction page calculates and visualizes Snell's law, critical angles, and total internal reflection.

### Settings

The Settings page provides a foundation for future application configuration options.

## 5. Reflection Calculator

### 5.1 Purpose

The Reflection Calculator determines the angle of reflection for an incident light ray.

The calculation follows:

θᵣ = θᵢ

Where:

- θᵣ is the reflected angle.
- θᵢ is the incident angle.

Both angles are measured relative to the surface normal.

### 5.2 Instructions

1. Open the Reflection page.
2. Locate the Incident Angle input.
3. Enter an angle between 0° and 90°.
4. Click **Calculate Reflection**.
5. Review the reflected angle.
6. Examine the optical ray diagram.

### 5.3 Example

Input:

Incident Angle = 45°

Output:

Reflected Angle = 45.00°

The diagram displays incident and reflected rays at equal angles to the normal.

## 6. Refraction Calculator

### 6.1 Purpose

The Refraction Calculator determines the direction of light as it passes between two optical media.

The calculation follows Snell's law:

n₁ sin(θ₁) = n₂ sin(θ₂)

Where:

- n₁ is the refractive index of the incident medium.
- n₂ is the refractive index of the transmitted medium.
- θ₁ is the incident angle.
- θ₂ is the refracted angle.

### 6.2 Instructions

1. Open the Refraction page.
2. Enter the first refractive index.
3. Enter the second refractive index.
4. Enter the incident angle.
5. Click **Calculate Refraction**.
6. Review the calculated results.
7. Examine the optical ray diagram.

### 6.3 Example: Air to Glass

Input:

- n₁ = 1.0
- n₂ = 1.5
- Incident Angle = 30°

Expected output:

Refracted Angle ≈ 19.47°

The refracted ray bends toward the surface normal.

## 7. Critical Angle

### 7.1 Purpose

The critical angle represents the incident angle at which the refracted ray travels along the boundary between two media.

The calculation applies when:

n₁ > n₂

The equation is:

θc = arcsin(n₂ / n₁)

### 7.2 Example

Input:

- n₁ = 1.5
- n₂ = 1.0

Expected output:

Critical Angle ≈ 41.81°

When n₁ ≤ n₂, the critical angle is not applicable.

## 8. Total Internal Reflection

### 8.1 Purpose

Total internal reflection occurs when light travels from a higher refractive index to a lower refractive index and the incident angle exceeds the critical angle.

### 8.2 Example

Input:

- n₁ = 1.5
- n₂ = 1.0
- Incident Angle = 50°

Expected output:

- Total Internal Reflection: Yes
- Critical Angle: 41.81°
- Refracted Angle: No transmitted ray (TIR)

The diagram displays incident and reflected rays without a transmitted ray.

## 9. Understanding the Ray Diagrams

Optik uses a two-dimensional coordinate system to illustrate light-ray behavior.

The diagrams include:

- **Blue:** Incident ray
- **Orange:** Reflected ray
- **Green:** Refracted ray
- **Dashed vertical line:** Surface normal
- **Horizontal line:** Optical interface

The colors reflect the default visualization theme.

The diagrams illustrate idealized ray geometry and do not represent optical intensity.

## 10. Input Restrictions

Incident angles must be between 0° and 90°.

Refractive indices must be positive.

The graphical interface uses numerical input controls to restrict values to supported ranges.

Invalid mathematical inputs may produce an error message.

## 11. Troubleshooting

### Application Does Not Start

Confirm that Python and the required dependencies are installed.

Run:

```powershell
python -m pip install -r requirements.txt
```

Then retry:

```powershell
python main.py
```

### Matplotlib Import Error

Install Matplotlib:

```powershell
python -m pip install matplotlib
```

### PySide6 Import Error

Install PySide6:

```powershell
python -m pip install PySide6
```

### Diagram Does Not Update

Click the Calculate button after changing the numerical inputs.

### Unexpected Calculation Results

Verify that the refractive indices are entered in the correct order.

The first index represents the incident medium, and the second represents the transmitted medium.

## 12. Known Limitations

Optik v0.1.0 uses idealized geometrical optics calculations.

It does not currently calculate:

- Fresnel reflectance
- Optical power
- Polarization
- Diffraction
- Interference
- Absorption
- Complex optical systems

The application is intended for educational and computational reference purposes.

## 13. Future Development

Future versions may include additional optics and photonics tools, advanced simulations, and expanded visualization capabilities.

## 14. License

Optik is distributed under the MIT License.

Refer to the LICENSE file in the project root for the complete license terms.