
"""
Optik — Optical Dispersion Diagram
Version: 0.4.0

Matplotlib visualization for wavelength-dependent
refractive index and prism angular deviation.

Features:
    - Refractive index versus wavelength
    - Prism deviation versus wavelength
    - Visible spectrum color visualization
    - Light and dark themes
    - Diagram export
    - Diagram clearing
    - Integration with Cauchy's dispersion model

Dependencies:
    matplotlib
    numpy

Related modules:
    optics/dispersion.py
    optics/prisms.py
"""

from __future__ import annotations

from typing import Optional

import matplotlib.pyplot as plt
import numpy as np

from matplotlib.figure import Figure
from matplotlib.colors import to_rgba

from optics.dispersion import (
    CauchyCoefficients,
    DispersionResult,
    SpectralPrismResult,
    calculate_spectral_dispersion,
    calculate_spectral_prism_deviation,
    VISIBLE_MIN_NM,
    VISIBLE_MAX_NM,
)


# ============================================================
# CONSTANTS
# ============================================================

DEFAULT_START_WAVELENGTH = VISIBLE_MIN_NM
DEFAULT_END_WAVELENGTH = VISIBLE_MAX_NM

DEFAULT_SAMPLES = 100

LIGHT_BACKGROUND = "#FFFFFF"
DARK_BACKGROUND = "#1E1E1E"

LIGHT_FOREGROUND = "#202020"
DARK_FOREGROUND = "#F0F0F0"

REFRACTIVE_INDEX_COLOR = "#0072B2"
DEVIATION_COLOR = "#D55E00"


# ============================================================
# WAVELENGTH COLOR CONVERSION
# ============================================================

def wavelength_to_rgb(
    wavelength_nm: float,
) -> tuple[float, float, float]:
    """
    Approximate a visible wavelength as an RGB color.

    Parameters
    ----------
    wavelength_nm : float
        Wavelength in nanometers.

    Returns
    -------
    tuple[float, float, float]
        RGB values between 0 and 1.

    Notes
    -----
    This is an illustrative color approximation.
    It is not a colorimetric conversion.
    """

    wavelength = float(wavelength_nm)

    if wavelength < 380.0 or wavelength > 750.0:
        return (0.5, 0.5, 0.5)

    if wavelength < 440.0:
        red = -(wavelength - 440.0) / (440.0 - 380.0)
        green = 0.0
        blue = 1.0

    elif wavelength < 490.0:
        red = 0.0
        green = (wavelength - 440.0) / (490.0 - 440.0)
        blue = 1.0

    elif wavelength < 510.0:
        red = 0.0
        green = 1.0
        blue = -(wavelength - 510.0) / (510.0 - 490.0)

    elif wavelength < 580.0:
        red = (wavelength - 510.0) / (580.0 - 510.0)
        green = 1.0
        blue = 0.0

    elif wavelength < 645.0:
        red = 1.0
        green = -(wavelength - 645.0) / (645.0 - 580.0)
        blue = 0.0

    else:
        red = 1.0
        green = 0.0
        blue = 0.0

    return (
        float(np.clip(red, 0.0, 1.0)),
        float(np.clip(green, 0.0, 1.0)),
        float(np.clip(blue, 0.0, 1.0)),
    )


# ============================================================
# DISPERSION DIAGRAM
# ============================================================

