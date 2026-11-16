
"""
Optik — Optical Dispersion Diagram Tests
Version: 0.4.0

Unit tests for visualization/dispersion_diagram.py.

Coverage:
    - Diagram initialization
    - Refractive index plots
    - Prism deviation plots
    - Visible spectrum rendering
    - Wavelength-to-RGB conversion
    - Light and dark themes
    - Clearing and redrawing
    - Image export
    - Invalid input handling

Run:
    python -m pytest tests/test_dispersion_diagram.py -v
"""

import math

import matplotlib

matplotlib.use("Agg")

import numpy as np
import pytest

from matplotlib.colors import to_rgba
from matplotlib.figure import Figure

from optics.dispersion import (
    CauchyCoefficients,
    DispersionResult,
    SpectralPrismResult,
    DispersionError,
    calculate_cauchy_index,
    calculate_spectral_prism_deviation,
)

from visualization.dispersion_diagram import (
    DispersionDiagram,
    wavelength_to_rgb,
)


# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture
def glass_coefficients():
    """Illustrative coefficients for dispersive glass."""

    return CauchyCoefficients(
        A=1.5046,
        B=0.00420,
        C=0.00012,
    )


@pytest.fixture
def constant_coefficients():
    """Coefficients for a constant refractive index."""

    return CauchyCoefficients(
        A=1.5,
        B=0.0,
        C=0.0,
    )


@pytest.fixture
def diagram():
    """Create a light-theme dispersion diagram."""

    figure = Figure(figsize=(9, 6))

    return DispersionDiagram(
        figure=figure,
        dark_mode=False,
    )


@pytest.fixture
def dark_diagram():
    """Create a dark-theme dispersion diagram."""

    figure = Figure(figsize=(9, 6))

    return DispersionDiagram(
        figure=figure,
        dark_mode=True,
    )


# ============================================================
# INITIALIZATION TESTS
# ============================================================

class TestDispersionDiagramInitialization:

    def test_creates_figure(self, diagram):
        assert isinstance(diagram.figure, Figure)

    def test_creates_axes(self, diagram):
        assert diagram.ax is not None
        assert diagram.ax in diagram.figure.axes

    def test_uses_supplied_figure(self):
        figure = Figure(figsize=(10, 7))

        diagram = DispersionDiagram(figure=figure)

        assert diagram.figure is figure

    def test_initial_results_empty(self, diagram):
        assert diagram.last_results == []

    def test_initial_light_mode(self, diagram):
        assert diagram.dark_mode is False

    def test_initial_dark_mode(self, dark_diagram):
        assert dark_diagram.dark_mode is True


# ============================================================
# WAVELENGTH COLOR TESTS
# ============================================================

class TestWavelengthToRGB:

    @pytest.mark.parametrize(
        "wavelength",
        [
            380.0,
            400.0,
            440.0,
            470.0,
            490.0,
            510.0,
            550.0,
            580.0,
            620.0,
            645.0,
            700.0,
            750.0,
        ],
    )
    def test_rgb_values_in_range(self, wavelength):
        color = wavelength_to_rgb(wavelength)

        assert len(color) == 3

        assert all(
            0.0 <= component <= 1.0
            for component in color
        )

    def test_outside_visible_range(self):
        assert wavelength_to_rgb(300.0) == (
            0.5, 0.5, 0.5
        )

        assert wavelength_to_rgb(800.0) == (
            0.5, 0.5, 0.5
        )

    def test_green_wavelength(self):
        red, green, blue = wavelength_to_rgb(530.0)

        assert green == pytest.approx(1.0)
        assert blue == pytest.approx(0.0)
        assert red > 0.0

    def test_blue_wavelength(self):
        red, green, blue = wavelength_to_rgb(470.0)

        assert red == pytest.approx(0.0)
        assert blue == pytest.approx(1.0)
        assert green > 0.0

    def test_red_wavelength(self):
        red, green, blue = wavelength_to_rgb(700.0)

        assert red == pytest.approx(1.0)
        assert green == pytest.approx(0.0)
        assert blue == pytest.approx(0.0)


