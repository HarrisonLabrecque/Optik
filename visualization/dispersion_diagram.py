
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
    - Validation of spectral plotting data

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

    This is an illustrative approximation, not a
    colorimetrically accurate conversion.
    """

    wavelength = float(wavelength_nm)

    if not np.isfinite(wavelength):
        raise ValueError(
            "Wavelength must be a finite number."
        )

    if wavelength < 380.0 or wavelength > 750.0:
        return (0.5, 0.5, 0.5)

    if wavelength < 440.0:
        red = -(wavelength - 440.0) / 60.0
        green = 0.0
        blue = 1.0

    elif wavelength < 490.0:
        red = 0.0
        green = (wavelength - 440.0) / 50.0
        blue = 1.0

    elif wavelength < 510.0:
        red = 0.0
        green = 1.0
        blue = -(wavelength - 510.0) / 20.0

    elif wavelength < 580.0:
        red = (wavelength - 510.0) / 70.0
        green = 1.0
        blue = 0.0

    elif wavelength < 645.0:
        red = 1.0
        green = -(wavelength - 645.0) / 65.0
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
            figure
            if figure is not None
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

        for text in self.ax.get_legend().get_texts() \
                if self.ax.get_legend() else []:
            text.set_color(foreground)

    def set_dark_mode(self, enabled: bool) -> None:
        """Change the diagram theme."""

        self.dark_mode = bool(enabled)
        self._apply_theme()
        self._refresh_canvas()

    # ========================================================
    # CANVAS REFRESH
    # ========================================================

    def _refresh_canvas(self) -> None:
        """Request a Matplotlib canvas redraw."""

        canvas = self.figure.canvas

        if canvas is not None:
            canvas.draw_idle()

    # ========================================================
    # SPECTRAL DATA VALIDATION
    # ========================================================

    @staticmethod
    def _filter_finite_results(
        results: list[
            DispersionResult | SpectralPrismResult
        ],
        y_attribute: str,
    ) -> list[
        DispersionResult | SpectralPrismResult
    ]:
        """Keep results containing finite plot coordinates."""

        valid_results = []

        for result in results:
            wavelength = float(result.wavelength_nm)
            value = float(
                getattr(result, y_attribute)
            )

            if (
                np.isfinite(wavelength)
                and np.isfinite(value)
            ):
                valid_results.append(result)

        return valid_results

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
            Valid calculated spectral refractive indices.
        """

        results = calculate_spectral_dispersion(
            start_wavelength_nm,
            end_wavelength_nm,
            coefficients,
            samples,
        )

        valid_results = self._filter_finite_results(
            results,
            "refractive_index",
        )

        if not valid_results:
            raise ValueError(
                "No valid refractive index values "
                "were calculated for this wavelength range."
            )

        wavelengths = np.array(
            [
                result.wavelength_nm
                for result in valid_results
            ],
            dtype=float,
        )

        indices = np.array(
            [
                result.refractive_index
                for result in valid_results
            ],
            dtype=float,
        )

        self.clear()

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

        self.last_results = valid_results

        self._finalize()

        return valid_results

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

        Invalid or non-finite data points are excluded.

        Raises
        ------
        ValueError
            If no valid prism deviation values exist.
        """

        results = calculate_spectral_prism_deviation(
            apex_angle=apex_angle,
            incident_angle=incident_angle,
            coefficients=coefficients,
            start_wavelength_nm=start_wavelength_nm,
            end_wavelength_nm=end_wavelength_nm,
            samples=samples,
        )

        valid_results = self._filter_finite_results(
            results,
            "deviation_angle",
        )

        if not valid_results:
            raise ValueError(
                "No valid prism deviation values were "
                "calculated. Check the apex angle, "
                "incident angle, refractive index, "
                "and wavelength range."
            )

        wavelengths = np.array(
            [
                result.wavelength_nm
                for result in valid_results
            ],
            dtype=float,
        )

        deviations = np.array(
            [
                result.deviation_angle
                for result in valid_results
            ],
            dtype=float,
        )

        self.clear()

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
        self.ax.set_ylabel(
            "Deviation Angle (degrees)"
        )

        self.last_results = valid_results

        self._finalize()

        return valid_results

    # ========================================================
    # VISIBLE SPECTRUM DIAGRAM
    # ========================================================

    def draw_visible_spectrum(
        self,
        start_wavelength_nm: float = VISIBLE_MIN_NM,
        end_wavelength_nm: float = VISIBLE_MAX_NM,
        samples: int = 100,
    ) -> None:
        """Draw an illustrative visible-spectrum strip."""

        if (
            not isinstance(samples, int)
            or isinstance(samples, bool)
        ):
            raise ValueError(
                "Sample count must be an integer."
            )

        if samples < 2:
            raise ValueError(
                "Sample count must be at least 2."
            )

        start = float(start_wavelength_nm)
        end = float(end_wavelength_nm)

        if not (
            np.isfinite(start)
            and np.isfinite(end)
            and start < end
        ):
            raise ValueError(
                "Invalid wavelength range."
            )

        wavelengths = np.linspace(
            start,
            end,
            samples,
        )

        colors = np.array(
            [
                wavelength_to_rgb(wavelength)
                for wavelength in wavelengths
            ]
        )

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

        self.ax.set_title(
            "Visible Light Spectrum"
        )

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
            handles, labels = (
                self.ax.get_legend_handles_labels()
            )

            if handles:
                self.ax.legend(loc="best")

        self._apply_theme()

        self.figure.tight_layout()

        self._refresh_canvas()

    # ========================================================
    # CLEAR
    # ========================================================

    def clear(self) -> None:
        """Clear the current diagram."""

        self.ax.clear()
        self.last_results = []

        self._apply_theme()
        self._refresh_canvas()

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

    try:
        results = diagram.draw_prism_deviation(
            apex_angle=45.0,
            incident_angle=40.0,
            coefficients=coefficients,
            samples=100,
        )

        print(
            "Calculated deviation points:",
            len(results),
        )

        print(
            "First deviation:",
            results[0].deviation_angle,
        )

        print(
            "Last deviation:",
            results[-1].deviation_angle,
        )

        plt.show()

    except (ValueError, ArithmeticError) as exc:
        print(
            "Prism deviation plotting failed:",
            exc,
        )