class DispersionDiagram:
    """
    Matplotlib-based optical dispersion visualization.

    Parameters
    ----------
    figure : Figure, optional
        Existing Matplotlib figure.

    dark_mode : bool
        Enable dark theme.
    """

    def __init__(
        self,
        figure: Optional[Figure] = None,
        dark_mode: bool = False,
    ) -> None:

        self.figure = (
            figure if figure is not None
            else Figure(figsize=(9, 6))
        )

        self.ax = self.figure.add_subplot(111)

        self.dark_mode = bool(dark_mode)

        self.last_results: list[
            DispersionResult | SpectralPrismResult
        ] = []

        self._apply_theme()

    # ========================================================
    # THEME
    # ========================================================

    def _apply_theme(self) -> None:
        """Apply light or dark theme colors."""

        background = (
            DARK_BACKGROUND
            if self.dark_mode
            else LIGHT_BACKGROUND
        )

        foreground = (
            DARK_FOREGROUND
            if self.dark_mode
            else LIGHT_FOREGROUND
        )

        self.figure.patch.set_facecolor(background)
        self.ax.set_facecolor(background)

        self.ax.tick_params(colors=foreground)

        for spine in self.ax.spines.values():
            spine.set_color(foreground)

        self.ax.xaxis.label.set_color(foreground)
        self.ax.yaxis.label.set_color(foreground)
        self.ax.title.set_color(foreground)

    def set_dark_mode(self, enabled: bool) -> None:
        """Change the diagram theme."""

        self.dark_mode = bool(enabled)
        self._apply_theme()

        if self.figure.canvas is not None:
            self.figure.canvas.draw_idle()

    # ========================================================
    # REFRACTIVE INDEX DIAGRAM
    # ========================================================

    def draw_refractive_index(
        self,
        coefficients: CauchyCoefficients,
        start_wavelength_nm: float = DEFAULT_START_WAVELENGTH,
        end_wavelength_nm: float = DEFAULT_END_WAVELENGTH,
        samples: int = DEFAULT_SAMPLES,
    ) -> list[DispersionResult]:
        """
        Draw refractive index versus wavelength.

        Returns
        -------
        list[DispersionResult]
            Calculated spectral refractive indices.
        """

        results = calculate_spectral_dispersion(
            start_wavelength_nm,
            end_wavelength_nm,
            coefficients,
            samples,
        )

        self.clear()

        wavelengths = np.array([
            result.wavelength_nm
            for result in results
        ])

        indices = np.array([
            result.refractive_index
            for result in results
        ])

        self.ax.plot(
            wavelengths,
            indices,
            color=REFRACTIVE_INDEX_COLOR,
            linewidth=2.5,
            label="Refractive Index",
        )

        self.ax.set_title(
            "Refractive Index vs Wavelength"
        )

        self.ax.set_xlabel("Wavelength (nm)")
        self.ax.set_ylabel("Refractive Index")

        self.last_results = results

        self._finalize()

        return results

    # ========================================================
    # PRISM DEVIATION DIAGRAM
    # ========================================================

    def draw_prism_deviation(
        self,
        apex_angle: float,
        incident_angle: float,
        coefficients: CauchyCoefficients,
        start_wavelength_nm: float = DEFAULT_START_WAVELENGTH,
        end_wavelength_nm: float = DEFAULT_END_WAVELENGTH,
        samples: int = DEFAULT_SAMPLES,
    ) -> list[SpectralPrismResult]:
        """
        Draw prism deviation angle versus wavelength.

        Returns
        -------
        list[SpectralPrismResult]
            Calculated prism deviations.
        """

        results = calculate_spectral_prism_deviation(
            apex_angle=apex_angle,
            incident_angle=incident_angle,
            coefficients=coefficients,
            start_wavelength_nm=start_wavelength_nm,
            end_wavelength_nm=end_wavelength_nm,
            samples=samples,
        )

        self.clear()

        wavelengths = np.array([
            result.wavelength_nm
            for result in results
        ])

        deviations = np.array([
            result.deviation_angle
            for result in results
        ])

        self.ax.plot(
            wavelengths,
            deviations,
            color=DEVIATION_COLOR,
            linewidth=2.5,
            label="Prism Deviation",
        )

        self.ax.set_title(
            "Prism Deviation vs Wavelength"
        )

        self.ax.set_xlabel("Wavelength (nm)")
        self.ax.set_ylabel("Deviation Angle (degrees)")

        self.last_results = results

        self._finalize()

        return results

    # ========================================================
    # SPECTRAL COLOR DIAGRAM
    # ========================================================

    def draw_visible_spectrum(
        self,
        start_wavelength_nm: float = VISIBLE_MIN_NM,
        end_wavelength_nm: float = VISIBLE_MAX_NM,
        samples: int = 100,
    ) -> None:
        """
        Draw an illustrative visible-spectrum color strip.

        The color strip represents approximate RGB colors
        across visible wavelengths.
        """

        if not isinstance(samples, int) or isinstance(samples, bool):
            raise ValueError("Sample count must be an integer.")

        if samples < 2:
            raise ValueError("Sample count must be at least 2.")

        start = float(start_wavelength_nm)
        end = float(end_wavelength_nm)

        if not (
            np.isfinite(start)
            and np.isfinite(end)
            and start < end
        ):
            raise ValueError("Invalid wavelength range.")

        wavelengths = np.linspace(
            start,
            end,
            samples,
        )

        colors = np.array([
            wavelength_to_rgb(wavelength)
            for wavelength in wavelengths
        ])

        strip = np.tile(
            colors[np.newaxis, :, :],
            (30, 1, 1),
        )

        self.clear()

        self.ax.imshow(
            strip,
            aspect="auto",
            extent=[start, end, 0, 1],
            origin="lower",
        )

        self.ax.set_title("Visible Light Spectrum")
        self.ax.set_xlabel("Wavelength (nm)")
        self.ax.set_yticks([])

        self.last_results = []

        self._finalize(show_legend=False)

    # ========================================================
    # FINALIZE
    # ========================================================

    def _finalize(
        self,
        show_legend: bool = True,
    ) -> None:
        """Finalize plot formatting."""

        self.ax.grid(
            True,
            linestyle="--",
            alpha=0.2,
        )

        if show_legend:
            self.ax.legend(loc="best")

        self._apply_theme()

        self.figure.tight_layout()

        if self.figure.canvas is not None:
            self.figure.canvas.draw_idle()

    # ========================================================
    # CLEAR
    # ========================================================

    def clear(self) -> None:
        """Clear the current diagram."""

        self.ax.clear()
        self.last_results = []

        self._apply_theme()

        if self.figure.canvas is not None:
            self.figure.canvas.draw_idle()

    # ========================================================
    # SAVE
    # ========================================================

    def save(
        self,
        filename: str,
        dpi: int = 150,
    ) -> None:
        """Export the current diagram."""

        self.figure.savefig(
            filename,
            dpi=dpi,
            bbox_inches="tight",
        )


# ============================================================
# STANDALONE PREVIEW
# ============================================================

if __name__ == "__main__":

    coefficients = CauchyCoefficients(
        A=1.5046,
        B=0.00420,
        C=0.00012,
    )

    diagram = DispersionDiagram()

    diagram.draw_refractive_index(
        coefficients=coefficients,
        samples=100,
    )

    plt.show()