# ============================================================
# REFRACTIVE INDEX PLOT TESTS
# ============================================================

class TestRefractiveIndexPlot:

    def test_returns_dispersion_results(
        self,
        diagram,
        glass_coefficients,
    ):
        results = diagram.draw_refractive_index(
            glass_coefficients,
            samples=10,
        )

        assert len(results) == 10

        assert all(
            isinstance(result, DispersionResult)
            for result in results
        )

    def test_stores_last_results(
        self,
        diagram,
        glass_coefficients,
    ):
        results = diagram.draw_refractive_index(
            glass_coefficients,
            samples=10,
        )

        assert diagram.last_results is results

    def test_creates_one_line(
        self,
        diagram,
        glass_coefficients,
    ):
        diagram.draw_refractive_index(
            glass_coefficients,
            samples=10,
        )

        assert len(diagram.ax.lines) == 1

    def test_wavelength_axis_data(
        self,
        diagram,
        glass_coefficients,
    ):
        results = diagram.draw_refractive_index(
            glass_coefficients,
            start_wavelength_nm=400.0,
            end_wavelength_nm=700.0,
            samples=4,
        )

        x_data = diagram.ax.lines[0].get_xdata()

        assert x_data == pytest.approx(
            [400.0, 500.0, 600.0, 700.0]
        )

        assert len(results) == 4

    def test_refractive_index_axis_data(
        self,
        diagram,
        glass_coefficients,
    ):
        diagram.draw_refractive_index(
            glass_coefficients,
            start_wavelength_nm=400.0,
            end_wavelength_nm=700.0,
            samples=4,
        )

        line = diagram.ax.lines[0]

        wavelengths = line.get_xdata()
        indices = line.get_ydata()

        expected = [
            calculate_cauchy_index(
                wavelength,
                glass_coefficients,
            )
            for wavelength in wavelengths
        ]

        assert indices == pytest.approx(expected)

    def test_plot_title(
        self,
        diagram,
        glass_coefficients,
    ):
        diagram.draw_refractive_index(
            glass_coefficients,
        )

        assert diagram.ax.get_title() == (
            "Refractive Index vs Wavelength"
        )

    def test_axis_labels(
        self,
        diagram,
        glass_coefficients,
    ):
        diagram.draw_refractive_index(
            glass_coefficients,
        )

        assert diagram.ax.get_xlabel() == "Wavelength (nm)"
        assert diagram.ax.get_ylabel() == "Refractive Index"

    def test_normal_dispersion_curve(
        self,
        diagram,
        glass_coefficients,
    ):
        diagram.draw_refractive_index(
            glass_coefficients,
            samples=20,
        )

        indices = diagram.ax.lines[0].get_ydata()

        assert indices[0] > indices[-1]

    def test_constant_index_horizontal_line(
        self,
        diagram,
        constant_coefficients,
    ):
        diagram.draw_refractive_index(
            constant_coefficients,
            samples=10,
        )

        indices = diagram.ax.lines[0].get_ydata()

        assert np.allclose(indices, 1.5)


# ============================================================
# PRISM DEVIATION PLOT TESTS
# ============================================================

