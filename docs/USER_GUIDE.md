# Optik — User Guide

**Version:** 0.2.0  
**Application:** Optik  
**Category:** Optics and Photonics Desktop Software  
**Status:** Release Candidate

---

## 1. Introduction

Optik is an open-source desktop application designed to help users perform fundamental optical calculations and visualize light-ray behavior.

Version 0.2.0 expands the original geometrical optics functionality with thin lens calculations, magnification, image classification, and additional scientific visualization capabilities.

The application currently includes:

- Reflection calculator.
- Refraction calculator.
- Critical-angle calculations.
- Total internal reflection detection.
- Thin Lens calculator.
- Magnification and image height calculations.
- Converging and diverging lens ray diagrams.
- Two-dimensional optical visualization.
- Light and Dark appearance themes.

Optik is intended for students, educators, researchers, engineers, and individuals interested in optics and photonics.

## 2. System Requirements

### 2.1 Software

- Compatible Python 3 installation.
- PySide6.
- Matplotlib.
- NumPy.
- SciPy.

Python 3.14 is the primary development environment. Compatibility with other Python versions depends on the installed package versions.

### 2.2 Operating System

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

Activate the environment:

```powershell
.venv\Scripts\Activate.ps1
```

On Linux/macOS:

```bash
source .venv/bin/activate
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

Optik v0.2.0 provides five main pages.

| Page | Description |
|---|---|
| Home | Application overview and calculator shortcuts |
| Reflection | Reflection calculations and ray visualization |
| Refraction | Refraction, critical-angle, and total internal reflection calculations |
| Thin Lens | Lens calculations, magnification, and image formation diagrams |
| Settings | Application preferences and appearance settings |

### 4.1 Home

The Home page serves as the application's landing page.

It provides shortcuts to the available optical calculators.

Select the Thin Lens feature card to open the Thin Lens calculator.

### 4.2 Sidebar

Use the sidebar to switch between the available application pages.

The selected page appears in the main content area.

### 4.3 Settings

The Settings page provides application preferences.

Optik supports Light and Dark appearance themes.

Supported settings are saved between application sessions.

## 5. Reflection Calculator

### 5.1 Purpose

The Reflection Calculator determines the angle of reflection for an incident light ray.

The calculation follows:

**θᵣ = θᵢ**

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

**Input**

Incident Angle = 45°

**Expected output**

Reflected Angle = 45.00°

The diagram displays incident and reflected rays at equal angles to the normal.

## 6. Refraction Calculator

### 6.1 Purpose

The Refraction Calculator determines the direction of light as it passes between two optical media.

The calculation follows Snell's law:

**n₁ sin(θ₁) = n₂ sin(θ₂)**

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

**Input**

- n₁ = 1.0
- n₂ = 1.5
- Incident Angle = 30°

**Expected output**

Refracted Angle ≈ 19.47°

The refracted ray bends toward the surface normal.

## 7. Critical Angle

### 7.1 Purpose

The critical angle represents the incident angle at which the refracted ray travels along the boundary between two media.

The calculation applies when:

**n₁ > n₂**

The equation is:

**θc = arcsin(n₂ / n₁)**

### 7.2 Example

**Input**

- n₁ = 1.5
- n₂ = 1.0

**Expected output**

Critical Angle ≈ 41.81°

When n₁ ≤ n₂, the critical angle is not applicable.

## 8. Total Internal Reflection

### 8.1 Purpose

Total internal reflection occurs when light travels from a higher refractive index to a lower refractive index and the incident angle exceeds the critical angle.

### 8.2 Example

**Input**

- n₁ = 1.5
- n₂ = 1.0
- Incident Angle = 50°

**Expected output**

- Total Internal Reflection: Yes
- Critical Angle: 41.81°
- Refracted Angle: No transmitted ray (TIR)

The diagram displays incident and reflected rays without a transmitted ray.

## 9. Thin Lens Calculator

### 9.1 Purpose

The Thin Lens Calculator determines image formation properties for ideal converging and diverging lenses.

The calculator uses the thin lens equation:

**1/f = 1/dₒ + 1/dᵢ**

Where:

- f = Focal length.
- dₒ = Object distance.
- dᵢ = Image distance.

The calculator also determines magnification, image height, image orientation, and relative image size.

### 9.2 Opening the Calculator

1. Launch Optik.
2. Select **Thin Lens** from the sidebar, or open it from the Home dashboard.
3. Locate the lens input controls.

### 9.3 Input Parameters

The Thin Lens calculator accepts three main inputs.

| Input | Description |
|---|---|
| Focal Length | Focal length of the lens |
| Object Distance | Distance between the object and lens |
| Object Height | Height of the object |

Use consistent distance units. For example, enter all three measurements in centimeters.

### 9.4 Instructions

1. Open the Thin Lens page.
2. Enter the focal length.
3. Enter the object distance.
4. Enter the object height.
5. Click **Calculate**.
6. Review the image distance and magnification.
7. Review the image height, orientation, and size classification.
8. Examine the lens ray diagram.

The diagram updates when a new calculation is performed.

### 9.5 Converging Lenses

A converging lens has a positive focal length.

Depending on the object position, it may produce a real or virtual image.

**Example: Real image formation**

Input:

- Focal Length = +10 cm
- Object Distance = 30 cm
- Object Height = 5 cm

Expected results:

- Image Distance = +15 cm
- Magnification = −0.50
- Image Height = −2.50 cm
- Orientation = Inverted
- Image Size = Reduced
- Image Type = Real

The image forms on the opposite side of the lens.

### 9.6 Diverging Lenses

A diverging lens has a negative focal length.

For a real object, an ideal diverging lens produces a virtual, upright, reduced image.

**Example: Virtual image formation**

Input:

- Focal Length = −10 cm
- Object Distance = 30 cm
- Object Height = 5 cm

Expected results:

- Image Distance = −7.50 cm
- Magnification = +0.25
- Image Height = +1.25 cm
- Orientation = Upright
- Image Size = Reduced
- Image Type = Virtual

The virtual image appears on the same side of the lens as the object.

### 9.7 Object Inside the Focal Length

For a converging lens, an object positioned inside the focal length produces a virtual, upright, enlarged image.

**Example**

Input:

- Focal Length = +10 cm
- Object Distance = 5 cm
- Object Height = 2 cm

Expected results:

- Image Distance = −10 cm
- Magnification = +2.00
- Image Height = +4 cm
- Orientation = Upright
- Image Size = Enlarged
- Image Type = Virtual

### 9.8 Object at the Focal Point

When an object is located exactly at the focal point of a converging lens, the outgoing rays are parallel.

In the ideal thin lens model, the image is at infinity.

Some numerical results or diagram elements may be represented differently for this special case.

## 10. Understanding Magnification

### 10.1 Magnification Equation

Optik calculates signed magnification using:

**m = −dᵢ / dₒ**

Where:

- m = Magnification.
- dᵢ = Image distance.
- dₒ = Object distance.

### 10.2 Image Height

The image height is calculated using:

**hᵢ = m × hₒ**

Where:

- hᵢ = Image height.
- hₒ = Object height.

### 10.3 Image Orientation

| Magnification | Orientation |
|---|---|
| Negative | Inverted |
| Positive | Upright |

### 10.4 Image Size

| Magnification Magnitude | Classification |
|---|---|
| Greater than 1 | Enlarged |
| Less than 1 | Reduced |
| Equal to 1 | Same size |

Magnification describes the image size relative to the object.

## 11. Understanding the Ray Diagrams

### 11.1 Reflection and Refraction Diagrams

Optik uses a two-dimensional coordinate system to illustrate light-ray behavior.

The default visualization includes:

- **Blue:** Incident ray.
- **Orange:** Reflected ray.
- **Green:** Refracted ray.
- **Dashed vertical line:** Surface normal.
- **Horizontal line:** Optical interface.

Colors may vary with visualization settings.

### 11.2 Thin Lens Diagrams

Thin lens diagrams illustrate the relationship between the object, lens, focal points, and image.

Important elements include:

- Optical axis.
- Lens position.
- Focal points.
- Object arrow.
- Image arrow.
- Principal optical rays.

In the standard lens diagram:

- The lens is located at the center.
- The object is positioned to the left of the lens.
- Real images form on the opposite side.
- Virtual images appear on the object side.

Virtual images are identified by extending diverging rays backward to their apparent point of origin.

### 11.3 Matplotlib Navigation Toolbar

The Thin Lens visualization includes Matplotlib navigation controls.

Depending on the toolbar configuration, available controls may include:

- Home: Restore the original view.
- Back: Return to the previous view.
- Forward: Move to the next view.
- Pan: Move around the diagram.
- Zoom: Zoom into a selected region.
- Save: Save the displayed figure.

### 11.4 Diagram Limitations

Ray diagrams illustrate idealized optical geometry.

They do not represent optical intensity, diffraction, interference, or full electromagnetic wave propagation.

## 12. Input Restrictions

### 12.1 Reflection and Refraction

- Incident angles must be between 0° and 90°.
- Refractive indices must be positive.
- Numerical inputs must be valid and finite.

### 12.2 Thin Lens

- Focal length must not be zero.
- Object distance must be positive.
- Input distances must use consistent units.
- The object height must satisfy the calculator's supported input range.
- Invalid mathematical inputs may produce an error message.

The graphical interface uses numerical controls to restrict inputs to supported ranges.

## 13. Application Appearance and Settings

Optik supports Light and Dark appearance themes.

To change the theme:

1. Open the Settings page.
2. Locate the appearance setting.
3. Select the preferred theme.
4. Return to the calculator page.

The application applies the selected theme to supported interface components.

The Thin Lens Plot Manager supports matching light and dark plotting themes.

Supported application settings and calculation defaults are stored using Qt's `QSettings`.

## 14. Troubleshooting

### 14.1 Application Does Not Start

Confirm that Python and the required dependencies are installed.

Run:

```powershell
python -m pip install -r requirements.txt
```

Then retry:

```powershell
python main.py
```

### 14.2 Matplotlib Import Error

Install Matplotlib:

```powershell
python -m pip install matplotlib
```

### 14.3 PySide6 Import Error

Install PySide6:

```powershell
python -m pip install PySide6
```

### 14.4 Diagram Does Not Update

Click the Calculate button after changing the numerical inputs.

Verify that the calculation completed successfully.

### 14.5 Unexpected Refraction Results

Verify that the refractive indices are entered in the correct order.

The first index represents the incident medium, and the second represents the transmitted medium.

### 14.6 Unexpected Lens Results

Check the following:

- Focal length sign.
- Object distance.
- Object height.
- Consistent measurement units.
- Whether the image is real or virtual.

Remember that a negative image distance indicates a virtual image under the application's sign convention.

### 14.7 Lens Diagram Does Not Appear

1. Confirm that valid numerical inputs have been entered.
2. Click Calculate.
3. Check whether a calculation error was displayed.
4. Restart the application if the visualization remains unresponsive.

### 14.8 Matplotlib Toolbar Problems

Ensure that the installed Matplotlib version is compatible with the installed PySide6 version.

If a dependency error occurs, reinstall the project requirements.

## 15. Known Limitations

Optik v0.2.0 uses idealized geometrical optics calculations.

The application does not currently calculate:

- Fresnel reflectance.
- Optical power transmission.
- Polarization-dependent effects.
- Diffraction.
- Interference.
- Absorption and scattering.
- Lens aberrations.
- Thick lens behavior.
- Complex multi-element optical systems.

The application is intended for educational and computational reference purposes.

## 16. Future Development

Planned future development includes:

| Version | Planned Features |
|---|---|
| v0.3.0 | Concave and convex mirror calculations |
| v0.4.0 | Multiple lenses and optical systems |
| v0.5.0 | Wave optics |
| v0.6.0 | Interference and diffraction |
| v0.7.0 | Polarization |
| v0.8.0 | Optical materials |
| v0.9.0 | Numerical and Fourier optics |
| v1.0.0 | Stable release |

Future features and schedules are subject to change.

## 17. License

Optik is distributed under the MIT License.

Refer to the `LICENSE` file in the project root for the complete license terms.