class TestPrismDeviationPlot:

    def test_returns_spectral_prism_results(
        self,
        diagram,
        glass_coefficients,
    ):
        results = diagram.draw_prism_deviation(
            apex_angle=60.0,
            incident_angle=50.0,
            coefficients=glass_coefficients,
            samples=10,
        )

        assert len(results) == 10

        assert all(
            isinstance(result, SpectralPrismResult)
            for result in results
        )

    def test_creates_one_line(
        self,
        diagram,
        glass_coefficients,
    ):
        diagram.draw_prism_deviation(
            60.0,
            50.0,
            glass_coefficients,
            samples=10,
        )

        assert len(diagram.ax.lines) == 1

    def test_deviation_matches_calculations(
        self,
        diagram,
        glass_coefficients,
    ):
        results = diagram.draw_prism_deviation(
            60.0,
            50.0,
            glass_coefficients,
            samples=5,
        )

        expected = calculate_spectral_prism_deviation(
            apex_angle=60.0,
            incident_angle=50.0,
            coefficients=glass_coefficients,
            samples=5,
        )

        plotted = diagram.ax.lines[0].get_ydata()

        assert plotted == pytest.approx(
            [item.deviation_angle for item in expected]
        )

        assert len(results) == len(expected)

    def test_prism_deviation_axis_labels(
        self,
        diagram,
        glass_coefficients,
    ):
        diagram.draw_prism_deviation(
            60.0,
            50.0,
            glass_coefficients,
        )

        assert diagram.ax.get_xlabel() == "Wavelength (nm)"
        assert diagram.ax.get_ylabel() == (
            "Deviation Angle (degrees)"
        )

    def test_short_wavelength_greater_deviation(
        self,
        diagram,
        glass_coefficients,
    ):
        diagram.draw_prism_deviation(
            60.0,
            50.0,
            glass_coefficients,
            samples=10,
        )

        deviations = diagram.ax.lines[0].get_ydata()

        assert deviations[0] > deviations[-1]

    def test_constant_index_constant_deviation(
        self,
        diagram,
        constant_coefficients,
    ):
        diagram.draw_prism_deviation(
            60.0,
            50.0,
            constant_coefficients,
            samples=10,
        )

        deviations = diagram.ax.lines[0].get_ydata()

        assert np.allclose(
            deviations,
            deviations[0],
        )


# ============================================================
# VISIBLE SPECTRUM TESTS
# ============================================================

class TestVisibleSpectrum:

    def test_creates_spectrum_image(self, diagram):
        diagram.draw_visible_spectrum()

        assert len(diagram.ax.images) == 1

    def test_spectrum_has_rgb_channels(self, diagram):
        diagram.draw_visible_spectrum(samples=20)

        image = diagram.ax.images[0].get_array()

        assert image.shape == (30, 20, 3)

    def test_spectrum_wavelength_extent(self, diagram):
        diagram.draw_visible_spectrum(
            start_wavelength_nm=400.0,
            end_wavelength_nm=700.0,
            samples=20,
        )

        extent = diagram.ax.images[0].get_extent()

        assert extent == pytest.approx(
            [400.0, 700.0, 0.0, 1.0]
        )

    def test_spectrum_title(self, diagram):
        diagram.draw_visible_spectrum()

        assert diagram.ax.get_title() == (
            "Visible Light Spectrum"
        )

    def test_spectrum_has_no_results(self, diagram):
        diagram.draw_visible_spectrum()

        assert diagram.last_results == []

    def test_invalid_spectrum_sample_count(self, diagram):
        with pytest.raises(ValueError):
            diagram.draw_visible_spectrum(samples=1)

    def test_invalid_spectrum_range(self, diagram):
        with pytest.raises(ValueError):
            diagram.draw_visible_spectrum(
                start_wavelength_nm=700.0,
                end_wavelength_nm=400.0,
            )


# ============================================================
# THEME TESTS
# ============================================================

class TestDispersionDiagramThemes:

    def test_light_background(self, diagram):
        assert diagram.figure.get_facecolor() == pytest.approx(
            to_rgba("#FFFFFF")
        )

    def test_dark_background(self, dark_diagram):
        assert dark_diagram.figure.get_facecolor() == pytest.approx(
            to_rgba("#1E1E1E")
        )

    def test_switch_to_dark_mode(self, diagram):
        diagram.set_dark_mode(True)

        assert diagram.dark_mode is True

        assert diagram.figure.get_facecolor() == pytest.approx(
            to_rgba("#1E1E1E")
        )

    def test_switch_to_light_mode(self, dark_diagram):
        dark_diagram.set_dark_mode(False)

        assert dark_diagram.dark_mode is False

        assert dark_diagram.figure.get_facecolor() == pytest.approx(
            to_rgba("#FFFFFF")
        )

    def test_theme_preserves_results(
        self,
        diagram,
        glass_coefficients,
    ):
        results = diagram.draw_refractive_index(
            glass_coefficients,
        )

        diagram.set_dark_mode(True)

        assert diagram.last_results is results


# ============================================================
# CLEAR AND REDRAW TESTS
# ============================================================

class TestDispersionDiagramClear:

    def test_clear_removes_lines(
        self,
        diagram,
        glass_coefficients,
    ):
        diagram.draw_refractive_index(
            glass_coefficients,
        )

        diagram.clear()

        assert len(diagram.ax.lines) == 0

    def test_clear_removes_images(self, diagram):
        diagram.draw_visible_spectrum()

        diagram.clear()

        assert len(diagram.ax.images) == 0

    def test_clear_resets_results(
        self,
        diagram,
        glass_coefficients,
    ):
        diagram.draw_refractive_index(
            glass_coefficients,
        )

        diagram.clear()

        assert diagram.last_results == []

    def test_redraw_replaces_previous_plot(
        self,
        diagram,
        glass_coefficients,
    ):
        diagram.draw_refractive_index(
            glass_coefficients,
        )

        diagram.draw_prism_deviation(
            60.0,
            50.0,
            glass_coefficients,
        )

        assert len(diagram.ax.lines) == 1

        assert diagram.ax.get_title() == (
            "Prism Deviation vs Wavelength"
        )

    def test_switch_from_spectrum_to_curve(
        self,
        diagram,
        glass_coefficients,
    ):
        diagram.draw_visible_spectrum()

        diagram.draw_refractive_index(
            glass_coefficients,
        )

        assert len(diagram.ax.images) == 0
        assert len(diagram.ax.lines) == 1


# ============================================================
# EXPORT TESTS
# ============================================================

class TestDispersionDiagramExport:

    @pytest.mark.parametrize(
        "extension",
        ["png", "svg", "pdf"],
    )
    def test_save_plot(
        self,
        diagram,
        glass_coefficients,
        tmp_path,
        extension,
    ):
        diagram.draw_refractive_index(
            glass_coefficients,
        )

        output = tmp_path / f"dispersion.{extension}"

        diagram.save(str(output))

        assert output.exists()
        assert output.stat().st_size > 0

    def test_save_spectrum(
        self,
        diagram,
        tmp_path,
    ):
        diagram.draw_visible_spectrum()

        output = tmp_path / "visible_spectrum.png"

        diagram.save(str(output))

        assert output.exists()
        assert output.stat().st_size > 0

    def test_save_custom_dpi(
        self,
        diagram,
        glass_coefficients,
        tmp_path,
    ):
        diagram.draw_refractive_index(
            glass_coefficients,
        )

        output = tmp_path / "dispersion_300dpi.png"

        diagram.save(str(output), dpi=300)

        assert output.exists()
        assert output.stat().st_size > 0


# ============================================================
# ERROR HANDLING TESTS
# ============================================================

class TestDispersionDiagramErrors:

    def test_invalid_coefficients(self, diagram):
        with pytest.raises(DispersionError):
            diagram.draw_refractive_index(
                coefficients=None,
            )

    def test_invalid_wavelength_range(
        self,
        diagram,
        glass_coefficients,
    ):
        with pytest.raises(DispersionError):
            diagram.draw_refractive_index(
                coefficients=glass_coefficients,
                start_wavelength_nm=700.0,
                end_wavelength_nm=400.0,
            )

    def test_invalid_sample_count(
        self,
        diagram,
        glass_coefficients,
    ):
        with pytest.raises(DispersionError):
            diagram.draw_refractive_index(
                coefficients=glass_coefficients,
                samples=1,
            )

    def test_invalid_prism_geometry(
        self,
        diagram,
        glass_coefficients,
    ):
        with pytest.raises(DispersionError):
            diagram.draw_prism_deviation(
                apex_angle=90.0,
                incident_angle=20.0,
                coefficients=glass_coefficients,
            )


# ============================================================
# TEST MODULE EXECUTION
# ============================================================

if __name__ == "__main__":
    raise SystemExit(
        pytest.main([__file__, "-v"])
    )
